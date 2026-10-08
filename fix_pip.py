import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

content = content.replace("Trash2, Plus, Maximize2, Minimize2, GripHorizontal } from 'lucide-react';", "Trash2, Plus, Maximize2, Minimize2, GripHorizontal, ChevronRight, ChevronLeft } from 'lucide-react';")

# Add isDocked state
content = content.replace("const [pipSize, setPipSize] = useState<'small' | 'large'>('small');", "const [pipSize, setPipSize] = useState<'small' | 'large'>('small');\n  const [isDocked, setIsDocked] = useState(false);")

old_pip = """      {isPiPMode && (
        <motion.div 
          drag
          dragMomentum={false}
          initial={{ opacity: 0, y: 50, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          className={`fixed z-[100] bg-gray-900 text-white rounded-2xl shadow-2xl flex flex-col border border-gray-700 overflow-hidden cursor-move ${pipSize === 'small' ? 'w-64 p-3' : 'w-80 p-5'}`}
          style={{ bottom: '24px', right: '24px', touchAction: 'none' }}
        >
          <div className="flex items-center justify-between mb-2 opacity-50 hover:opacity-100 transition-opacity">
            <GripHorizontal size={16} className="text-gray-400 mx-auto" />
            <div className="absolute top-2 right-2 flex gap-1">
              <button onClick={() => setPipSize(s => s === 'small' ? 'large' : 'small')} className="bg-gray-800 text-gray-400 hover:text-white rounded-full p-1 border border-gray-700 pointer-events-auto">
                {pipSize === 'small' ? <Maximize2 size={12} /> : <Minimize2 size={12} />}
              </button>
              <button onClick={() => setIsPiPMode(false)} className="bg-gray-800 text-gray-400 hover:text-white rounded-full p-1 border border-gray-700 pointer-events-auto">
                <XIcon size={12} />
              </button>
            </div>
          </div>
          
          <div className={`flex items-center gap-4 ${pipSize === 'large' ? 'flex-col text-center mt-2' : ''}`}>
            <div className="flex-1">
              <div className="text-xs text-gray-400 font-semibold mb-1">STUDY TIMER</div>
              <div className={`${pipSize === 'small' ? 'text-2xl' : 'text-4xl'} font-mono font-bold tracking-wider`}>{formatTime(todayStudyTime + elapsedSeconds)}</div>
            </div>
            <button 
              onClick={currentSession ? handleStopSession : handleStartSession}
              disabled={starting || stopping}
              className={`${pipSize === 'small' ? 'w-12 h-12' : 'w-16 h-16'} shrink-0 rounded-full flex items-center justify-center pointer-events-auto ${currentSession ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'}`}
            >
              {currentSession ? <Square size={pipSize === 'small' ? 20 : 28} fill="currentColor" /> : <Play size={pipSize === 'small' ? 20 : 28} fill="currentColor" className="ml-1" />}
            </button>
          </div>
        </motion.div>
      )}"""

new_pip = """      {isPiPMode && (
        isDocked ? (
          <motion.div 
            initial={{ x: 100 }}
            animate={{ x: 0 }}
            className="fixed top-1/2 right-0 -translate-y-1/2 z-[100] bg-gray-900 text-white rounded-l-2xl shadow-2xl flex items-center border border-r-0 border-gray-700 p-2 cursor-pointer hover:bg-gray-800 transition-colors"
            onClick={() => setIsDocked(false)}
          >
            <ChevronLeft size={20} className="text-gray-400 mr-2" />
            <div className="flex flex-col items-center gap-2">
              <div className="text-[10px] text-gray-400 font-semibold rotate-180" style={{ writingMode: 'vertical-rl' }}>STUDY TIMER</div>
              <div className={`w-3 h-3 rounded-full ${currentSession ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`}></div>
            </div>
          </motion.div>
        ) : (
          <motion.div 
            drag
            dragMomentum={false}
            onDragEnd={(e, info) => {
              if (info.point.x > window.innerWidth - 50) {
                setIsDocked(true);
              }
            }}
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            className={`fixed z-[100] bg-gray-900 text-white rounded-2xl shadow-2xl flex flex-col border border-gray-700 overflow-hidden cursor-move ${pipSize === 'small' ? 'w-64 p-3' : 'w-80 p-5'}`}
            style={{ bottom: '24px', right: '24px', touchAction: 'none' }}
          >
            <div className="flex items-center justify-between mb-2 opacity-100 transition-opacity">
              <GripHorizontal size={16} className="text-gray-400 mx-auto opacity-50 hover:opacity-100" />
              <div className="absolute top-2 right-2 flex gap-1">
                <button onClick={() => setIsDocked(true)} className="bg-white/10 hover:bg-white/20 text-gray-200 rounded-full p-1.5 transition-colors pointer-events-auto backdrop-blur-sm" title="Dock to side">
                  <ChevronRight size={14} />
                </button>
                <button onClick={() => setPipSize(s => s === 'small' ? 'large' : 'small')} className="bg-white/10 hover:bg-white/20 text-gray-200 rounded-full p-1.5 transition-colors pointer-events-auto backdrop-blur-sm" title={pipSize === 'small' ? 'Maximize' : 'Minimize'}>
                  {pipSize === 'small' ? <Maximize2 size={14} /> : <Minimize2 size={14} />}
                </button>
                <button onClick={() => setIsPiPMode(false)} className="bg-white/10 hover:bg-white/20 hover:bg-red-500/80 text-gray-200 rounded-full p-1.5 transition-colors pointer-events-auto backdrop-blur-sm" title="Close">
                  <XIcon size={14} />
                </button>
              </div>
            </div>
            
            <div className={`flex items-center gap-4 ${pipSize === 'large' ? 'flex-col text-center mt-2' : ''}`}>
              <div className="flex-1">
                <div className="text-xs text-gray-400 font-semibold mb-1">STUDY TIMER</div>
                <div className={`${pipSize === 'small' ? 'text-2xl' : 'text-4xl'} font-mono font-bold tracking-wider`}>{formatTime(todayStudyTime + elapsedSeconds)}</div>
              </div>
              <button 
                onClick={currentSession ? handleStopSession : handleStartSession}
                disabled={starting || stopping}
                className={`${pipSize === 'small' ? 'w-12 h-12' : 'w-16 h-16'} shrink-0 rounded-full flex items-center justify-center pointer-events-auto shadow-lg transition-transform hover:scale-105 active:scale-95 ${currentSession ? 'bg-red-500 hover:bg-red-600 text-white' : 'bg-green-500 hover:bg-green-600 text-white'}`}
              >
                {currentSession ? <Square size={pipSize === 'small' ? 20 : 28} fill="currentColor" /> : <Play size={pipSize === 'small' ? 20 : 28} fill="currentColor" className="ml-1" />}
              </button>
            </div>
          </motion.div>
        )
      )}"""

content = content.replace(old_pip, new_pip)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
