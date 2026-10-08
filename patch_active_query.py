import re
with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

content = content.replace('''    const activeQuery = query(
      collection(db, 'studySessions'),
      where('status', '==', 'studying'),
      limit(20)
    );''', '''    const activeQuery = query(
      collection(db, 'studySessions'),
      where('status', '==', 'studying'),
      orderBy('startTime', 'desc'),
      limit(20)
    );''')

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
