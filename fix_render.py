import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

hidden_elements = """
      <canvas ref={canvasRef} width="400" height="200" style={{ display: 'none' }} />
      <video ref={videoRef} autoPlay muted playsInline style={{ display: 'none' }} />
"""

content = content.replace(
    '<div className="h-full flex flex-col bg-gray-50 overflow-y-auto pb-10 custom-scrollbar">',
    '<div className="h-full flex flex-col bg-gray-50 overflow-y-auto pb-10 custom-scrollbar">\n' + hidden_elements
)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
