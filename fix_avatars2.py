import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Add length=1
    content = content.replace(
        "&background=0D8ABC&color=fff`",
        "&background=0D8ABC&color=fff&length=1`"
    )
    
    with open(filepath, 'w') as f:
        f.write(content)

for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            process_file(os.path.join(root, file))
