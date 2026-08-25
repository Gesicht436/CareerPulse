import os
import json
import pandas as pd

PROCESSED_PATH = os.path.join("core_engine", "datasets", "processed", "cleaned_job_descriptions.csv")
ROOT_PATH = os.path.join("core_engine", "datasets", "cleaned_job_descriptions.csv")
DATA_PATH = PROCESSED_PATH if os.path.exists(PROCESSED_PATH) else ROOT_PATH

def inspect():
    if not os.path.exists(DATA_PATH):
        print(f"[ERROR] Cleaned dataset not found at {DATA_PATH}")
        return

    print("Loading sample from cleaned dataset...")
    df = pd.read_csv(DATA_PATH, nrows=50000)

    print(f"\n=======================================================")
    print(f"   CareerPulse Processed Dataset Explorer (50k sample)")
    print(f"   Total Columns: {len(df.columns)}")
    print(f"=======================================================\n")
    print(f"Columns: {list(df.columns)}\n")

    while True:
        print("\nChoose an option:")
        print("1. View first 3 records in detail")
        print("2. Search jobs by keyword (e.g. 'Software', 'React', 'Data')")
        print("3. View statistics (Experience & Qualifications distribution)")
        print("4. View random job posting")
        print("5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            for idx in range(min(3, len(df))):
                print(f"\n--- RECORD #{idx+1} ---")
                print(json.dumps(df.iloc[idx].to_dict(), indent=2))

        elif choice == "2":
            query = input("Enter search term: ").strip().lower()
            mask = df['Job Title'].str.lower().str.contains(query, na=False) | \
                   df['Role'].str.lower().str.contains(query, na=False) | \
                   df['skills'].str.lower().str.contains(query, na=False)
            matches = df[mask].head(5)
            print(f"\nFound {len(df[mask]):,} matches in 50k sample. Showing top {len(matches)}:\n")
            for i, (_, row) in enumerate(matches.iterrows()):
                print(f"[{i+1}] {row['Job Title']} | Role: {row['Role']} | Exp: {row['Experience']} yrs | Qual: {row['Qualifications']} | Salary: {row['Salary Range']}")
                print(f"    Company: {row['Company']} ({row['location']}, {row['Country']})")
                print(f"    Skills: {str(row['skills'])[:100]}...\n")

        elif choice == "3":
            print("\n--- QUALIFICATIONS DISTRIBUTION ---")
            print(df['Qualifications'].value_counts().to_string())
            print("\n--- NORMALIZED EXPERIENCE (YEARS) DISTRIBUTION ---")
            print(df['Experience'].value_counts().sort_index().to_string())
            print("\n--- WORK TYPE DISTRIBUTION ---")
            print(df['Work Type'].value_counts().to_string())

        elif choice == "4":
            sample = df.sample(1).iloc[0]
            print("\n--- RANDOM JOB RECORD ---")
            print(json.dumps(sample.to_dict(), indent=2))

        elif choice == "5" or choice == "q":
            print("Exiting explorer.")
            break
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    inspect()
