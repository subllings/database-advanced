#!/usr/bin/env python3
"""
Comprehensive icon removal script for all Python files in the project.
This script removes ALL emoji icons and replaces them with clean text.
"""

import re
import os
import glob

def remove_icons_from_file(file_path):
"""Remove all emoji icons from a file."""
try:
with open(file_path, 'r', encoding='utf-8') as f:
content = f.read()

original_content = content

# Dictionary of icon replacements
replacements = {
'': '',
'': '',
'Description:': 'Description:',
'Tip:': 'Tip:',
'': '',
'': '',
'': '',
'': '',
'': '',
'': '',
'': '',
'': '',
'': '',
'SUCCESS:': 'SUCCESS:',
'ERROR:': 'ERROR:',
'Box Office:': 'Box Office:',
'': '',
'Year:': 'Year:',
'Rating:': 'Rating:',
'Genres:': 'Genres:',
'Title:': 'Title:',
'MOVIE DETAILS': 'MOVIE DETAILS',
'': '',
'': '',
'': '',
'-': '-',
'Duration:': 'Duration:'
}

# Apply replacements
for icon, replacement in replacements.items():
if replacement:
content = content.replace(f'{icon} ', f'{replacement} ')
content = content.replace(icon, replacement)
else:
content = content.replace(f'{icon} ', '')
content = content.replace(icon, '')

# Clean up extra spaces
content = re.sub(r' +', ' ', content)
content = re.sub(r'^ +', '', content, flags=re.MULTILINE)

# Only write if changes were made
if content != original_content:
with open(file_path, 'w', encoding='utf-8') as f:
f.write(content)
print(f'✓ Cleaned icons from: {file_path}')
return True
else:
print(f'- No icons found in: {file_path}')
return False

except Exception as e:
print(f'✗ Error processing {file_path}: {e}')
return False

def main():
"""Main function to clean all Python files."""
print("ELASTICSEARCH MOVIE SEARCH - ICON REMOVAL")
print("=" * 50)

# Find all Python files in the project
python_files = []

# Add main directory files
python_files.extend(glob.glob('*.py'))

# Add src directory files
python_files.extend(glob.glob('src/*.py'))

cleaned_count = 0
total_count = len(python_files)

print(f"Found {total_count} Python files to process...")
print()

for file_path in python_files:
if remove_icons_from_file(file_path):
cleaned_count += 1

print()
print("=" * 50)
print(f"COMPLETED: {cleaned_count}/{total_count} files cleaned")
print("All emoji icons have been removed!")
print("=" * 50)

if __name__ == "__main__":
main()
