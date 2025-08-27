#!/usr/bin/env python3
"""
Fix indentation destroyed by icon removal script
"""

import os
import re

def fix_python_indentation(file_path):
    """Fix Python indentation by re-adding proper spacing"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    current_indent = 0
    in_class = False
    in_function = False
    in_docstring = False
    
    for i, line in enumerate(lines):
        original_line = line
        line = line.rstrip()
        
        # Skip empty lines
        if not line.strip():
            fixed_lines.append(original_line)
            continue
            
        # Check for docstring markers
        if '"""' in line:
            if line.count('"""') == 2:
                # Single line docstring
                pass
            else:
                in_docstring = not in_docstring
        
        # Don't process lines inside docstrings
        if in_docstring and '"""' not in line:
            fixed_lines.append(original_line)
            continue
            
        # Check for class definitions
        if line.strip().startswith('class ') and line.strip().endswith(':'):
            current_indent = 0
            in_class = True
            in_function = False
            fixed_lines.append(line + '\n')
            continue
            
        # Check for function/method definitions
        if line.strip().startswith('def ') and line.strip().endswith(':'):
            if in_class:
                current_indent = 4  # Method in class
                in_function = True
            else:
                current_indent = 0  # Top-level function
                in_function = True
            fixed_lines.append(' ' * current_indent + line.strip() + '\n')
            continue
            
        # Check for control structures
        if re.match(r'^\s*(if|elif|else|for|while|try|except|finally|with).*:', line.strip()):
            if in_function:
                indent = 8 if in_class else 4
            elif in_class:
                indent = 4
            else:
                indent = 0
            fixed_lines.append(' ' * indent + line.strip() + '\n')
            continue
            
        # Regular content lines
        if line.strip():
            if in_function:
                # Content inside function
                if in_class:
                    indent = 8  # Method content
                else:
                    indent = 4  # Function content
            elif in_class:
                # Content inside class but not in method
                if line.strip().startswith('"""'):
                    indent = 4  # Class docstring
                else:
                    indent = 4  # Class attributes
            else:
                # Top-level content
                indent = 0
                
            fixed_lines.append(' ' * indent + line.strip() + '\n')
        else:
            fixed_lines.append(original_line)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print(f"Fixed indentation in {file_path}")

def main():
    """Fix all Python files in the workspace"""
    
    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"Found {len(python_files)} Python files to fix:")
    for file in python_files:
        print(f"  {file}")
    
    # Fix each file
    for file_path in python_files:
        try:
            fix_python_indentation(file_path)
        except Exception as e:
            print(f"Error fixing {file_path}: {e}")

if __name__ == '__main__':
    main()
