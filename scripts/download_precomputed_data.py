import os
import sys
import zipfile
import urllib.request
import time

DATASETS_DIR = os.path.join("core_engine", "datasets")
ZIP_DEST = os.path.join(DATASETS_DIR, "careerpulse_1.6m_dataset_bundle.zip")

# Default public download URL (can be customized with your Hugging Face or GitHub Release URL)
DEFAULT_URL = os.getenv(
    "CAREERPULSE_DATASET_URL", 
    "https://huggingface.co/datasets/CareerPulse/careerpulse-1.6m-embeddings/resolve/main/careerpulse_1.6m_dataset_bundle.zip"
)

def download_progress_hook(block_num, block_size, total_size):
    downloaded = block_num * block_size
    if total_size > 0:
        percent = min(100, (downloaded / total_size) * 100)
        mb_down = downloaded / (1024 * 1024)
        mb_total = total_size / (1024 * 1024)
        sys.stdout.write(f"\rDownloading: {percent:.1f}% ({mb_down:.1f} MB / {mb_total:.1f} MB)")
        sys.stdout.flush()

def download_and_extract(url: str = DEFAULT_URL):
    print("=======================================================")
    print("   CareerPulse 1.61M Precomputed Dataset Downloader")
    print("=======================================================\n")

    os.makedirs(DATASETS_DIR, exist_ok=True)
    os.makedirs(os.path.join(DATASETS_DIR, "embeddings", "cache_checkpoints"), exist_ok=True)

    # Check if already installed
    full_pt = os.path.join(DATASETS_DIR, "embeddings", "dataset_embeddings_full.pt")
    fallback_pt = os.path.join(DATASETS_DIR, "dataset_embeddings_full.pt")
    jobs_db = os.path.join(DATASETS_DIR, "jobs.db")
    if (os.path.exists(full_pt) or os.path.exists(fallback_pt)) and os.path.exists(jobs_db):
        print(f"Dataset already present at '{DATASETS_DIR}'. Ready to run!")
        return

    print(f"Source URL: {url}")
    print(f"Target Directory: {os.path.abspath(DATASETS_DIR)}\n")

    try:
        start_time = time.time()
        print("Starting download...")
        urllib.request.urlretrieve(url, ZIP_DEST, reporthook=download_progress_hook)
        print("\nDownload complete! Extracting pre-computed artifacts...")

        with zipfile.ZipFile(ZIP_DEST, 'r') as zip_ref:
            zip_ref.extractall(DATASETS_DIR)

        # Cleanup zip file
        if os.path.exists(ZIP_DEST):
            os.remove(ZIP_DEST)

        dur = time.time() - start_time
        print(f"\nSUCCESS: 1.61M Dataset & Vector Embeddings ready in {dur:.2f}s!")
        print("Your CareerPulse instance is now fully configured for instant 1.61M semantic search.\n")

    except Exception as e:
        print(f"\n[ERROR] Failed to download dataset bundle: {e}")
        print("Please check your internet connection or provide a custom URL via CAREERPULSE_DATASET_URL environment variable.")

if __name__ == "__main__":
    custom_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    download_and_extract(custom_url)
