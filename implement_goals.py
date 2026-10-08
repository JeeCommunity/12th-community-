import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

# Add states for daily goals
state_code = """  const [todayStudyTime, setTodayStudyTime] = useState(0);
  const [dailyGoals, setDailyGoals] = useState<DailyGoal[]>([]);
  const [isGoalsExpanded, setIsGoalsExpanded] = useState(true);
  const [newGoalTitle, setNewGoalTitle] = useState('');
  const [todayGoalTimes, setTodayGoalTimes] = useState<Record<string, number>>({});
"""
content = re.sub(r'  const \[todayStudyTime, setTodayStudyTime\] = useState\(0\);', state_code, content)

# Add DailyGoal interface at top if needed, we added to types.ts but we need to import it
if "DailyGoal" not in content[:500]:
    content = content.replace("import { UserProfile, StudySession, StudyRoom, RoomMessage } from '../types';", "import { UserProfile, StudySession, StudyRoom, RoomMessage, DailyGoal } from '../types';")

# Add dailyGoals fetcher
goals_fetch_effect = """
  useEffect(() => {
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
  }, [currentUserProfile.uid]);
"""
content = content.replace("  useEffect(() => {\n    const startOfDay = new Date();\n    startOfDay.setHours(0, 0, 0, 0);\n    const q = query(", goals_fetch_effect + "\n  useEffect(() => {\n    const startOfDay = new Date();\n    startOfDay.setHours(0, 0, 0, 0);\n    const q = query(")

# Update the big useEffect to track todayGoalTimes
goal_times_logic_1 = """      let mySession: StudySession | null = null;
      let myTodayTime = 0;
      let goalTimes: Record<string, number> = {};
"""
content = content.replace("      let mySession: StudySession | null = null;\n      let myTodayTime = 0;\n", goal_times_logic_1)

goal_times_logic_2 = """        if (session.userId === currentUserProfile.uid) {
          if (session.status === 'studying') {
            mySession = session;
          } else if (session.status === 'completed' && session.duration) {
            myTodayTime += session.duration;
            if (session.goal) {
              goalTimes[session.goal] = (goalTimes[session.goal] || 0) + session.duration;
            }
          }
        }
"""
content = re.sub(r'        if \(session.userId === currentUserProfile.uid\) \{\n          if \(session.status === \'studying\'\) \{\n            mySession = session;\n          \} else if \(session.status === \'completed\' && session.duration\) \{\n            myTodayTime \+= session.duration;\n          \}\n        \}\n', goal_times_logic_2, content)

goal_times_logic_3 = """      setCurrentSession(mySession);
      setTodayStudyTime(myTodayTime);
      setTodayGoalTimes(goalTimes);
"""
content = content.replace("      setCurrentSession(mySession);\n      setTodayStudyTime(myTodayTime);\n", goal_times_logic_3)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
