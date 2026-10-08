import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

pattern = r'  if \(currentSession && currentSession.roomId === activeRoom\?\.id\) \{\n    roomParticipants\.unshift\(\{[\s\S]*?\}\);\n  \}\n'
content = re.sub(pattern, '', content)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
