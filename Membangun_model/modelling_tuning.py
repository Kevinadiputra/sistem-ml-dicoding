import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, learning_curve
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score, 
    confusion_matrix, 
    ConfusionMatrixDisplay, 
    classification_report
)

# --- DagsHub Integration ---
# Replace 'USERNAME' and 'PROJECT' with your DagsHub username and project name.
# Or set DAGSHUB_USERNAME and DAGSHUB_REPO environment variables.
repo_owner = os.getenv("DAGSHUB_USERNAME", "USERNAME")
repo_name = os.getenv("DAGSHUB_REPO", "PROJECT")

if repo_owner != "USERNAME" and repo_name != "PROJECT":
    try:
        import dagshub
        print(f"Initializing DagsHub integration for {repo_owner}/{repo_name}...")
        dagshub.init(repo_owner=repo_owner, repo_name=repo_name, mlflow=True)
    except Exception as e:
        print(f"DagsHub initialization failed: {e}. Falling back to local tracking.")
else:
    print("DagsHub placeholders ('USERNAME' or 'PROJECT') detected. Running MLflow locally.")

def train_tuning():
    # Set experiment
    mlflow.set_experiment("Heart_Disease_Tuning")
    
    # Load dataset
    train_path = "dataset_preprocessed/train.csv"
    test_path = "dataset_preprocessed/test.csv"
    
    if not os.path.exists(train_path) or not os.path.exists(test_path):
        raise FileNotFoundError("Preprocessed data not found. Please run preprocessing first.")
        
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    X_train = train_df.drop(columns=['target'])
    y_train = train_df['target']
    X_test = test_df.drop(columns=['target'])
    y_test = test_df['target']
    
    # Define hyperparameter grid
    param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [3, 5, 7, None],
        'min_samples_split': [2, 5]
    }
    
    print("Running GridSearchCV hyperparameter tuning...")
    base_model = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(
        estimator=base_model, 
        param_grid=param_grid, 
        cv=5, 
        scoring='accuracy', 
        n_jobs=-1
    )
    
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    
    print(f"Best Parameters: {best_params}")
    
    # Evaluate best model
    preds = best_model.predict(X_test)
    probs = best_model.predict_proba(X_test)[:, 1]
    
    # Calculate Metrics
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, average='weighted')
    rec = recall_score(y_test, preds, average='weighted')
    f1 = f1_score(y_test, preds, average='weighted')
    
    print(f"Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}")
    
    # Manual MLflow Logging
    with mlflow.start_run() as run:
        # Log parameters
        print("Logging parameters manually...")
        for param_name, param_val in best_params.items():
            mlflow.log_param(param_name, param_val)
        
        # Log all tested hyperparameters from grid (optional but good practice)
        mlflow.log_param("tuning_algorithm", "GridSearchCV")
        
        # Log metrics
        print("Logging metrics manually...")
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", prec)
        mlflow.log_metric("recall", rec)
        mlflow.log_metric("f1_score", f1)
        
        # Create Artifacts directory
        artifacts_dir = "artifacts"
        os.makedirs(artifacts_dir, exist_ok=True)
        
        # 1. Confusion Matrix Plot
        print("Generating confusion matrix...")
        cm_path = os.path.join(artifacts_dir, "confusion_matrix.png")
        cm = confusion_matrix(y_test, preds)
        plt.figure(figsize=(6, 5))
        ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Normal", "Heart Disease"]).plot(cmap='Blues', ax=plt.gca())
        plt.title("Confusion Matrix")
        plt.tight_layout()
        plt.savefig(cm_path)
        plt.close()
        mlflow.log_artifact(cm_path)
        
        # 2. Feature Importance Plot
        print("Generating feature importance...")
        fi_path = os.path.join(artifacts_dir, "feature_importance.png")
        importances = best_model.feature_importances_
        indices = np.argsort(importances)[::-1]
        features = X_train.columns
        plt.figure(figsize=(10, 6))
        plt.title("Feature Importance - Random Forest")
        plt.bar(range(X_train.shape[1]), importances[indices], align="center", color="skyblue")
        plt.xticks(range(X_train.shape[1]), [features[i] for i in indices], rotation=90)
        plt.tight_layout()
        plt.savefig(fi_path)
        plt.close()
        mlflow.log_artifact(fi_path)
        
        # 3. Classification Report Text
        print("Generating classification report...")
        report_path = os.path.join(artifacts_dir, "classification_report.txt")
        report_str = classification_report(y_test, preds, target_names=["Normal", "Heart Disease"])
        with open(report_path, "w") as f:
            f.write(report_str)
        mlflow.log_artifact(report_path)
        
        # 4. Learning Curve Plot
        print("Generating learning curve...")
        lc_path = os.path.join(artifacts_dir, "learning_curve.png")
        train_sizes, train_scores, test_scores = learning_curve(
            best_model, X_train, y_train, cv=5, n_jobs=-1, 
            train_sizes=np.linspace(0.1, 1.0, 5), random_state=42
        )
        train_mean = np.mean(train_scores, axis=1)
        test_mean = np.mean(test_scores, axis=1)
        plt.figure(figsize=(8, 5))
        plt.plot(train_sizes, train_mean, 'o-', color="r", label="Training score")
        plt.plot(train_sizes, test_mean, 'o-', color="g", label="Cross-validation score")
        plt.title("Learning Curve (Random Forest)")
        plt.xlabel("Training Examples")
        plt.ylabel("Score (Accuracy)")
        plt.legend(loc="best")
        plt.tight_layout()
        plt.savefig(lc_path)
        plt.close()
        mlflow.log_artifact(lc_path)
        
        # 5. Prediction Distribution Plot
        print("Generating prediction distribution...")
        pd_path = os.path.join(artifacts_dir, "prediction_distribution.png")
        plt.figure(figsize=(8, 5))
        sns.histplot(probs, kde=True, bins=15, color="purple")
        plt.title("Prediction Probability Distribution (Heart Disease)")
        plt.xlabel("Predicted Probability")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(pd_path)
        plt.close()
        mlflow.log_artifact(pd_path)
        
        # Log model
        mlflow.sklearn.log_model(best_model, "best_model_sklearn")
        
        print("Tuning experimentation complete! All artifacts and metrics logged manually.")

if __name__ == "__main__":
    train_tuning()
