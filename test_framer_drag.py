import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

target = """            style={{ top: '50%', y: `calc(-50% + ${dockY}px)` }}"""
replacement = """            style={{ top: '50%', marginTop: '-32px', y: dockY }}"""

content = content.replace(target, replacement)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
