import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

target_draw = """    let animationId: number;
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
    
    return () => cancelAnimationFrame(animationId);"""

replacement_draw = """    let intervalId: any;
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
      
      // Manually calculate time here since formatTime might not be ready on first render, though it should be.
      const totalSeconds = totalTimeRef.current;
      const h = Math.floor(totalSeconds / 3600);
      const m = Math.floor((totalSeconds % 3600) / 60);
      const s = totalSeconds % 60;
      const timeStr = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
      ctx.fillText(timeStr, canvas.width / 2, 130);
      
      // Draw status indicator
      if (currentSession) {
        ctx.fillStyle = '#22c55e';
        ctx.beginPath();
        ctx.arc(30, 30, 8, 0, 2 * Math.PI);
        ctx.fill();
      }
    };
    
    draw();
    // 1000ms is perfectly fine for a timer and will run in background if media is playing
    intervalId = setInterval(draw, 1000);
    
    // Setup video stream once
    if (videoRef.current && !videoRef.current.srcObject) {
      // 1 fps is enough for a timer, saves CPU!
      videoRef.current.srcObject = canvas.captureStream(1);
    }
    
    return () => clearInterval(intervalId);"""

content = content.replace(target_draw, replacement_draw)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
