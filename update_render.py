import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

# 1. Remove elapsedSeconds state
content = re.sub(r'  const \[elapsedSeconds, setElapsedSeconds\] = useState\(0\);\n', '', content)

# 2. Remove elapsedSeconds useEffect
elapsed_effect_pattern = r'  useEffect\(\(\) => \{\n    let interval: any;\n    if \(currentSession\) \{\n      const updateTimer = \(\) => \{\n        const now = Date\.now\(\);\n        const diff = Math\.floor\(\(now - currentSession\.startTime\) / 1000\);\n        setElapsedSeconds\(diff >= 0 \? diff : 0\);\n      \};\n      updateTimer\(\);\n      interval = setInterval\(updateTimer, 1000\);\n    \} else \{\n      setElapsedSeconds\(0\);\n    \}\n    return \(\) => \{\n      if \(interval\) clearInterval\(interval\);\n    \};\n  \}, \[currentSession\]\);\n'
content = re.sub(elapsed_effect_pattern, '', content)

# 3. Replace {formatTime(todayStudyTime + elapsedSeconds)}
content = content.replace(
    "{formatTime(todayStudyTime + elapsedSeconds)}",
    "{formatTime(todayStudyTime + (currentSession ? Math.floor((now - currentSession.startTime) / 1000) : 0))}"
)

# 4. Replace {formatTime(elapsedSeconds)} for the top user in list
content = content.replace(
    "{formatTime(elapsedSeconds)}",
    "{formatTime(todayStudyTime + (currentSession ? Math.floor((now - currentSession.startTime) / 1000) : 0))}"
)

# 5. Replace activeStudents map
start_marker = "{activeStudents.map((student, idx) => ("
end_marker = "                    )} <!-- END OF ACTIVE STUDENTS MAP -->" # Wait, I don't know the exact end marker.

