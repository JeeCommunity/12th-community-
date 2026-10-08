import re
with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

# 1. Patch dailyGoals
content = re.sub(r'    const unsub = onSnapshot\(q, \(snapshot\) => \{.*?return \(\) => unsub\(\);\n  \}, \[currentUserProfile\.uid\]\);', '''    const fetchGoals = async () => {
      try {
        const snapshot = await getDocs(q);
        const goals: DailyGoal[] = [];
        snapshot.forEach(docSnap => {
          const data = { id: docSnap.id, ...docSnap.data() } as DailyGoal;
          goals.push(data);
        });
        setDailyGoals(goals);
      } catch (error) {
        console.error("Firestore error fetching daily goals:", error);
      }
    };
    fetchGoals();
    const interval = setInterval(fetchGoals, 30000);
    return () => clearInterval(interval);
  }, [currentUserProfile.uid]);''', content, flags=re.DOTALL, count=1)

# 2. Patch active and completed queries
content = re.sub(r'    const unsubActive = onSnapshot\(activeQuery, \(snapshot\) => \{.*?    return \(\) => \{\n      unsubActive\(\);\n      unsubCompleted\(\);\n    \};\n  \}, \[currentUserProfile\.uid\]\);', '''    const fetchData = async () => {
      try {
        const [activeSnap, completedSnap] = await Promise.all([
          getDocs(activeQuery),
          getDocs(myCompletedQuery)
        ]);

        const statsMap = new Map<string, StudentStats>();
        let mySession: StudySession | null = null;
        
        activeSnap.forEach((docSnap) => {
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
        
        let myTodayTime = 0;
        let goalTimes: Record<string, number> = {};
        completedSnap.forEach((docSnap) => {
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
      } catch (error) {
        console.error("Firestore error fetching study data:", error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, [currentUserProfile.uid]);''', content, flags=re.DOTALL)

# 3. Patch roomMessages
content = re.sub(r'    const unsub = onSnapshot\(q, \(snapshot\) => \{.*?return \(\) => unsub\(\);\n  \}, \[activeRoom\]\);', '''    const fetchMessages = async () => {
      try {
        const snapshot = await getDocs(q);
        const msgs: RoomMessage[] = [];
        snapshot.forEach(docSnap => msgs.push({ id: docSnap.id, ...docSnap.data() } as RoomMessage));
        setRoomMessages(msgs.reverse());
      } catch (error) {
        console.error("Firestore error fetching room messages:", error);
      }
    };
    fetchMessages();
    const interval = setInterval(fetchMessages, 5000); // 5s for chat to feel a bit live
    return () => clearInterval(interval);
  }, [activeRoom]);''', content, flags=re.DOTALL)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
