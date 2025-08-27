@echo off
echo ===============================================
echo REMOVING ICONS FROM MOVIE SEARCH ENGINE
echo ===============================================
echo.

cd /d "e:\_SoftEng\_BeCode\database-advanced\elasticsearch_movie_search"

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Removing icons from Python files...
python -c "
import re
import os

# List of files to clean
files_to_clean = [
    'main.py',
    'demo_advanced.py',
    'src/search_interface.py',
    'src/movie_search_engine.py',
    'src/data_indexer.py'
]

# List of icons and symbols to remove  
icons_to_remove = ['🚀', '🔍', '•', '📽️', '📅', '⭐', '🎭', '🎬', '💡', '🔄', '🏆', '📊', '🎯', '📖', '🧪', '🖥️', '🔗', '👋', '✅', '❌', '💰', '📍', '📝', '💾', '📤', '📈']

for file_path in files_to_clean:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove each icon
        for icon in icons_to_remove:
            content = content.replace(icon, '')
        
        # Clean up extra spaces but preserve formatting
        content = re.sub(r'  +', ' ', content)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Icons removed from {file_path}')
        else:
            print(f'No icons found in {file_path}')
    else:
        print(f'File not found: {file_path}')

print('Icon removal complete!')
"

echo.
echo All icons have been removed!
echo You can now run the demo with: run-demo.bat
pause
