import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env file automatically
load_dotenv()

# Configuration: (Dataset Ref, Target Path)
DATASETS = [
    ("ravindrasinghrana/job-description-dataset", "core_engine/datasets/raw"),
]


def setup_kaggle_auth():
    """
    Configures Kaggle credentials from environment variables or .env file.
    Supports KAGGLE_USERNAME + KAGGLE_KEY, KAGGLE_API_TOKEN, or ~/.kaggle/kaggle.json.
    """
    token = os.getenv("KAGGLE_API_TOKEN")
    if token:
        token = token.strip().strip('"').strip("'")
        if ":" in token and not token.startswith("{"):
            parts = token.split(":", 1)
            os.environ["KAGGLE_USERNAME"] = parts[0].strip()
            os.environ["KAGGLE_KEY"] = parts[1].strip()
        elif token.startswith("{"):
            import json
            try:
                data = json.loads(token)
                os.environ["KAGGLE_USERNAME"] = data.get("username", "")
                os.environ["KAGGLE_KEY"] = data.get("key", "")
            except Exception:
                pass

    username = os.getenv("KAGGLE_USERNAME")
    key = os.getenv("KAGGLE_KEY")
    kaggle_json_path = Path.home() / ".kaggle" / "kaggle.json"

    if (not username or not key) and not kaggle_json_path.exists():
        print("\n[ERROR] Kaggle credentials not found!")
        print("Please provide your credentials in .env file using one of the following:")
        print("  Option A:")
        print("    KAGGLE_USERNAME=your_kaggle_username")
        print("    KAGGLE_KEY=your_kaggle_api_key")
        print("  Option B:")
        print("    KAGGLE_API_TOKEN=your_username:your_api_key")
        print("Or place your 'kaggle.json' inside ~/.kaggle/kaggle.json\n")
        sys.exit(1)


def download_data():
    """
    Downloads datasets from Kaggle using the Kaggle API.
    """
    setup_kaggle_auth()

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
