with open('src/components/PostCard.tsx', 'r') as f:
    content = f.read()
content = content.replace("src={getAvatarUrl(photoURL, name)}", "src={getAvatarUrl(photoURL, authorName)}")
with open('src/components/PostCard.tsx', 'w') as f:
    f.write(content)

with open('src/components/Comments.tsx', 'r') as f:
    content = f.read()
content = content.replace("src={getAvatarUrl(photoURL, name)}", "src={getAvatarUrl(photoURL, authorName)}")
with open('src/components/Comments.tsx', 'w') as f:
    f.write(content)
