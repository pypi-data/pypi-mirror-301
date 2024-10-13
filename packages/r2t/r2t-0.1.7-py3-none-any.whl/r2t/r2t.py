#!/usr/bin/env python


import os
import argparse
from pathlib import Path
import re
import sys
import chardet

# python r2t.py --path "c:\code\gemini-1.5" --ext .py,.txt,.md --out gemcli.txt --respect-git yes

def parse_ignore_pattern(pattern, base_path=''):
    """
    Parse an ignore pattern and return a compiled regex object.
    
    :param pattern: The ignore pattern to parse
    :param base_path: The base path to prepend to the pattern (for .gitignore in subdirectories)
    :return: A tuple (compiled regex object, is_negation)
    """
    is_negation = pattern.startswith('!')
    if is_negation:
        pattern = pattern[1:]

    pattern = pattern.rstrip('/')
    if base_path:
        pattern = os.path.join(base_path, pattern)
    if pattern.startswith('/'):
        pattern = '^' + re.escape(pattern[1:])
    elif '/' in pattern:
        pattern = '^' + re.escape(pattern)
    else:
        pattern = '(^|/)' + re.escape(pattern)
    pattern = pattern.replace('\\*', '.*') + '(/|$)'
    return re.compile(pattern), is_negation


def should_ignore(path, ignore_patterns):
    """
    Check if a path should be ignored based on the ignore patterns.
    
    :param path: The path to check
    :param ignore_patterns: A list of tuples (compiled regex object, is_negation)
    :return: True if the path should be ignored, False otherwise
    """
    path_str = str(path)
    ignore = False
    for pattern, is_negation in ignore_patterns:
        if pattern.search(path_str):
            ignore = not is_negation
    return ignore


def read_ignore_file(filepath, base_path=''):
    """
    Read an ignore file and return a list of tuples (compiled regex object, is_negation).
    
    :param filepath: Path to the ignore file
    :param base_path: Base path for relative patterns
    :return: A list of tuples (compiled regex object, is_negation)
    """
    ignore_patterns = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_patterns.append(
                        parse_ignore_pattern(line, base_path))
    except FileNotFoundError:
        print(f"Warning: Ignore file not found: {filepath}")
    except Exception as e:
        print(f"Error reading ignore file {filepath}: {str(e)}")
    return ignore_patterns


def read_gitignore(path):
    """
    Read all .gitignore files in the directory tree and return a list of compiled regex objects.
    
    :param path: Root path to start searching for .gitignore files
    :return: A list of compiled regex objects
    """
    gitignore_patterns = []
    for root, _, files in os.walk(path):
        if '.gitignore' in files:
            gitignore_path = Path(root) / '.gitignore'
            relative_root = Path(root).relative_to(path)
            base_path = str(relative_root) if str(relative_root) != '.' else ''
            gitignore_patterns.extend(
                read_ignore_file(gitignore_path, base_path))
    return gitignore_patterns


def generate_tree(path, extensions, ignore_patterns, specific_files=None, prefix="", is_root=True):
    tree = []
    try:
        contents = sorted(path.iterdir(), key=lambda x: (
            x.is_file(), x.name.lower()))
    except PermissionError:
        return [f"{prefix}Error: Permission denied"]
    except Exception as e:
        return [f"{prefix}Error: {str(e)}"]

    if is_root:
        tree.append(f"{path.name}/")
        prefix = "    "

    for i, item in enumerate(contents):
        if item.name == '.git':
            continue
        relative_path = item.relative_to(path)
        if ignore_patterns and should_ignore(relative_path, ignore_patterns):
            continue

        is_last = i == len(contents) - 1
        current_prefix = "└── " if is_last else "├── "

        if item.is_dir():
            tree.append(f"{prefix}{current_prefix}{item.name}/")
            subtree = generate_tree(item, extensions, ignore_patterns, specific_files,
                                    prefix + ("    " if is_last else "│   "), is_root=False)
            if subtree:  # Only add non-empty subtrees
                tree.extend(subtree)
        else:
            # Check if the file should be included based on extensions or specific files
            include_file = (extensions and item.suffix.lower() in extensions) or \
                           (specific_files and any(f.resolve() == item.resolve()
                            for f in specific_files))
            if include_file:
                tree.append(f"{prefix}{current_prefix}{item.name}")

    # Add specific files that weren't found in the directory structure
    if is_root and specific_files:
        for file in specific_files:
            if file.is_relative_to(path) and not any(item.endswith(file.name) for item in tree):
                tree.append(f"{prefix}└── {file.relative_to(path)}")

    return tree


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read(4096)  # Read first 4KB of the file
    result = chardet.detect(raw_data)
    return result['encoding']


def combine_files(path, extensions, output_file, ignore_patterns, specific_files=None):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Generate and write the directory tree
        tree = generate_tree(Path(path), extensions,
                             ignore_patterns, specific_files)
        outfile.write("Directory Tree:\n")
        outfile.write("\n".join(tree))
        outfile.write("\n\n" + "="*80 + "\n\n")

        files_processed = set()
        for root, dirs, files in os.walk(path):
            if '.git' in dirs:
                dirs.remove('.git')

            dirs[:] = [d for d in dirs if not should_ignore(
                Path(root).relative_to(path) / d, ignore_patterns)]
            files = [f for f in files if not should_ignore(
                Path(root).relative_to(path) / f, ignore_patterns)]

            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(path)

                # Debug print
                print(f"Checking file: {file_path}")

                should_process = False
                if extensions and file_path.suffix.lower() in extensions:
                    should_process = True
                if specific_files and any(file_path.resolve() == f.resolve() for f in specific_files):
                    should_process = True

                if should_process:
                    # Debug print
                    print(f"Processing file: {file_path}")

                    outfile.write(f"File: {relative_path}\n\n")
                    try:
                        encoding = detect_encoding(file_path)
                        with open(file_path, 'r', encoding=encoding) as infile:
                            content = infile.read()
                            outfile.write(content)
                            if not content.endswith('\n'):
                                outfile.write('\n')  # Ensure there's a newline at the end of each file
                    except UnicodeDecodeError:
                        outfile.write(
                            f"Error: Unable to decode file {relative_path} with detected encoding {encoding}\n")
                    except PermissionError:
                        outfile.write(
                            f"Error: Permission denied when reading file {relative_path}\n")
                    except FileNotFoundError:
                        outfile.write(
                            f"Error: File {relative_path} not found\n")
                    except Exception as e:
                        outfile.write(
                            f"Error reading file {relative_path}: {str(e)}\n")
                    outfile.write("\n" + "="*80 + "\n\n")

                    if specific_files:
                        files_processed.add(str(file_path.resolve()))

        if specific_files:
            missing_files = set(str(f.resolve())
                                for f in specific_files) - files_processed
            if missing_files:
                outfile.write(
                    "The following specified files were not found:\n")
                for file in missing_files:
                    outfile.write(f"- {file}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Combine files with specified extensions into a single file.",
        epilog="""
Examples:
  # Combine all Python files in the current directory
  python r2t.py --path . --ext .py --out combined_python.txt

  # Combine specific files from different subdirectories
  python r2t.py --path . --files src/main.py,docs/README.md,tests/test_main.py --out important_files.txt

  # Combine all .txt and .md files, respecting .gitignore
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--path", required=True, help="Target directory path")
    parser.add_argument(
        "--ext", help="Comma-separated list of file extensions")
    parser.add_argument("--out", required=True, help="Output filename")
    parser.add_argument(
        "--respect-git", choices=['yes', 'no'], default='no', help="Respect .gitignore rules")
    parser.add_argument("--ignore-file", help="Path to additional ignore file")
    parser.add_argument(
        "--files", help="Comma-separated list of specific files to include")

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    path = Path(args.path).resolve()
    if not path.is_dir():
        print(f"Error: The specified path '{path}' is not a valid directory.")
        return

    extensions = [ext.strip().lower()
                  for ext in args.ext.split(',')] if args.ext else []
    output_file = args.out
    respect_git = args.respect_git == 'yes'
    specific_files = [Path(args.path) / Path(f.strip()).relative_to(Path(f.strip()).anchor)
                      for f in args.files.split(',')] if args.files else None

    if not extensions and not specific_files:
        print("Error: You must specify either --ext or --files.")
        return

    ignore_patterns = []
    if respect_git:
        ignore_patterns.extend(read_gitignore(path))
    if args.ignore_file:
        ignore_patterns.extend(read_ignore_file(args.ignore_file))

    try:
        combine_files(path, extensions, output_file,
                      ignore_patterns, specific_files)
        print(f"Files combined successfully. Output: {output_file}")
        if specific_files:
            print(
                "Note: Check the output file for any specified files that were not found.")
    except PermissionError:
        print(f"Error: Permission denied when writing to {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()

