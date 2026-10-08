import re
with open('src/components/CreatePost.tsx', 'r') as f:
    content = f.read()

content = re.sub(
    r'if \(file\.size > 700 \* 1024\) \{\s*alert\("Image is too large! Maximum size is 700KB \(Storage limits\)\."\);',
    r'if (file.size > 10 * 1024 * 1024) {\n        alert("Image is too large! Maximum size is 10MB.");',
    content
)

with open('src/components/CreatePost.tsx', 'w') as f:
    f.write(content)
