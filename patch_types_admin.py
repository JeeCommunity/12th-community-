import re

with open('src/types.ts', 'r') as f:
    content = f.read()

content = content.replace(
    "  isBlocked?: boolean;\n  state?: string;",
    "  isBlocked?: boolean;\n  isAdmin?: boolean;\n  state?: string;"
)

content = content.replace(
    "  reportsCount: number;\n}",
    "  reportsCount: number;\n  isPinned?: boolean;\n  reports?: {userId: string, reason: string}[];\n}"
)

with open('src/types.ts', 'w') as f:
    f.write(content)
