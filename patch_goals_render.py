import re
with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

content = content.replace('''                                const userGoals = allDailyGoals[student.userId] || [];''', '''                                const userGoals = student.userId === currentUserProfile.uid ? dailyGoals : [];''')

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
