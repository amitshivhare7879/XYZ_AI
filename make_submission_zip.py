import os
import zipfile
from pathlib import Path

def create_submission_zip(output_filename="XYZ_AI_Submission.zip"):
    root_dir = Path(__file__).parent.resolve()
    zip_path = root_dir / output_filename

    # Exclude unwanted directories and file patterns
    EXCLUDED_DIRS = {
        '.git', '.github', '.pytest_cache', '__pycache__', '.venv', 'venv', 
        'node_modules', '.idea', '.vscode', '.system_generated'
    }
    EXCLUDED_FILES = {
        output_filename, '.DS_Store', 'Thumbs.db', '.coverage'
    }
    EXCLUDED_EXTENSIONS = {
        '.pyc', '.pyo', '.pyd', '.log', '.tmp'
    }

    print(f"Creating clean submission archive: {zip_path.name}...")
    
    file_count = 0
    total_uncompressed_bytes = 0

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(root_dir):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith('.')]

            for file in sorted(files):
                if file in EXCLUDED_FILES or file.startswith('.'):
                    if file not in ['.env.example', '.gitignore']:
                        continue
                
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in EXCLUDED_EXTENSIONS:
                    continue

                abs_file_path = Path(root) / file
                rel_file_path = abs_file_path.relative_to(root_dir)

                # Skip if file is the zip itself
                if abs_file_path.resolve() == zip_path:
                    continue

                zipf.write(abs_file_path, arcname=str(rel_file_path))
                file_count += 1
                total_uncompressed_bytes += abs_file_path.stat().st_size

    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"Successfully created {zip_path.name}!")
    print(f"  Files included: {file_count}")
    print(f"  Uncompressed size: {total_uncompressed_bytes / (1024 * 1024):.2f} MB")
    print(f"  Compressed archive size: {zip_size_mb:.2f} MB")
    print(f"  Archive location: {zip_path}")

if __name__ == '__main__':
    create_submission_zip()
