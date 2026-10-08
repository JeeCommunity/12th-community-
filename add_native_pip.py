import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

# Add useRef
content = content.replace("import React, { useState, useEffect } from 'react';", "import React, { useState, useEffect, useRef } from 'react';")

# Add refs and canvas drawing
refs_code = """
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const totalTimeRef = useRef(0);
  const isNativePipActive = useRef(false);

  useEffect(() => {
    totalTimeRef.current = todayStudyTime + elapsedSeconds;
  }, [todayStudyTime, elapsedSeconds]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    let animationId: number;
    const draw = () => {
      ctx.fillStyle = '#111827';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      ctx.fillStyle = '#9ca3af';
      ctx.font = 'bold 24px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('STUDY TIMER', canvas.width / 2, 50);
      
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 72px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(formatTime(totalTimeRef.current), canvas.width / 2, 130);
      
      // Draw status indicator
      if (currentSession) {
        ctx.fillStyle = '#22c55e';
        ctx.beginPath();
        ctx.arc(30, 30, 8, 0, 2 * Math.PI);
        ctx.fill();
      }
      
      animationId = requestAnimationFrame(draw);
    };
    draw();
    
    // Setup video stream once
    if (videoRef.current && !videoRef.current.srcObject) {
      videoRef.current.srcObject = canvas.captureStream(30);
    }
    
    return () => cancelAnimationFrame(animationId);
  }, [currentSession]); // re-run if session changes for the status indicator (though we could also use a ref for it)

  const handlePiPClick = async () => {
    try {
      if (videoRef.current && document.pictureInPictureEnabled) {
        await videoRef.current.play();
        await videoRef.current.requestPictureInPicture();
        isNativePipActive.current = true;
        
        // Setup Media Session API for play/pause from PiP
        if ('mediaSession' in navigator) {
          navigator.mediaSession.setActionHandler('play', () => {
            handleStartSession();
          });
          navigator.mediaSession.setActionHandler('pause', () => {
            handleStopSession();
          });
        }
      } else {
        setIsPiPMode(true);
      }
    } catch (err) {
      console.error('Native PiP failed:', err);
      setIsPiPMode(true);
    }
  };

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    
    const onLeavePiP = () => {
      isNativePipActive.current = false;
    };
    video.addEventListener('leavepictureinpicture', onLeavePiP);
    return () => video.removeEventListener('leavepictureinpicture', onLeavePiP);
  }, []);
"""

content = content.replace("  const [showPipControls, setShowPipControls] = useState(false);", "  const [showPipControls, setShowPipControls] = useState(false);\n" + refs_code)

content = content.replace("onClick={() => setIsPiPMode(true)}", "onClick={handlePiPClick}")

# Add hidden canvas and video to the render tree
hidden_elements = """
      <canvas ref={canvasRef} width="400" height="200" style={{ display: 'none' }} />
      <video ref={videoRef} muted playsInline style={{ display: 'none' }} />
"""
content = content.replace("    <div className=\"max-w-4xl mx-auto space-y-6\">", "    <div className=\"max-w-4xl mx-auto space-y-6\">\n" + hidden_elements)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
