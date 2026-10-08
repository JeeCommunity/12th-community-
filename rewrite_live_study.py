import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

# Add interface
interface_code = """export interface StudentStats {
  userId: string;
  userName: string;
  userPhotoURL?: string;
  totalTime: number;
  isStudying: boolean;
  currentSessionStartTime?: number;
  currentGoal?: string;
  roomId?: string;
}
"""
content = content.replace("interface Props {", interface_code + "\ninterface Props {")

# Change state types
content = content.replace(
    "const [activeStudents, setActiveStudents] = useState<StudySession[]>([]);",
    "const [activeStudents, setActiveStudents] = useState<StudentStats[]>([]);\n  const [now, setNow] = useState(Date.now());"
)

# Add now interval
now_interval = """  useEffect(() => {
    const interval = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(interval);
  }, []);
"""
content = content.replace("  useEffect(() => {\n    const q = query(", now_interval + "\n  useEffect(() => {\n    const startOfDay = new Date();\n    startOfDay.setHours(0, 0, 0, 0);\n    const q = query(\n      collection(db, 'studySessions'),\n      where('startTime', '>=', startOfDay.getTime())\n    );\n\n    const unsub = onSnapshot(q, (snapshot) => {\n      const statsMap = new Map<string, StudentStats>();\n      let mySession: StudySession | null = null;\n      let myTodayTime = 0;\n      \n      snapshot.forEach((docSnap) => {\n        const session = { id: docSnap.id, ...docSnap.data() } as StudySession;\n        \n        if (session.userId === currentUserProfile.uid) {\n          if (session.status === 'studying') {\n            mySession = session;\n          } else if (session.status === 'completed' && session.duration) {\n            myTodayTime += session.duration;\n          }\n        }\n        \n        if (!statsMap.has(session.userId)) {\n          statsMap.set(session.userId, {\n            userId: session.userId,\n            userName: session.userName,\n            userPhotoURL: session.userPhotoURL,\n            totalTime: 0,\n            isStudying: false,\n          });\n        }\n        \n        const stat = statsMap.get(session.userId)!;\n        \n        if (session.status === 'studying') {\n          stat.isStudying = true;\n          stat.currentSessionStartTime = session.startTime;\n          stat.currentGoal = session.goal;\n          stat.roomId = session.roomId;\n        } else if (session.status === 'completed' && session.duration) {\n          stat.totalTime += session.duration;\n        }\n      });\n      \n      setCurrentSession(mySession);\n      setTodayStudyTime(myTodayTime);\n      \n      const otherStudents = Array.from(statsMap.values()).filter(s => s.userId !== currentUserProfile.uid);\n      \n      otherStudents.sort((a, b) => {\n        if (a.isStudying && !b.isStudying) return -1;\n        if (!a.isStudying && b.isStudying) return 1;\n        return b.totalTime - a.totalTime;\n      });\n      \n      setActiveStudents(otherStudents);\n      setLoading(false);\n    });\n\n    return () => unsub();\n  }, [currentUserProfile.uid]);\n\n  /*")

# comment out the old fetchers
content = content.replace("    return () => { if (unsub) unsub(); };\n  }, [currentUserProfile.uid]);", "    return () => { if (unsub) unsub(); };\n  }, [currentUserProfile.uid]);\n  */")


with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
