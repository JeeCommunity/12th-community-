import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

# Add dockY state
content = content.replace("const [isDocked, setIsDocked] = useState(false);", "const [isDocked, setIsDocked] = useState(false);\n  const [dockY, setDockY] = useState(0);")

target = """        isDocked ? (
          <motion.div 
            initial={{ x: 100 }}
            animate={{ x: 0 }}
            className="fixed top-1/2 right-0 -translate-y-1/2 z-[100] bg-gray-900 text-white rounded-l-2xl shadow-2xl flex items-center border border-r-0 border-gray-700 p-2 cursor-pointer hover:bg-gray-800 transition-colors"
            onClick={() => setIsDocked(false)}
          >"""

replacement = """        isDocked ? (
          <motion.div 
            drag="y"
            dragMomentum={false}
            onDragEnd={(e, info) => setDockY(prev => prev + info.offset.y)}
            initial={{ x: 100 }}
            animate={{ x: 0 }}
            className="fixed right-0 z-[100] bg-gray-900 text-white rounded-l-2xl shadow-2xl flex items-center border border-r-0 border-gray-700 p-2 cursor-grab active:cursor-grabbing hover:bg-gray-800 transition-colors"
            style={{ top: '50%', y: `calc(-50% + ${dockY}px)` }}
            onClick={() => setIsDocked(false)}
          >"""

content = content.replace(target, replacement)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
