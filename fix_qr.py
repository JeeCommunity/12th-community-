import re

with open('src/components/ShareAppModal.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    '<QRCodeCanvas id="share-qr-code" value={shareUrl} size={180} level="H" includeMargin={false} />',
    '<QRCodeCanvas id="share-qr-code" value={shareUrl} size={256} level="H" includeMargin={true} />'
)

with open('src/components/ShareAppModal.tsx', 'w') as f:
    f.write(content)
