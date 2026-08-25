import os
import sys
import zipfile
import time

DATASETS_DIR = os.path.join("core_engine", "datasets")
PACKAGE_OUTPUT = os.path.join("core_engine", "datasets", "careerpulse_1.6m_dataset_bundle.zip")

FILES_TO_PACK = [
    ("jobs.db", "jobs.db"),
    ("embeddings/dataset_embeddings_full.pt", "embeddings/dataset_embeddings_full.pt"),
    ("embeddings/dataset_meta_full.pt", "embeddings/dataset_meta_full.pt")
]

def package_artifacts():
    print("=======================================================")
    print("   CareerPulse 1.61M Dataset Artifact Packager")
    print("=======================================================\n")

    resolved_files = []
    for rel_path, arc_name in FILES_TO_PACK:
        path = os.path.join(DATASETS_DIR, rel_path)
        # Fallback to root datasets dir if not yet in embeddings folder
        if not os.path.exists(path):
            fallback = os.path.join(DATASETS_DIR, os.path.basename(rel_path))
            if os.path.exists(fallback):
                path = fallback
            else:
                print(f"[ERROR] Required artifact '{rel_path}' not found in '{DATASETS_DIR}'.")
                sys.exit(1)
        size_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"• Found: {arc_name} ({size_mb:.2f} MB)")
        resolved_files.append((path, arc_name))

    print(f"\nCompressing into '{PACKAGE_OUTPUT}' (this may take 1-2 minutes)...")
    start_time = time.time()

    with zipfile.ZipFile(PACKAGE_OUTPUT, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for file_path, arc_name in resolved_files:
            print(f"  Adding {arc_name}...")
            zipf.write(file_path, arcname=arc_name)

    total_time = time.time() - start_time
    zip_size_mb = os.path.getsize(PACKAGE_OUTPUT) / (1024 * 1024)

    print(f"\nSUCCESS: Bundle created successfully!")
    print(f"Archive: {PACKAGE_OUTPUT}")
    print(f"Compressed Size: {zip_size_mb:.2f} MB ({zip_size_mb/1024:.2f} GB)")
    print(f"Packaging Time: {total_time:.2f}s\n")
    print("Next Steps:")
    print("1. Upload this zip file to your preferred cloud host:")
    print("   - Hugging Face Hub (Recommended: Free, unlimited bandwidth)")
    print("   - GitHub Releases (Tag a new release and attach the zip)")
    print("   - Google Drive / AWS S3 / Cloudflare R2")
    print("2. Teammates can run 'uv run python scripts/download_precomputed_data.py' to download and extract in < 60s!")

if __name__ == "__main__":
    package_artifacts()
