import re

with open('src/types.ts', 'r') as f:
    content = f.read()

content = content.replace("  fileUrl?: string;\n  fileName?: string;\n  fileType?: string;\n  fileUrl?: string;\n  fileName?: string;\n  fileType?: string;", "  fileUrl?: string;\n  fileName?: string;\n  fileType?: string;")

with open('src/types.ts', 'w') as f:
    f.write(content)

