import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

content = content.replace("goal: studyGoal.trim() || (activeRoom?.goal || 'Focusing on studies'),", "goal: studyGoal.trim() || activeRoom?.goal || '',")

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
