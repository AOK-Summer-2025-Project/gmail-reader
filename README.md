# gmail-reader
Tool for downloading DRS reports and extracting mp3 metadata

Gmail DRS Report Downloader & MP3 Extractor 
1.  Project Overview 
This tool automates the process of: 

Downloading `.txt` attachment reports from Gmail within a specific date range 
Extracting `.mp3`-related metadata from those reports 
Saving the cleaned metadata into a structured CSV file 
It consists of two Python scripts: 

`gmail_reader.py`: Downloads all `.txt` attachments from emails between two dates 
`extract_mp3s.py`: Extracts `.mp3` metadata and saves it to `drs_master_mp3s.csv` 
Output: A file called `drs_master_mp3s.csv` containing audio file metadata (object IDs, URNs, and file URNs) consolidated from all `.txt` attachments. 

2. Downloading Python 
Check if Python is installed by opening terminal and running python3 --version 

If it's not installed, download it from: https://www.python.org/downloads/ 

 

To install required packages, run the following in Terminal: 

pip3 install --upgrade google-api-python-client google-auth google-auth-oauthlib pandas 

3. Setting up Gmail API Access 
Before running the gmail_reader.py script, you'll need to configure access to the Gmail API through Google Cloud. Follow these steps: 

Step 1: Create a Google Cloud Project 

Go to the Google Cloud Console. 
Click the project dropdown (top bar) → "New Project". 
Name the project (e.g., DRS Gmail Downloader) and click Create. 
Step 2: Enable the Gmail API 

In the Google Cloud Console, go to APIs & Services > Library. 
Search for Gmail API, select it, and click Enable. 
Step 3: Create OAuth Credentials 

Go to APIs & Services > Credentials. 
Click "Create Credentials" → choose "OAuth client ID". 
If prompted, configure the OAuth consent screen (use "External" and basic info). 
Under Application type, choose "Desktop App". 
Name it something like DRS Script Access and click Create. 
Step 4: Download credentials.json 

After creating the OAuth client ID, click Download JSON. 
Save the file to your project directory and rename it to credentials.json. 
 

4. Configuration and Running the Scripts 
Folder Setup 
Your working directory should include: 
project-folder/ 
├── gmail_reader.py        # pulls .txt files from Gmail 
├── extract_mp3s.py        # extracts .mp3 metadata into a CSV 
├── credentials.json       # provided to you (no setup needed) 
 
 

 All other files like `token.json`, `drs_reports/`, and `drs_master_mp3s.csv` will be created automatically after running the scripts. 

Step 1: Set the Date Range and File Paths 
Open `gmail_reader.py` and configure the following: 

 

1. Set your email search window: 

start_date = '2025/07/01' 
end_date = '2025/07/01’ 
Use YYYY/MM/DD format. 
2. Update file paths to match your folder location: 

TOKEN_FILE = '/your/path/to/token.json' 
CREDENTIALS_FILE = '/your/path/to/credentials.json' 
OUTPUT_DIR = '/your/path/to/drs_reports' 
Step 2: Run `gmail_reader.py` 
Navigate to your folder in Terminal and run: 

python3 gmail_reader.py 

A browser window will open the first time for Gmail login. 
The script will download `.txt` attachments from emails in the date range. 
Files will be saved into your `drs_reports/` directory. 
Step 3: Run `extract_mp3s.py` 
Now open `extract_mp3s.py` and update the folder path.: 

DRS_DIR = '/your/path/to/drs_reports' 

Also verify the output CSV path: 

OUTPUT_CSV = '/your/path/to/drs_master_mp3s.csv' 

Then run: 

python3 extract_mp3s.py 

The script scans all `.txt` files in `drs_reports/` 
Extracts `.mp3`-related metadata 
Saves a clean file called `drs_master_mp3s.csv` 
 
