import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # If it's a tsx file, we might need to add the import if it has an image
    if 'ui-avatars.com' not in content:
        return

    # Add import
    import_statement = "import { getAvatarUrl } from '../utils';\n"
    if filepath == 'src/components/ProfileSetup.tsx' or filepath == 'src/components/CommunityFeed.tsx' or filepath == 'src/components/Comments.tsx' or filepath == 'src/components/PostCard.tsx' or filepath == 'src/components/CreatePost.tsx' or filepath == 'src/components/LiveStudyRoom.tsx' or filepath == 'src/components/AdminPanel.tsx':
        if "import { getAvatarUrl }" not in content:
            # Insert after other imports
            content = content.replace("import React", "import { getAvatarUrl } from '../utils';\nimport React")
            if "import { getAvatarUrl }" not in content:
                content = "import { getAvatarUrl } from '../utils';\n" + content
    
    # We need to replace the src={...} logic
    # src/components/CommunityFeed.tsx: src={currentUserProfile.photoURL || `https://ui-avatars.com...`}
    # Let's just use regex to replace src={...} where it matches our pattern.
    
    # 1. ProfileSetup.tsx
    content = re.sub(
        r"src=\{photoURL \|\| `https://ui-avatars\.com/api/\?name=\$\{encodeURIComponent\([^}]+\)\}&background=0D8ABC&color=fff&length=1`\}",
        r"src={getAvatarUrl(photoURL, name)}",
        content
    )
    
    # 2. CommunityFeed.tsx
    content = re.sub(
        r"src=\{currentUserProfile\.photoURL \|\| `https://ui-avatars\.com/api/\?name=\$\{encodeURIComponent\([^}]+\)\}&background=0D8ABC&color=fff&length=1`\}",
        r"src={getAvatarUrl(currentUserProfile.photoURL, currentUserProfile.name)}",
        content
    )
    
    # 3. LiveStudyRoom.tsx (2 places)
    content = re.sub(
        r"src=\{student\.userPhotoURL \|\| `https://ui-avatars\.com/api/\?name=\$\{encodeURIComponent\([^}]+\)\}&background=0D8ABC&color=fff&length=1`\}",
        r"src={getAvatarUrl(student.userPhotoURL, student.userName)}",
        content
    )
    content = re.sub(
        r"src=\{p\.userPhotoURL \|\| `https://ui-avatars\.com/api/\?name=\$\{encodeURIComponent\([^}]+\)\}&background=0D8ABC&color=fff&length=1`\}",
        r"src={getAvatarUrl(p.userPhotoURL, p.userName)}",
        content
    )
    
    # 4. Comments.tsx
    content = re.sub(
        r"src=\{photoURL \|\| `https://ui-avatars\.com/api/\?name=\$\{encodeURIComponent\([^}]+\)\}&background=0D8ABC&color=fff&length=1`\}",
        r"src={getAvatarUrl(photoURL, authorName)}",
        content
    )
    
    # 5. PostCard.tsx
    content = re.sub(
        r"src=\{photoURL \|\| `https://ui-avatars\.com/api/\?name=\$\{encodeURIComponent\([^}]+\)\}&background=0D8ABC&color=fff&length=1`\}",
        r"src={getAvatarUrl(photoURL, authorName)}",
        content
    )
    
    # 6. CreatePost.tsx
    content = re.sub(
        r"src=\{currentUser\.photoURL \|\| `https://ui-avatars\.com/api/\?name=\$\{encodeURIComponent\([^}]+\)\}&background=0D8ABC&color=fff&length=1`\}",
        r"src={getAvatarUrl(currentUser.photoURL, currentUser.name)}",
        content
    )
    
    # 7. AdminPanel.tsx
    content = re.sub(
        r"src=\{user\.photoURL \|\| `https://ui-avatars\.com/api/\?name=\$\{encodeURIComponent\([^}]+\)\}&background=0D8ABC&color=fff&length=1`\}",
        r"src={getAvatarUrl(user.photoURL, user.name)}",
        content
    )
    
    with open(filepath, 'w') as f:
        f.write(content)

for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            process_file(os.path.join(root, file))
