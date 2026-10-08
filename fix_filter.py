import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

target = "const otherStudents = Array.from(statsMap.values()).filter(s => s.userId !== currentUserProfile.uid);"
replacement = "const otherStudents = Array.from(statsMap.values()).filter(s => s.userId !== currentUserProfile.uid && (s.totalTime > 0 || s.isStudying));"
content = content.replace(target, replacement)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
