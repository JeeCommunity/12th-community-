import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

# Remove sorting from useEffect
target_sort = """      otherStudents.sort((a, b) => {
        if (a.userId === currentUserProfile.uid) return -1;
        if (b.userId === currentUserProfile.uid) return 1;
        if (a.isStudying && !b.isStudying) return -1;
        if (!a.isStudying && b.isStudying) return 1;
        return b.totalTime - a.totalTime;
      });
      
      setActiveStudents(otherStudents);"""

replacement_sort = """      setActiveStudents(otherStudents);"""

content = content.replace(target_sort, replacement_sort)

# Add sorting to render
target_render = """                    {activeStudents.map((student, idx) => {
                      const studentTotalTime = student.totalTime + (student.isStudying && student.currentSessionStartTime ? Math.floor((now - student.currentSessionStartTime) / 1000) : 0);"""

replacement_render = """                    {[...activeStudents].sort((a, b) => {
                      const aTotal = a.totalTime + (a.isStudying && a.currentSessionStartTime ? Math.floor((now - a.currentSessionStartTime) / 1000) : 0);
                      const bTotal = b.totalTime + (b.isStudying && b.currentSessionStartTime ? Math.floor((now - b.currentSessionStartTime) / 1000) : 0);
                      return bTotal - aTotal;
                    }).map((student, idx) => {
                      const studentTotalTime = student.totalTime + (student.isStudying && student.currentSessionStartTime ? Math.floor((now - student.currentSessionStartTime) / 1000) : 0);"""

content = content.replace(target_render, replacement_render)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
