import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data(filepath="dataset_raw/heart_disease.csv"):
    """Loads the raw dataset."""
    print(f"Loading data from {filepath}...")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Source file {filepath} not found.")
    df = pd.read_csv(filepath)
    return df

def clean_data(df):
    """Handles missing values and duplicates."""
    print("Cleaning data...")
    # 1. Handle duplicate values
    duplicates_count = df.duplicated().sum()
    if duplicates_count > 0:
        df = df.drop_duplicates().reset_index(drop=True)
        print(f"Removed {duplicates_count} duplicate rows.")

    # 2. Handle missing values
    # Fill numeric column missing values with median
    numeric_cols_with_nan = [col for col in df.columns if df[col].isnull().any()]
    for col in numeric_cols_with_nan:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"Filled missing values in '{col}' with median: {median_val}")

    return df

def feature_engineering(df):
    """Performs feature engineering to create new features."""
    print("Performing feature engineering...")
    # Copy dataframe to avoid SettingWithCopyWarning
    df_feat = df.copy()

    # 1. Risk Ratio: cholesterol / resting blood pressure
    df_feat['chol_bps_ratio'] = df_feat['chol'] / (df_feat['trestbps'] + 1e-5)

    # 2. Age group categorical feature (discretization)
    # 0: Young (<45), 1: Middle-aged (45-60), 2: Elderly (>60)
    df_feat['age_group'] = pd.cut(df_feat['age'], bins=[0, 45, 60, np.inf], labels=[0, 1, 2]).astype(int)

    # 3. Heart rate / age ratio
    df_feat['hr_age_ratio'] = df_feat['thalach'] / (df_feat['age'] + 1e-5)

    return df_feat

def preprocess(df, target_col='target'):
    """Performs scaling, encoding categorical variables, and train-test split."""
    print("Preprocessing features (encoding, scaling, and train-test split)...")
    
    # Separate features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Identify categorical and numeric features
    categorical_cols = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal', 'age_group']
    numeric_cols = [col for col in X.columns if col not in categorical_cols]

    # Apply One-Hot Encoding to multi-category features
    # (cp, restecg, slope, thal, age_group have multiple values)
    multi_cat_cols = ['cp', 'restecg', 'slope', 'thal', 'age_group']
    X_encoded = pd.get_dummies(X, columns=multi_cat_cols, drop_first=True)

    # Convert all dummy boolean columns to int
    dummy_cols = [col for col in X_encoded.columns if any(mc in col for mc in multi_cat_cols)]
    X_encoded[dummy_cols] = X_encoded[dummy_cols].astype(int)

    # Train-Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )

    # Apply scaling on numeric features
    scaler = StandardScaler()
    
    # Scale train set
    X_train_scaled = X_train.copy()
    X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    
    # Scale test set using train scaler parameters
    X_test_scaled = X_test.copy()
    X_test_scaled[numeric_cols] = scaler.transform(X_test[numeric_cols])

    # Recombine features and targets for saved datasets
    train_preprocessed = X_train_scaled.copy()
    train_preprocessed[target_col] = y_train

    test_preprocessed = X_test_scaled.copy()
    test_preprocessed[target_col] = y_test

    return train_preprocessed, test_preprocessed

def save_dataset(train_df, test_df, output_dir="dataset_preprocessed"):
    """Saves the preprocessed datasets to the target folder."""
    # Write to the requested folder
    for folder in [output_dir, output_dir.replace("dataset_preprocessed", "dataset_preprocessing")]:
        print(f"Saving preprocessed datasets to '{folder}'...")
        os.makedirs(folder, exist_ok=True)
        
        train_path = os.path.join(folder, "train.csv")
        test_path = os.path.join(folder, "test.csv")
        
        train_df.to_csv(train_path, index=False)
        test_df.to_csv(test_path, index=False)
        
        print(f"Preprocessed train set saved to {train_path} with shape {train_df.shape}")
        print(f"Preprocessed test set saved to {test_path} with shape {test_df.shape}")

def main():
    """Main execution function."""
    raw_path = "Eksperimen_SML_Kevin_Adiputra/dataset_raw/heart_disease.csv"
    out_dir = "Eksperimen_SML_Kevin_Adiputra/preprocessing/dataset_preprocessed"
    
    # Path fallbacks to handle running from root vs inside preprocessing/ folder
    if not os.path.exists("Eksperimen_SML_Kevin_Adiputra/dataset_raw") and os.path.exists("../dataset_raw"):
        raw_path = "../dataset_raw/heart_disease.csv"
        out_dir = "dataset_preprocessed"
        
    df = load_data(raw_path)
    df_clean = clean_data(df)
    df_feat = feature_engineering(df_clean)
    train_preprocessed, test_preprocessed = preprocess(df_feat, target_col='target')
    save_dataset(train_preprocessed, test_preprocessed, out_dir)
    print("Preprocessing completed successfully!")

if __name__ == "__main__":
    main()
