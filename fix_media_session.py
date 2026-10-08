import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

target_click = """        // Setup Media Session API for play/pause from PiP
        if ('mediaSession' in navigator) {
          navigator.mediaSession.setActionHandler('play', () => {
            handleStartSession();
          });
          navigator.mediaSession.setActionHandler('pause', () => {
            handleStopSession();
          });
        }"""

content = content.replace(target_click, "")

media_session_effect = """
  useEffect(() => {
    if ('mediaSession' in navigator && isNativePipActive.current) {
      navigator.mediaSession.setActionHandler('play', () => {
        handleStartSession();
      });
      navigator.mediaSession.setActionHandler('pause', () => {
        handleStopSession();
      });
      navigator.mediaSession.playbackState = currentSession ? 'playing' : 'paused';
    }
  }, [currentSession, starting, stopping, studyGoal, activeRoom, currentUserProfile]);
"""

content = content.replace("  const handlePiPClick = async () => {", media_session_effect + "\n  const handlePiPClick = async () => {")

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
