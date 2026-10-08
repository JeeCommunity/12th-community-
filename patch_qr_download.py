import re

with open('src/components/ShareAppModal.tsx', 'r') as f:
    content = f.read()

# Replace SVG with Canvas and add Download icon
content = content.replace(
    "import { QRCodeSVG } from 'qrcode.react';",
    "import { QRCodeCanvas } from 'qrcode.react';"
)
content = content.replace(
    "import { X, Share2, MessageCircle, Send } from 'lucide-react';",
    "import { X, Share2, MessageCircle, Send, Download } from 'lucide-react';"
)

# Add handleDownloadQR function
download_function = """  const handleDownloadQR = () => {
    const canvas = document.getElementById('share-qr-code') as HTMLCanvasElement;
    if (canvas) {
      const pngUrl = canvas.toDataURL('image/png').replace('image/png', 'image/octet-stream');
      const downloadLink = document.createElement('a');
      downloadLink.href = pngUrl;
      downloadLink.download = 'class12-community-qr.png';
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
    }
  };

  const handleNativeShare = async () => {"""
content = content.replace("  const handleNativeShare = async () => {", download_function)

# Replace QRCodeSVG with QRCodeCanvas and add the button
old_qr_section = """          <div className="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 inline-block">
            <QRCodeSVG value={shareUrl} size={180} level="H" includeMargin={false} />
          </div>"""

new_qr_section = """          <div className="flex flex-col items-center gap-3">
            <div className="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 inline-block">
              <QRCodeCanvas id="share-qr-code" value={shareUrl} size={180} level="H" includeMargin={false} />
            </div>
            <button 
              onClick={handleDownloadQR}
              className="flex items-center gap-1.5 text-sm font-semibold text-blue-600 hover:text-blue-700 bg-blue-50 hover:bg-blue-100 px-4 py-2 rounded-full transition-colors"
            >
              <Download size={16} />
              Download QR Code
            </button>
          </div>"""

content = content.replace(old_qr_section, new_qr_section)

with open('src/components/ShareAppModal.tsx', 'w') as f:
    f.write(content)
