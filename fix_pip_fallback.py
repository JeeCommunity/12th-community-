import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

content = content.replace("if (videoRef.current && document.pictureInPictureEnabled) {", "if (videoRef.current && typeof videoRef.current.requestPictureInPicture === 'function') {")

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
