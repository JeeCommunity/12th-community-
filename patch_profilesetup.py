with open('src/components/ProfileSetup.tsx', 'r') as f:
    content = f.read()

content = content.replace("file.size > 1048576", "file.size > 2097152")
content = content.replace("1MB", "2MB")

with open('src/components/ProfileSetup.tsx', 'w') as f:
    f.write(content)
