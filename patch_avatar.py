import re

with open('src/components/ProfileSetup.tsx', 'r') as f:
    content = f.read()

# Make sure we use a consistent color instead of random
content = content.replace(
    "&background=random",
    "&background=0D8ABC&color=fff"
)

# Also if photoURL is a google one, maybe the user wants to override it with UI avatars unless they explicitly upload?
# Let's just remove the user.photoURL from the initial state, BUT what if it's already in the DB?
# Let's add a clear button or something, or just if it's googleusercontent, we can strip it.
# Actually, let's just ignore googleusercontent.com URLs in photoURL everywhere if they want the name's first letter? No, that's too aggressive.
# If I look at the screenshot, the "A" has a green background. `ui-avatars.com` with `background=random` could be green.
# Wait, look at the screenshot. The "A" is a standard Android/Google green. It's definitely the Google default.
# What if we just clear `photoURL` if it contains 'googleusercontent.com' in `ProfileSetup`?

content = content.replace(
    "const [photoURL, setPhotoURL] = useState(existingProfile?.photoURL || '');",
    "const [photoURL, setPhotoURL] = useState((existingProfile?.photoURL?.includes('googleusercontent.com') ? '' : existingProfile?.photoURL) || '');"
)

with open('src/components/ProfileSetup.tsx', 'w') as f:
    f.write(content)
