import pandas as pd
from pathlib import Path

INPUT_FOLDER = Path(r"C:\Users\matth\edf\csv_automation\csv_inputs") # folder with input CSVs
OUTPUT_FOLDER = Path(r"C:\Users\matth\edf\csv_automation\clean_data_output")  # folder to save output
OUTPUT_FILE = OUTPUT_FOLDER / "clean_data_output.csv"  # full path to output CSV

df_list = []

# Loop through all files in the folder
for f in INPUT_FOLDER.iterdir():

    df = pd.read_csv(f, sep=None, engine="python", header=0, encoding="utf-8-sig")

    # Standardise column headers
    df.columns = df.columns.str.strip().str.lower()

    # Proper case names
    if "first name" in df.columns:
        df["first name"] = df["first name"].str.strip().str.title()
    if "last name" in df.columns:
        df["last name"] = df["last name"].str.strip().str.title()
    
    # Ensures all emails have no blank space
    if "email" in df.columns:
        df["email"] = df["email"].str.strip().str.lower()

    df_list.append(df)

if df_list:

    # Merges all CSV files
    merged_df = pd.concat(df_list, ignore_index=True)
    
    # Deduplicates the merged file by email
    if "email" in merged_df.columns:
        merged_df = merged_df.drop_duplicates(subset="email")
    
    merged_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Merged and cleaned CSV saved in: {OUTPUT_FILE}")
else:
    print("No CSV files found in the folder.")