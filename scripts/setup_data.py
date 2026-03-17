import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env file automatically
load_dotenv()

# Configuration: (Dataset Ref, Target Path)
DATASETS = [
    ("adityarajsrv/job-descriptions-2025-tech-and-non-tech-roles", "core_engine/data_layer/raw"),
]

def download_data():
    """
    Downloads datasets from Kaggle using the Kaggle API.
    """
    # 1. Check for API Token
    # Kaggle library automatically picks up KAGGLE_API_TOKEN if set
    token = os.getenv("KAGGLE_API_TOKEN")
    if not token:
        print("\n[ERROR] KAGGLE_API_TOKEN not found in environment variables.")
        print("Please check your .env file or set the variable in your shell.\n")
        sys.exit(1)

    # 2. Process each dataset
    for ref, target_dir in DATASETS:
        target_path = Path(target_dir)
        print(f"\n---> Fetching: {ref}")
        print(f"---> Target: {target_path.absolute()}")

        # Ensure directory exists
        target_path.mkdir(parents=True, exist_ok=True)

        try:
            # Run the kaggle download command
            # -d: dataset ref
            # -p: destination path
            # --unzip: extract files
            cmd = ["kaggle", "datasets", "download", "-d", ref, "-p", str(target_path), "--unzip"]
            
            # Using subprocess directly to ensure it runs in the current environment
            subprocess.run(cmd, check=True)
            print(f"DONE: Successfully downloaded and unzipped into {target_dir}\n")

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to download {ref}. Error: {e}\n")
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred: {e}\n")

if __name__ == "__main__":
    download_data()
