import re
with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

content = content.replace('''    const q = query(
      collection(db, 'dailyGoals'),
      where('userId', '==', currentUserProfile.uid),
      where('createdAt', '>=', startOfDay.getTime()),
      orderBy('createdAt', 'asc')
    );''', '''    const q = query(
      collection(db, 'dailyGoals'),
      where('createdAt', '>=', startOfDay.getTime()),
      orderBy('createdAt', 'asc'),
      limit(100)
    );''')

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
