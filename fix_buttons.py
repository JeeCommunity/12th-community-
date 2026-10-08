import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

target = """            <div className="flex gap-3">
              <button onClick={() => setIsPiPMode(true)} className="flex-1 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold py-3 rounded-2xl transition-colors flex items-center justify-center gap-2 text-sm backdrop-blur-sm">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><rect x="11" y="11" width="8" height="6" rx="1" ry="1"></rect></svg>
                PiP
              </button>
              <button onClick={() => setIsPiPMode(true)} className="flex-1 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold py-3 rounded-2xl transition-colors flex items-center justify-center gap-2 text-sm backdrop-blur-sm">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
                Notify
              </button>"""

replacement = """            <div className="flex gap-3">
              <button onClick={() => setIsPiPMode(true)} className="flex-1 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold py-3 rounded-2xl transition-colors flex items-center justify-center gap-2 text-sm backdrop-blur-sm">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><rect x="11" y="11" width="8" height="6" rx="1" ry="1"></rect></svg>
                PiP
              </button>
              <button className="flex-1 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold py-3 rounded-2xl transition-colors flex items-center justify-center gap-2 text-sm backdrop-blur-sm">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
                Notify
              </button>"""

content = content.replace(target, replacement)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
