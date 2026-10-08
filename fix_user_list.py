import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

target = """      setCurrentSession(mySession);
      setTodayStudyTime(myTodayTime);
      setTodayGoalTimes(goalTimes);
      
      const otherStudents = Array.from(statsMap.values()).filter(s => s.totalTime > 0 || s.isStudying);"""

replacement = """      if (!statsMap.has(currentUserProfile.uid)) {
        statsMap.set(currentUserProfile.uid, {
          userId: currentUserProfile.uid,
          userName: currentUserProfile.name,
          userPhotoURL: currentUserProfile.photoURL,
          totalTime: 0,
          isStudying: false,
        });
      }
      
      setCurrentSession(mySession);
      setTodayStudyTime(myTodayTime);
      setTodayGoalTimes(goalTimes);
      
      const otherStudents = Array.from(statsMap.values()).filter(s => s.userId === currentUserProfile.uid || s.totalTime > 0 || s.isStudying);"""

content = content.replace(target, replacement)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
