import requests
import json

# URL of the model serving API (FastAPI)
URL = "http://127.0.0.1:8000/predict"

def send_inference_request():
    # Example input matching the 22 preprocessed features of a single sample
    payload = {
        "age": 0.54,              # Scaled age
        "trestbps": -0.12,         # Scaled resting blood pressure
        "chol": 0.45,             # Scaled cholesterol
        "thalach": -0.56,          # Scaled max heart rate
        "oldpeak": 0.89,           # Scaled ST depression
        "chol_bps_ratio": 0.51,    # Scaled ratio
        "hr_age_ratio": -0.62,     # Scaled ratio
        "sex": 1,                 # Male
        "fbs": 0,                 # Fasting blood sugar < 120
        "exang": 1,                # Exercise induced angina
        "ca": 2,                  # Major vessels colored
        # Encoded Chest Pain (OHE)
        "cp_1": 0,
        "cp_2": 1,                # Non-anginal pain
        "cp_3": 0,
        # Encoded RestECG (OHE)
        "restecg_1": 1,
        "restecg_2": 0,
        # Encoded Slope (OHE)
        "slope_1": 0,
        "slope_2": 1,
        # Encoded Thalassemia (OHE)
        "thal_1": 0,
        "thal_2": 1,              # Reversable defect
        "thal_3": 0,
        # Encoded Age Group (OHE)
        "age_group_1": 1,
        "age_group_2": 0
    }
    
    print(f"Sending inference request to {URL}...")
    print(f"Payload:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(URL, json=payload)
        
        if response.status_code == 200:
            print("\nResponse Received Successfully!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"\nFailed! Status Code: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("\nConnection Error! Please make sure that your serving application (prometheus_exporter.py) is running on port 8000.")
        print("Run command: uvicorn prometheus_exporter:app --reload")

if __name__ == "__main__":
    send_inference_request()
