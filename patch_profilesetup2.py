with open('src/components/ProfileSetup.tsx', 'r') as f:
    content = f.read()

content = content.replace("file.size > 2097152", "file.size > 5242880")
content = content.replace("2MB", "5MB")

with open('src/components/ProfileSetup.tsx', 'w') as f:
    f.write(content)
