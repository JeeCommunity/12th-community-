import re
with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

content = content.replace('''    const unsub = onSnapshot(q, (snapshot) => {
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
    });''', '''    const unsub = onSnapshot(q, (snapshot) => {
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
    });''')

content = content.replace('''      setActiveStudents(active);
      setLoading(false);
    });''', '''      setActiveStudents(active);
      setLoading(false);
    }, (error) => {
      console.error("Firestore error fetching study sessions:", error);
      setLoading(false);
    });''')

content = content.replace('''    const unsub = onSnapshot(q, (snapshot) => {
      const msgs: RoomMessage[] = [];
      snapshot.forEach(docSnap => msgs.push({ id: docSnap.id, ...docSnap.data() } as RoomMessage));
      setRoomMessages(msgs);
    });''', '''    const unsub = onSnapshot(q, (snapshot) => {
      const msgs: RoomMessage[] = [];
      snapshot.forEach(docSnap => msgs.push({ id: docSnap.id, ...docSnap.data() } as RoomMessage));
      setRoomMessages(msgs);
    }, (error) => {
      console.error("Firestore error fetching room messages:", error);
    });''')

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
