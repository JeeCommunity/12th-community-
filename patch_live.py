with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

import re

# Remove the huge query and the commented out code
# We will replace the block from `useEffect(() => { ... startOfDay.setHours(0, 0, 0, 0); ... `
# down to `  }, [currentUserProfile.uid]);\n  /* ... */` with our optimized version.

new_use_effect = '''  useEffect(() => {
    // 1. Fetch active students (studying right now)
    const activeQuery = query(
      collection(db, 'studySessions'),
      where('status', '==', 'studying'),
      limit(50)
    );

    const unsubActive = onSnapshot(activeQuery, (snapshot) => {
      const statsMap = new Map<string, StudentStats>();
      let mySession: StudySession | null = null;
      
      snapshot.forEach((docSnap) => {
        const session = { id: docSnap.id, ...docSnap.data() } as StudySession;
        
        if (session.userId === currentUserProfile.uid) {
          mySession = session;
        }
        
        statsMap.set(session.userId, {
          userId: session.userId,
          userName: session.userName,
          userPhotoURL: session.userPhotoURL,
          totalTime: 0,
          isStudying: true,
          currentSessionStartTime: session.startTime,
          currentGoal: session.goal,
          roomId: session.roomId
        });
      });
      
      setCurrentSession(mySession);
      const otherStudents = Array.from(statsMap.values()).filter(s => s.userId !== currentUserProfile.uid);
      setActiveStudents(otherStudents);
      setLoading(false);
    }, (error) => {
      console.error("Firestore error fetching active sessions:", error);
      setLoading(false);
    });

    // 2. Fetch current user's today's completed time
    const startOfDay = new Date();
    startOfDay.setHours(0, 0, 0, 0);
    const myCompletedQuery = query(
      collection(db, 'studySessions'),
      where('userId', '==', currentUserProfile.uid),
      where('status', '==', 'completed'),
      where('startTime', '>=', startOfDay.getTime())
    );

    const unsubCompleted = onSnapshot(myCompletedQuery, (snapshot) => {
      let myTodayTime = 0;
      let goalTimes: Record<string, number> = {};
      snapshot.forEach((docSnap) => {
        const session = docSnap.data() as StudySession;
        if (session.duration) {
          myTodayTime += session.duration;
          if (session.goal) {
            goalTimes[session.goal] = (goalTimes[session.goal] || 0) + session.duration;
          }
        }
      });
      setTodayStudyTime(myTodayTime);
      setTodayGoalTimes(goalTimes);
    });

    return () => {
      unsubActive();
      unsubCompleted();
    };
  }, [currentUserProfile.uid]);'''

# Using regex to replace from the first `useEffect` with `startOfDay` to the end of the `/* ... */` block
pattern = re.compile(r'  useEffect\(\(\) => \{\n    const startOfDay = new Date\(\);.*?  \}, \[currentUserProfile\.uid\]\);\n\n  /\*.*?\*/', re.DOTALL)
content = pattern.sub(new_use_effect, content)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
