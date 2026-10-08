import re
with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

content = content.replace('''useEffect(() => {
    const startOfDay = new Date();
    startOfDay.setHours(0, 0, 0, 0);
    const q = query(
      collection(db, 'dailyGoals'),
      where('createdAt', '>=', startOfDay.getTime()),
      orderBy('createdAt', 'asc'),
      limit(100)
    );
    const unsub = onSnapshot(q, (snapshot) => {
      const goals: DailyGoal[] = [];
      const grouped: Record<string, DailyGoal[]> = {};
      snapshot.forEach(docSnap => {
        const data = { id: docSnap.id, ...docSnap.data() } as DailyGoal;
        goals.push(data);
        if (!grouped[data.userId]) grouped[data.userId] = [];
        grouped[data.userId].push(data);
      });
      setAllDailyGoals(grouped);
      setDailyGoals(grouped[currentUserProfile.uid] || []);
    }, (error) => {
      console.error("Firestore error fetching daily goals:", error);
    });
    return () => unsub();
  }, [currentUserProfile.uid]);''', '''useEffect(() => {
    const startOfDay = new Date();
    startOfDay.setHours(0, 0, 0, 0);
    const q = query(
      collection(db, 'dailyGoals'),
      where('userId', '==', currentUserProfile.uid),
      where('createdAt', '>=', startOfDay.getTime()),
      orderBy('createdAt', 'asc'),
      limit(20)
    );
    const unsub = onSnapshot(q, (snapshot) => {
      const goals: DailyGoal[] = [];
      snapshot.forEach(docSnap => {
        const data = { id: docSnap.id, ...docSnap.data() } as DailyGoal;
        goals.push(data);
      });
      setDailyGoals(goals);
    }, (error) => {
      console.error("Firestore error fetching daily goals:", error);
    });
    return () => unsub();
  }, [currentUserProfile.uid]);''')

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
