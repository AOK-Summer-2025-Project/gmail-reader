"""
🎵 DRS MP3 Extractor

This script scans through a folder of DRS load report `.txt` files, extracts metadata 
about MP3 files, and compiles the results into a single summary CSV.

🔧 REQUIRED FILES:
- DRS load report `.txt` files exported from Gmail

📦 REQUIRED PYTHON LIBRARIES:
- pandas

📥 TO INSTALL REQUIRED LIBRARY:
    pip install pandas

📝 USER SETUP INSTRUCTIONS:
1. Replace `DRS_DIR` with the path to the folder containing your `.txt` load reports.
2. Replace `OUTPUT_CSV` with the desired output file path for the final summary.
3. Run the script to extract and save all MP3 metadata in one clean CSV.
"""

import os
import pandas as pd

# === USER CONFIGURATION ===
DRS_DIR = '/your/path/to/drs_reports'                   # Folder containing downloaded DRS .txt reports
OUTPUT_CSV = '/your/path/to/output/drs_master_mp3s.csv' # Final combined CSV output file

# === Prepare container to hold MP3 metadata across all files ===
mp3_rows = []

# === Loop through all .txt files in the input directory ===
for filename in os.listdir(DRS_DIR):
    if filename.endswith('.txt'):
        full_path = os.path.join(DRS_DIR, filename)
        try:
            # Attempt to read each file as a tab-separated dataframe
            df = pd.read_csv(full_path, sep='\t', dtype=str)
        except Exception as e:
            print(f"⚠️ Skipping {filename} due to error: {e}")
            continue

        # Strip whitespace from column names to ensure consistency
        df.columns = [col.strip() for col in df.columns]

        # === Identify MP3 rows ===
        # Keep rows where either FILE-ORIGPATH or FILE-FORMAT indicates ".mp3"
        mask = df['FILE-ORIGPATH'].str.contains('.mp3', case=False, na=False) | \
               df['FILE-FORMAT'].str.contains('mp3', case=False, na=False)
        mp3_only = df[mask]

        # === Select and group relevant metadata ===
        # Ensure needed columns are present before grouping
        needed_columns = ['OBJ-ID', 'OBJ-URN', 'OBJ-OSN', 'FILE-URN']
        if not mp3_only.empty:
            mp3_only = mp3_only[needed_columns]

            # Group by object identifiers and collect FILE-URNs into a list
            grouped = mp3_only.groupby(['OBJ-ID', 'OBJ-URN', 'OBJ-OSN'])['FILE-URN'] \
                              .apply(list).reset_index()

            # Convert list of FILE-URNs into a single comma-separated string
            grouped['FILE-URNs'] = grouped['FILE-URN'].apply(lambda x: ', '.join(x))
            grouped = grouped.drop(columns='FILE-URN')

            # Append grouped results for this file to master list
            mp3_rows.append(grouped)

# === Combine all collected MP3 records into one DataFrame and export ===
if mp3_rows:
    final_df = pd.concat(mp3_rows, ignore_index=True)
    final_df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Done! MP3 data written to {OUTPUT_CSV}")
else:
    print("⚠️ No MP3 rows found in any files.")
