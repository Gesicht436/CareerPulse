import os
import re
import time
import pandas as pd

RAW_DATA_PATH = os.path.join("core_engine", "datasets", "raw", "job_descriptions.csv")
PROCESSED_DIR = os.path.join("core_engine", "datasets", "processed")
CLEANED_DATA_PATH = os.path.join(PROCESSED_DIR, "cleaned_job_descriptions.csv")

COLUMNS_TO_DROP = [
    "longitude",
    "latitude",
    "Job Posting Date",
    "Company Size",
    "Benefits"
]

def normalize_experience(val) -> int:
    """
    Parses experience range (e.g. '5 to 15 Years'), calculates the average,
    adds 10% of that average, and returns a single integer.
    """
    if isinstance(val, (int, float)):
        return int(round(val * 1.10))
    if not isinstance(val, str) or not val.strip():
        return 0
    
    nums = [float(x) for x in re.findall(r'\d+', val)]
    if not nums:
        return 0
    
    avg = sum(nums) / len(nums)
    final_val = avg * 1.10
    return int(round(final_val))

def preprocess_dataset(chunk_size: int = 100000):
    if not os.path.exists(RAW_DATA_PATH):
        print(f"[ERROR] Raw dataset not found at '{RAW_DATA_PATH}'.")
        return

    print(f"=== Starting Preprocessing on '{RAW_DATA_PATH}' ===")
    print(f"Target Output: '{CLEANED_DATA_PATH}'")
    print(f"Columns to drop: {COLUMNS_TO_DROP}")
    print(f"Formula: round(average(numbers in Experience) * 1.10)\n")

    start_time = time.time()
    total_processed = 0

    # Ensure processed destination directory exists
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # Remove existing cleaned file if present
    if os.path.exists(CLEANED_DATA_PATH):
        os.remove(CLEANED_DATA_PATH)

    first_chunk = True

    for i, chunk in enumerate(pd.read_csv(RAW_DATA_PATH, chunksize=chunk_size)):
        chunk_start = time.time()
        
        # 1. Drop unnecessary columns (ignoring any not present)
        cols_present_to_drop = [c for c in COLUMNS_TO_DROP if c in chunk.columns]
        if cols_present_to_drop:
            chunk = chunk.drop(columns=cols_present_to_drop)

        # 2. Normalize Experience column to single integer
        if "Experience" in chunk.columns:
            chunk["Experience"] = chunk["Experience"].apply(normalize_experience)

        # 3. Stream write to cleaned CSV in processed folder
        chunk.to_csv(
            CLEANED_DATA_PATH,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False
        )

        total_processed += len(chunk)
        first_chunk = False
        chunk_duration = time.time() - chunk_start
        print(f"[Chunk {i+1:02d}] Processed {len(chunk):,} rows ({total_processed:,} total) in {chunk_duration:.2f}s")

    total_duration = time.time() - start_time
    file_size_mb = os.path.getsize(CLEANED_DATA_PATH) / (1024 * 1024)

    print(f"\n=== Preprocessing Completed Successfully! ===")
    print(f"Total Rows: {total_processed:,}")
    print(f"Total Time: {total_duration:.2f}s ({total_duration/60:.2f} minutes)")
    print(f"Cleaned CSV Saved at: '{CLEANED_DATA_PATH}' ({file_size_mb:.2f} MB)")

if __name__ == "__main__":
    preprocess_dataset()
