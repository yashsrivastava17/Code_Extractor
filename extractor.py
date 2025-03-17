#!/usr/bin/env python3
import os
from fnmatch import fnmatch
from tqdm import tqdm
import subprocess, logging, datetime

logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'extractor.log'),
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s'
)

IGNORE_PATTERNS = {
    'frontend-react': ['node_modules', 'build', 'dist', 'package-lock.json', '*.log', '*.env'],
    'frontend-angular': ['node_modules', 'dist', '*.log'],
    'frontend-vue': ['node_modules', 'dist', '*.log'],
    'backend-node': ['node_modules', '*.log', 'dist', 'coverage', '*.env'],
    'backend-python': ['venv', '__pycache__', '*.pyc', '*.log', '*.env'],
    'general': ['.git', '*.log', '__pycache__', 'env', 'venv', '.DS_Store']
}

def setup_dirs():
    # Get the script's directory dynamically
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ensure logs and output directories exist inside the script's directory
    logs_dir = os.path.join(script_dir, "logs")
    output_dir = os.path.join(script_dir, "output")

    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

def matches_ignore(file, ignore_list):
    return any(fnmatch(file, pattern) for pattern in ignore_list)

def detect_project_type(folder):
    if os.path.exists(os.path.join(folder, 'package.json')):
        with open(os.path.join(folder, 'package.json'), 'r') as f:
            package = f.read()
            if 'react' in package:
                return 'frontend-react'
            elif '@angular' in package:
                return 'frontend-angular'
            return 'general'
    elif any(f.endswith('.py') for f in os.listdir(folder)):
        return 'backend-python'
    return 'general'

def generate_file_list(root, ignore_patterns):
    file_list = []
    for path, dirs, files in os.walk(root):
        # Filter out directories we want to ignore
        dirs[:] = [d for d in dirs if not matches_ignore(d, ignore_patterns)]
        for file in files:
            rel_path = os.path.relpath(os.path.join(path, file), root)
            if not matches_ignore(rel_path, ignore_patterns):
                file_list.append(rel_path)
    return sorted(file_list)

def detect_git_info(root):
    try:
        branch = subprocess.check_output(['git', '-C', root, 'branch', '--show-current'], stderr=subprocess.DEVNULL).decode().strip()
        commit = subprocess.check_output(['git', '-C', root, 'rev-parse', '--short', 'HEAD'], stderr=subprocess.DEVNULL).decode().strip()
        return branch, commit
    except subprocess.CalledProcessError:
        return None, None

def extract_code(root, files, output_filename):
    output_paths = [
        os.path.join(root, output_filename),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', output_filename)
    ]
    for output_path in output_paths:
        with open(output_path, 'w', encoding='utf-8') as out_file:
            branch, commit = detect_git_info(root)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            out_file.write(f"# Code Extractor Output\nTimestamp: {timestamp}\n")
            if branch and commit:
                out_file.write(f"Git branch: {branch}\nGit commit: {commit}\n")

            out_file.write("\n## Files included:\n\n")
            out_file.writelines([f"- {file}\n" for file in files])
            out_file.write("\n---\n\n")
            
            for file in tqdm(files, desc="Extracting files"):
                out_file.write(f"### {file}\n\n```{os.path.splitext(file)[1][1:]}\n")
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        out_file.write(f.read())
                except Exception as e:
                    logging.error(f"Error reading {file}: {e}")
                    out_file.write(f"\n[Error reading file: {e}]")
                out_file.write("\n```\n\n")
                logging.info(f"Processed file: {file}")

def main():
    setup_dirs()
    folder = input("📂 Enter project folder path: ").strip()
    if not os.path.isdir(folder):
        logging.error("Invalid folder path entered.")
        print("❌ Invalid folder path.")
        return

    print("\n✨ Choose Mode:")
    print("1. Get all files")
    print("2. Select files manually")
    print("3. Intelligent Auto-Analysis")

    choice = input("Enter mode (1/2/3): ").strip()

    if choice == '1':
        files = generate_file_list(folder, [])
    elif choice == '2':
        files = generate_file_list(folder, [])
        selected = [file for file in files if input(f"Include {file}? (y/n): ").lower() == 'y']
        files = selected
    elif choice == '3':
        project_type = detect_project_type(folder)
        print(f"Detected project type: {project_type}")
        ignore = IGNORE_PATTERNS.get(project_type, IGNORE_PATTERNS['general'])
        files = generate_file_list(folder, ignore)
    else:
        print("Invalid choice.")
        return

    branch, commit = detect_git_info(folder)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    git_info_str = f"{branch}_{commit}" if branch and commit else "no_git"
    default_name = f"{os.path.basename(folder)}_{git_info_str}_{timestamp}.md"

    output_filename = input(f"💾 Enter output filename [{default_name}]: ").strip()
    if not output_filename:
        output_filename = default_name

    extract_code(folder, files, output_filename)
    print(f"✅ Extraction complete. File saved at output/{output_filename}")

if __name__ == '__main__':
    main()
