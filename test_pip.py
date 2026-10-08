import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

# Add state
content = content.replace("const [sendingMsg, setSendingMsg] = useState(false);", "const [sendingMsg, setSendingMsg] = useState(false);\n  const [isPiPMode, setIsPiPMode] = useState(false);")

# Update button
content = content.replace('PiP\n              </button>', 'PiP\n              </button>').replace('<button className="flex-1 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold py-3 rounded-2xl transition-colors flex items-center justify-center gap-2 text-sm backdrop-blur-sm">', '<button onClick={() => setIsPiPMode(true)} className="flex-1 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold py-3 rounded-2xl transition-colors flex items-center justify-center gap-2 text-sm backdrop-blur-sm">')


# Add PiP component at the end of the return statement
pip_ui = """
      {isPiPMode && (
        <div className="fixed bottom-6 right-6 bg-gray-900 text-white p-4 rounded-2xl shadow-2xl z-50 flex items-center gap-4 w-64 border border-gray-700 animate-in slide-in-from-bottom-5">
          <div className="flex-1">
            <div className="text-xs text-gray-400 font-semibold mb-1">STUDY TIMER</div>
            <div className="text-2xl font-mono font-bold tracking-wider">{formatTime(todayStudyTime + elapsedSeconds)}</div>
          </div>
          <button 
            onClick={currentSession ? handleStopSession : handleStartSession}
            disabled={starting || stopping}
            className={`w-12 h-12 rounded-full flex items-center justify-center ${currentSession ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'}`}
          >
            {currentSession ? <Square size={20} fill="currentColor" /> : <Play size={20} fill="currentColor" className="ml-1" />}
          </button>
          <button onClick={() => setIsPiPMode(false)} className="absolute -top-2 -right-2 bg-gray-800 text-gray-400 hover:text-white rounded-full p-1 border border-gray-700">
            <XIcon size={16} />
          </button>
        </div>
      )}
"""

content = content.replace('    </div>\n  );\n}\n', pip_ui + '    </div>\n  );\n}\n')

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
