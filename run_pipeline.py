import os
import sys
import shutil
import subprocess

def run_step(cmd, description):
    print(f"\n=== Running: {description} ===")
    print(f"Command: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Error occurred during step: {description}")
        return False
    print("Success!")
    return True

def main():
    # Get current Python interpreter path
    python_exe = sys.executable
    print(f"Using Python interpreter: {python_exe}")

    # Step 1: Generate Raw Data
    if not run_step(f'"{python_exe}" generate_data.py', "Generate Raw Dataset"):
        return
        
    # Step 2: Run Preprocessing
    if not run_step(f'"{python_exe}" automate_HeartDisease.py', "Run Preprocessing Script"):
        return
        
    # Step 3: Copy preprocessed data to Workflow-CI
    print("\n=== Copying Preprocessed Data to Workflow-CI ===")
    src_path = os.path.join("dataset_preprocessed", "train.csv")
    dest_dir = os.path.join("Workflow-CI", "dataset")
    dest_path = os.path.join(dest_dir, "heart_disease_preprocessed.csv")
    
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copy(src_path, dest_path)
    print(f"Copied {src_path} to {dest_path}")
    print("\nAll pipeline prep steps completed successfully!")

if __name__ == "__main__":
    main()
