import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

content = content.replace("    const unsub = onSnapshot(q, (snapshot) => {", "    const unsub = onSnapshot(q, (snapshot) => {", 1)
content = content.replace("    });\\n\\n    return () => unsub();", "    }, (error) => { console.error('Snapshot error:', error); });\\n\\n    return () => unsub();", 1)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
