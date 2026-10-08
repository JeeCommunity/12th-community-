import re

with open('src/components/ProfileSetup.tsx', 'r') as f:
    content = f.read()

# Don't use user.photoURL as default, so it uses ui-avatars instead
content = content.replace(
    "const [photoURL, setPhotoURL] = useState(existingProfile?.photoURL || user.photoURL || '');",
    "const [photoURL, setPhotoURL] = useState(existingProfile?.photoURL || '');"
)

# Update the ui-avatars URL to be more dynamic and use the typed name, and fix the random background to be consistent based on name
content = content.replace(
    "src={photoURL || `https://ui-avatars.com/api/?name=${name || user.displayName || 'User'}&background=random`}",
    "src={photoURL || `https://ui-avatars.com/api/?name=${encodeURIComponent(name || 'User')}&background=random`}"
)

with open('src/components/ProfileSetup.tsx', 'w') as f:
    f.write(content)
