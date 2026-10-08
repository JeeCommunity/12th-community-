import re

with open('src/components/ShareAppModal.tsx', 'r') as f:
    content = f.read()

download_function_old = """  const handleDownloadQR = () => {
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
  };"""

download_function_new = """  const handleDownloadQR = () => {
    const originalCanvas = document.getElementById('share-qr-code') as HTMLCanvasElement;
    if (originalCanvas) {
      // Create a new canvas to add text and padding
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      
      const padding = 40;
      const textHeight = 60;
      canvas.width = originalCanvas.width + (padding * 2);
      canvas.height = originalCanvas.height + (padding * 2) + textHeight;
      
      // Fill white background
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Draw QR Code
      ctx.drawImage(originalCanvas, padding, padding);
      
      // Draw Text
      ctx.fillStyle = '#1e3a8a'; // text-blue-900
      ctx.font = 'bold 20px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Class 12th Community', canvas.width / 2, originalCanvas.height + padding + 30);
      
      ctx.fillStyle = '#6b7280'; // text-gray-500
      ctx.font = '14px monospace';
      ctx.fillText(shareUrl, canvas.width / 2, originalCanvas.height + padding + 55);

      const pngUrl = canvas.toDataURL('image/png').replace('image/png', 'image/octet-stream');
      const downloadLink = document.createElement('a');
      downloadLink.href = pngUrl;
      downloadLink.download = 'class12-community-qr.png';
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
    }
  };"""

content = content.replace(download_function_old, download_function_new)

with open('src/components/ShareAppModal.tsx', 'w') as f:
    f.write(content)
