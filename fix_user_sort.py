import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

target = """      otherStudents.sort((a, b) => {
        if (a.isStudying && !b.isStudying) return -1;
        if (!a.isStudying && b.isStudying) return 1;
        return b.totalTime - a.totalTime;
      });"""

replacement = """      otherStudents.sort((a, b) => {
        if (a.userId === currentUserProfile.uid) return -1;
        if (b.userId === currentUserProfile.uid) return 1;
        if (a.isStudying && !b.isStudying) return -1;
        if (!a.isStudying && b.isStudying) return 1;
        return b.totalTime - a.totalTime;
      });"""

content = content.replace(target, replacement)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
