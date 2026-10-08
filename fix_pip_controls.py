import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

content = content.replace("GripHorizontal, ChevronRight, ChevronLeft } from 'lucide-react';", "GripHorizontal, ChevronRight, ChevronLeft, MoreHorizontal } from 'lucide-react';")

# Add showPipControls state
content = content.replace("const [dockY, setDockY] = useState(0);", "const [dockY, setDockY] = useState(0);\n  const [showPipControls, setShowPipControls] = useState(false);")

target_pip = """            <div className="flex items-center justify-between mb-2 opacity-100 transition-opacity">
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
            </div>"""

replacement_pip = """            <div className="flex items-center justify-between mb-2 transition-opacity">
              <GripHorizontal size={16} className="text-gray-400 mx-auto opacity-50 hover:opacity-100" />
              <div className="absolute top-2 right-2 flex gap-1">
                {showPipControls && (
                  <motion.div initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} className="flex gap-1 mr-1">
                    <button onClick={() => setIsDocked(true)} className="bg-white/10 hover:bg-white/20 text-gray-200 rounded-full p-1.5 transition-colors pointer-events-auto backdrop-blur-sm" title="Dock to side">
                      <ChevronRight size={14} />
                    </button>
                    <button onClick={() => setPipSize(s => s === 'small' ? 'large' : 'small')} className="bg-white/10 hover:bg-white/20 text-gray-200 rounded-full p-1.5 transition-colors pointer-events-auto backdrop-blur-sm" title={pipSize === 'small' ? 'Maximize' : 'Minimize'}>
                      {pipSize === 'small' ? <Maximize2 size={14} /> : <Minimize2 size={14} />}
                    </button>
                    <button onClick={() => setIsPiPMode(false)} className="bg-white/10 hover:bg-white/20 hover:bg-red-500/80 text-gray-200 rounded-full p-1.5 transition-colors pointer-events-auto backdrop-blur-sm" title="Close">
                      <XIcon size={14} />
                    </button>
                  </motion.div>
                )}
                <button onClick={() => setShowPipControls(!showPipControls)} className="text-gray-400 hover:text-white rounded-full p-1 transition-colors pointer-events-auto">
                  <MoreHorizontal size={16} />
                </button>
              </div>
            </div>"""

content = content.replace(target_pip, replacement_pip)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
