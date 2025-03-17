🧩 Code Extractor

A robust, command-line Python tool designed to extract code context from project directories, optimized for preparing context for LLMs or code analysis tasks.

🚀 Features
	•	Automatic project-type detection: intelligently ignores common files (customizable).
	•	Git-aware: captures and includes current Git branch and commit information in your output.
	•	Customizable output: saves files clearly marked with date, git branch, and commit.
	•	Detailed logs and error handling: easily troubleshoot or review extraction history.

📂 Folder Structure

code-extractor/
├── extractor.py          # Main extraction script
├── .extractorignore      # Ignore patterns file
├── logs/                 # Logs storage
├── output/               # Extracted context output files
├── requirements.txt      # Required Python libraries
└── README.md             # Documentation (this file)

🔧 Installation & Setup

1. Clone or Download this repo

git clone <your_repo_url>
cd code-extractor

2. Install Dependencies

pip install -r requirements.txt

🖥 Usage

Run via terminal:

python3 extractor.py

	•	Enter the path to your project.
	•	Choose or confirm the output filename (auto-generated suggestion provided).

⚙️ Customization

To customize files or patterns to ignore, edit .extractorignore:

node_modules
*.log
__pycache__
venv
env
dist

📌 How Git Integration Works

The script automatically detects Git information (branch and commit) from your project folder, adding it into your output file and filename for version control clarity.

🚨 Logs & Error Handling

All actions, warnings, and errors are logged in:

logs/extractor.log

🎯 Make It Executable from Terminal (Recommended)

Make executable (Unix/macOS):

chmod +x ~/tools/code-extractor/extractor.py

Create Terminal Shortcut:

Open your terminal, run:

echo 'alias codextract="~/tools/code-extractor/extractor.py"' >> ~/.bashrc
source ~/.bashrc

Now you can easily run from anywhere:

codextract

🚀 Example Run:

codextract
📂 Enter project folder path: ~/projects/my-react-app
💾 Enter output filename [my-react-app_main_d9f8b1c_20250317_110030.md]:
Extracting files: 100%|██████████████████████| 87/87 [00:01<00:00, 56.23it/s]
✅ Extraction complete. File saved at output/my-react-app_main_d9f8b1c_20250317_110030.md
