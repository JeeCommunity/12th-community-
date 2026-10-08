import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find all ui-avatars.com URLs and update them
    # For example: `https://ui-avatars.com/api/?name=${currentUserProfile.name}`
    # We want: `https://ui-avatars.com/api/?name=${encodeURIComponent(currentUserProfile.name || 'User')}&background=0D8ABC&color=fff`
    
    # It's easier to just replace the whole template string if we can match it.
    
    content = re.sub(
        r"`https://ui-avatars\.com/api/\?name=\$\{([^}]+)\}(?:&background=random)?`",
        r"`https://ui-avatars.com/api/?name=${encodeURIComponent(\1 || 'User')}&background=0D8ABC&color=fff`",
        content
    )
    
    with open(filepath, 'w') as f:
        f.write(content)

for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            process_file(os.path.join(root, file))
