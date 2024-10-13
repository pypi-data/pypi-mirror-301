# r2t (Recursive File Combiner)

## Overview

**r2t** (Recursive to Text) is a powerful Python tool designed to combine multiple files from a directory and its subdirectories into a single output file. It offers flexibility in file selection, respects `.gitignore` rules, and provides a clear visualization of the included files. Whether you're consolidating code for review, preparing documentation, or creating backups, r2t streamlines the process with its robust features and user-friendly interface.

## Features

- **Recursive File Scanning:** Searches through all subdirectories from a given path.
- **Flexible File Selection:** 
  - Combine files based on extensions (e.g., `.py`, `.md`, `.txt`).
  - Specify individual files from different subdirectories.
- **Gitignore Compliance:** Option to respect `.gitignore` rules, excluding files and directories as specified.
- **Custom Ignore Files:** Support for additional ignore files to further customize exclusions.
- **Automatic Encoding Detection:** Uses `chardet` to automatically detect and handle various file encodings.
- **Comprehensive Error Handling:** Gracefully manages permission issues, missing files, and encoding errors.
- **Directory Tree Visualization:** Generates a clear tree structure of included files and directories in the output.
- **Detailed Output:** 
  - Combines file contents with clear separators and file path information.
  - Lists any specified files that were not found.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/r2t.git
   cd r2t
   ```

2. **Create a Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the `r2t.py` script with the desired arguments to combine files.

### Command-Line Arguments

- `--path`: **(Required)** Target directory path to scan for files.
- `--ext`: **(Optional)** Comma-separated list of file extensions to include (e.g., `.py,.md,.txt`).
- `--out`: **(Required)** Output filename where the combined content will be saved.
- `--respect-git`: **(Optional)** Choose `yes` or `no` to respect `.gitignore` rules. Default is `no`.
- `--ignore-file`: **(Optional)** Path to an additional ignore file.
- `--files`: **(Optional)** Comma-separated list of specific files to include.

### Examples

1. **Combine All Python Files in the Current Directory:**
   ```bash
   python r2t.py --path . --ext .py --out combined_python.txt
   ```

2. **Combine Specific Files from Different Subdirectories:**
   ```bash
   python r2t.py --path . --files src/main.py,docs/README.md,tests/test_main.py --out important_files.txt
   ```

3. **Combine All `.txt` and `.md` Files, Respecting `.gitignore`:**
   ```bash
   python r2t.py --path . --ext .txt,.md --out combined_text.md --respect-git yes
   ```

4. **Use an Additional Ignore File:**
   ```bash
   python r2t.py --path . --ext .py --out combined_python.txt --ignore-file custom_ignore.txt
   ```

## Output Structure

The output file contains:

1. **Directory Tree:** A visual representation of the included directories and files.
2. **Combined File Contents:** The content of each included file, clearly separated and labeled with its path.
3. **Summary of Missing Files:** If specific files were requested but not found, they are listed at the end.

## Error Handling

r2t handles various scenarios gracefully:

- **Permission Denied:** Skips files or directories without necessary permissions and logs a warning.
- **File Not Found:** Notifies if a specified file does not exist.
- **Encoding Errors:** Reports if a file's encoding cannot be detected or read.
- **Invalid Directory:** Checks if the specified path is a valid directory.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the Repository
2. Create a Feature Branch: `git checkout -b feature/YourFeature`
3. Commit Your Changes: `git commit -m 'Add some feature'`
4. Push to the Branch: `git push origin feature/YourFeature`
5. Open a Pull Request

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- Uses the [chardet](https://pypi.org/project/chardet/) library for robust encoding detection.
- Inspired by the need for efficient file consolidation in software development and documentation processes.
