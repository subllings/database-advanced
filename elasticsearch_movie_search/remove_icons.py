#!/usr/bin/env python3
import re

# Read the file
with open('src/search_interface.py', 'r', encoding='utf-8') as f:
    content = f.read()

# List of icons to remove
icons = ['📽️', '📅', '⭐', '🎭', '🎬', '🔍', '💡', '🔄', '🏆', '📊', '🚀', '🎯', '📖', '🧪', '🖥️', '🔗', '👋', '✅', '❌', '💰', '📍', '📝', '💾', '📤', '📈']

# Remove each icon
for icon in icons:
    content = content.replace(icon, '')

# Clean up extra spaces
content = re.sub(r' +', ' ', content)

# Write back
with open('src/search_interface.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("All icons removed from search_interface.py")
