import re

with open('src/components/Comments.tsx', 'r') as f:
    content = f.read()

target = "{usersMap?.[comments.find(c => c.id === replyingTo)?.authorId || '']?.name || comments.find(c => c.id === replyingTo)?.authorName}"
replacement = "{(usersMap?.[comments.find(c => c.id === replyingTo)?.authorId || '']?.name || comments.find(c => c.id === replyingTo)?.authorName || '').split(' ')[0]}"

content = content.replace(target, replacement)

with open('src/components/Comments.tsx', 'w') as f:
    f.write(content)
