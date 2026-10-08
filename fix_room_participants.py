import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

# Fix unshift
unshift_target = """  if (currentSession && currentSession.roomId === activeRoom?.id) {
    roomParticipants.unshift(currentSession);
  }"""
unshift_replace = """  if (currentSession && currentSession.roomId === activeRoom?.id) {
    roomParticipants.unshift({
      userId: currentUserProfile.uid,
      userName: currentUserProfile.name,
      userPhotoURL: currentUserProfile.photoURL,
      totalTime: todayStudyTime,
      isStudying: true,
      currentSessionStartTime: currentSession.startTime,
      currentGoal: currentSession.goal,
      roomId: currentSession.roomId,
    });
  }"""
content = content.replace(unshift_target, unshift_replace)

# Fix roomParticipants render map
render_target = """                          roomParticipants.map(p => (
                            <div key={p.id} className="flex items-center gap-2 bg-white border border-gray-200 rounded-full pl-1 pr-3 py-1 shadow-sm">
                              <img src={p.userPhotoURL || `https://ui-avatars.com/api/?name=${p.userName}`} alt={p.userName} className="w-6 h-6 rounded-full" />
                              <span className="text-sm font-medium text-gray-800">{p.userName}</span>
                              <div className="flex items-center gap-1 text-green-600 ml-1">
                                <span className="w-1.5 h-1.5 rounded-full bg-green-500" />
                                <span className="text-xs font-bold font-mono">{formatTime(Math.floor((Date.now() - p.startTime)/1000))}</span>
                              </div>
                            </div>
                          ))"""
render_replace = """                          roomParticipants.map(p => (
                            <div key={p.userId} className="flex items-center gap-2 bg-white border border-gray-200 rounded-full pl-1 pr-3 py-1 shadow-sm">
                              <img src={p.userPhotoURL || `https://ui-avatars.com/api/?name=${p.userName}`} alt={p.userName} className="w-6 h-6 rounded-full" />
                              <span className="text-sm font-medium text-gray-800">{p.userName}</span>
                              <div className="flex items-center gap-1 text-green-600 ml-1">
                                <span className="w-1.5 h-1.5 rounded-full bg-green-500" />
                                <span className="text-xs font-bold font-mono">{formatTime(p.totalTime + (p.isStudying && p.currentSessionStartTime ? Math.floor((now - p.currentSessionStartTime)/1000) : 0))}</span>
                              </div>
                            </div>
                          ))"""
content = content.replace(render_target, render_replace)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
