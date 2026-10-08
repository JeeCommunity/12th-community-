import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

content = content.replace("doc, getDoc, serverTimestamp, getDocs", "doc, getDoc, serverTimestamp, getDocs, deleteDoc")

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
