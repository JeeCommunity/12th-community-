import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

content = content.replace("{activeStudents.filter(s => s.isStudying).length + (currentSession ? 1 : 0)} Online", "{activeStudents.filter(s => s.isStudying).length} Online")

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
