import os
import pandas as pd
import numpy as np

def generate_heart_disease_dataset():
    # Set seed for reproducibility
    np.random.seed(42)
    n_samples = 300

    # Generate standard Cleveland Heart Disease features
    age = np.random.randint(29, 78, size=n_samples)
    sex = np.random.randint(0, 2, size=n_samples) # 1 = male, 0 = female
    cp = np.random.randint(0, 4, size=n_samples) # Chest pain type: 0, 1, 2, 3
    trestbps = np.random.randint(94, 200, size=n_samples) # Resting blood pressure
    chol = np.random.randint(126, 564, size=n_samples) # Serum cholesterol in mg/dl
    fbs = np.random.randint(0, 2, size=n_samples) # Fasting blood sugar > 120 mg/dl: 1, 0
    restecg = np.random.randint(0, 3, size=n_samples) # Resting ECG: 0, 1, 2
    thalach = np.random.randint(71, 202, size=n_samples) # Max heart rate
    exang = np.random.randint(0, 2, size=n_samples) # Exercise induced angina: 1, 0
    oldpeak = np.round(np.random.uniform(0.0, 6.2, size=n_samples), 1) # ST depression
    slope = np.random.randint(0, 3, size=n_samples) # Slope of peak exercise ST segment
    ca = np.random.randint(0, 5, size=n_samples) # Number of major vessels (0-4)
    thal = np.random.randint(0, 4, size=n_samples) # Thalassemia: 0 = normal; 1 = fixed; 2 = reversable; 3 = unspecified

    df = pd.DataFrame({
        'age': age,
        'sex': sex,
        'cp': cp,
        'trestbps': trestbps,
        'chol': chol,
        'fbs': fbs,
        'restecg': restecg,
        'thalach': thalach,
        'exang': exang,
        'oldpeak': oldpeak,
        'slope': slope,
        'ca': ca,
        'thal': thal
    })

    # Generate correlated target column (1 = heart disease, 0 = normal)
    # Target probability increases with oldpeak, cp, ca, age, and decreases with thalach
    logit = -2.5 + 0.02 * df['age'] + 0.8 * df['cp'] - 0.02 * df['thalach'] + 0.6 * df['oldpeak'] + 0.5 * df['ca'] + 0.7 * df['exang']
    prob = 1 / (1 + np.exp(-logit))
    df['target'] = (prob > np.random.uniform(0, 1, size=n_samples)).astype(int)

    # Introduce some realistic missing values and duplicates to test preprocessors
    # 5 random missing values in 'chol' and 'trestbps'
    for col in ['chol', 'trestbps']:
        missing_indices = np.random.choice(df.index, size=5, replace=False)
        df.loc[missing_indices, col] = np.nan

    # Add 3 duplicate rows
    duplicate_rows = df.iloc[0:3].copy()
    df = pd.concat([df, duplicate_rows], ignore_index=True)

    # Ensure output directory exists
    os.makedirs('dataset', exist_ok=True)
    df.to_csv('dataset/heart_disease.csv', index=False)
    print(f"Generated heart_disease.csv with shape {df.shape} in dataset/")

if __name__ == "__main__":
    generate_heart_disease_dataset()
