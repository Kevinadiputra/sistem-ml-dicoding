import os
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def train_autolog():
    # Set Experiment Name
    mlflow.set_experiment("Heart_Disease_Autolog")
    
    # Enable autologging
    mlflow.sklearn.autolog()
    
    # Load preprocessed datasets
    train_path = "dataset_preprocessed/train.csv"
    test_path = "dataset_preprocessed/test.csv"
    
    # Path fallbacks for running from root vs running from inside Membangun_model
    if not os.path.exists(train_path) or not os.path.exists(test_path):
        fallback_path = os.path.join("Membangun_model", train_path)
        if os.path.exists(fallback_path):
            train_path = fallback_path
            test_path = os.path.join("Membangun_model", test_path)
        else:
            fallback_path2 = os.path.join("preprocessing", train_path)
            if os.path.exists(fallback_path2):
                train_path = fallback_path2
                test_path = os.path.join("preprocessing", test_path)
            else:
                raise FileNotFoundError("Preprocessed data not found. Please run preprocessing first.")
        
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    # Split features and target
    X_train = train_df.drop(columns=['target'])
    y_train = train_df['target']
    X_test = test_df.drop(columns=['target'])
    y_test = test_df['target']
    
    print("Training RandomForest model with autologging...")
    with mlflow.start_run() as run:
        # Base Random Forest model
        model = RandomForestClassifier(
            n_estimators=100, 
            max_depth=5, 
            min_samples_split=2, 
            random_state=42
        )
        
        # Fit model (autolog tracks parameters and metrics automatically)
        model.fit(X_train, y_train)
        
        # Evaluate model
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        
        print(f"Model Accuracy on Test Set: {acc:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, preds))
        
        # Log model specifically as sklearn flavor
        mlflow.sklearn.log_model(model, "model_sklearn")
        print("Model and metrics successfully tracked via autolog!")

if __name__ == "__main__":
    train_autolog()
