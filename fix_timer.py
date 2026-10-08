with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

target = """          <div className="text-6xl sm:text-7xl font-black tracking-widest font-mono mb-2 drop-shadow-md">
            {formatTime(elapsedSeconds)}
          </div>
          <div className="text-blue-200 text-xs font-semibold uppercase tracking-widest mb-6">
            MY STUDY TIME • {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
          </div>"""

replacement = """          <div className="text-6xl sm:text-7xl font-black tracking-widest font-mono mb-2 drop-shadow-md">
            {formatTime(todayStudyTime + elapsedSeconds)}
          </div>
          <div className="text-blue-200 text-xs font-semibold uppercase tracking-widest mb-6">
            MY STUDY TIME • {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
          </div>"""

content = content.replace(target, replacement)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
