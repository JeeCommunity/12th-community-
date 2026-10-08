import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

# Add allDailyGoals state
content = content.replace("  const [dailyGoals, setDailyGoals] = useState<DailyGoal[]>([]);", "  const [dailyGoals, setDailyGoals] = useState<DailyGoal[]>([]);\n  const [allDailyGoals, setAllDailyGoals] = useState<Record<string, DailyGoal[]>>({});")

fetch_code = """
  useEffect(() => {
    const startOfDay = new Date();
    startOfDay.setHours(0, 0, 0, 0);
    const q = query(
      collection(db, 'dailyGoals'),
      where('createdAt', '>=', startOfDay.getTime()),
      orderBy('createdAt', 'asc')
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
    });
    return () => unsub();
  }, [currentUserProfile.uid]);
"""

old_fetch_code = """  useEffect(() => {
    const startOfDay = new Date();
    startOfDay.setHours(0, 0, 0, 0);
    const q = query(
      collection(db, 'dailyGoals'),
      where('userId', '==', currentUserProfile.uid),
      where('createdAt', '>=', startOfDay.getTime()),
      orderBy('createdAt', 'asc')
    );
    const unsub = onSnapshot(q, (snapshot) => {
      const goals: DailyGoal[] = [];
      snapshot.forEach(docSnap => goals.push({ id: docSnap.id, ...docSnap.data() } as DailyGoal));
      setDailyGoals(goals);
    });
    return () => unsub();
  }, [currentUserProfile.uid]);"""

content = content.replace(old_fetch_code, fetch_code.strip())

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
