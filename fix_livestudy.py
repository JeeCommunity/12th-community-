import re
with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

content = content.replace('''    const fetchData = async () => {
      try {
        const [activeSnap, completedSnap] = await Promise.all([
          getDocs(activeQuery),
          getDocs(myCompletedQuery)
        ]);''', '''    const startOfDay = new Date();
    startOfDay.setHours(0, 0, 0, 0);
    const myCompletedQuery = query(
      collection(db, 'studySessions'),
      where('userId', '==', currentUserProfile.uid),
      where('status', '==', 'completed'),
      where('startTime', '>=', startOfDay.getTime())
    );

    const fetchData = async () => {
      try {
        const [activeSnap, completedSnap] = await Promise.all([
          getDocs(activeQuery),
          getDocs(myCompletedQuery)
        ]);''')

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
