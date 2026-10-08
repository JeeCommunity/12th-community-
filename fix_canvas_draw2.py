import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

target = """      // Manually calculate time here since formatTime might not be ready on first render, though it should be.
      const totalSeconds = totalTimeRef.current;"""

replacement = """      // Calculate real time in case React intervals are throttled in background
      let totalSeconds = totalTimeRef.current;
      if (currentSession && currentSession.startTime) {
        totalSeconds = todayStudyTime + Math.floor((Date.now() - currentSession.startTime) / 1000);
      }"""

content = content.replace(target, replacement)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
