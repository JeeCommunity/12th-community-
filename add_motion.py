import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

# Add motion
if "from 'framer-motion'" not in content:
    content = content.replace("import React, { useState, useEffect } from 'react';", "import React, { useState, useEffect } from 'react';\nimport { motion } from 'framer-motion';")

# Add icons
content = content.replace("Trash2, Plus } from 'lucide-react';", "Trash2, Plus, Maximize2, Minimize2, GripHorizontal } from 'lucide-react';")

# Add size state
content = content.replace("const [isPiPMode, setIsPiPMode] = useState(false);", "const [isPiPMode, setIsPiPMode] = useState(false);\n  const [pipSize, setPipSize] = useState<'small' | 'large'>('small');")

old_pip = """      {isPiPMode && (
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
      )}"""

new_pip = """      {isPiPMode && (
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

content = content.replace(old_pip, new_pip)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
