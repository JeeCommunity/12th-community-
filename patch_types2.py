import re

with open('src/types.ts', 'r') as f:
    content = f.read()

content = content.replace(
    "  imageUrl?: string;",
    "  imageUrl?: string;\n  imageUrls?: string[];"
)

with open('src/types.ts', 'w') as f:
    f.write(content)
