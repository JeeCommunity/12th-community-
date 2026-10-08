import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

target = """    <div className="h-full flex flex-col bg-gray-50 overflow-y-auto pb-10 custom-scrollbar">
      <div className="bg-white px-4 py-3 border-b flex justify-center sticky top-0 z-10 shadow-sm">
        <h1 className="font-bold text-lg text-gray-900">Live Study Room</h1>
      </div>

      <div className="p-4 max-w-3xl mx-auto w-full space-y-6">
        
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-6 text-center text-white">
            <h2 className="text-2xl font-bold mb-1">Study together and stay focused.</h2>
            <p className="text-blue-100 text-sm opacity-90">Join the class 12 community in real-time study sessions.</p>
          </div>
          
          <div className="p-6 flex flex-col items-center">
            {currentSession && (
              <div className="mb-4 inline-flex items-center gap-2 bg-green-50 text-green-700 px-3 py-1 rounded-full text-sm font-semibold border border-green-200">
                <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                STUDYING
              </div>
            )}
            
            <div className="text-5xl md:text-6xl font-black text-gray-800 tracking-tight font-mono mb-2">
              {formatTime(elapsedSeconds)}
            </div>
            <div className="text-gray-500 text-sm font-medium mb-6 uppercase tracking-wider">
              My Study Time
            </div>

            {!currentSession ? (
              <div className="w-full max-w-sm space-y-4">
                <input
                  type="text"
                  value={studyGoal}
                  onChange={(e) => setStudyGoal(e.target.value)}
                  placeholder="What are you studying? (Optional)"
                  className="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
                />
                <button
                  onClick={handleStartSession}
                  disabled={starting}
                  className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3.5 rounded-xl transition-transform hover:scale-[1.02] active:scale-[0.98]"
                >
                  {starting ? <Loader2 className="animate-spin" /> : <Play size={20} />}
                  Start Study Session
                </button>
              </div>
            ) : (
              <div className="w-full max-w-sm space-y-4 text-center">
                <div className="bg-gray-50 rounded-xl p-3 border border-gray-200 flex flex-col gap-1">
                  <span className="text-gray-500 text-xs uppercase font-bold block">Current Goal</span>
                  <span className="text-gray-800 font-medium">{currentSession.goal || 'Focusing on studies'}</span>
                  {currentSession.roomId && (
                    <div className="text-xs text-blue-600 font-semibold mt-1">
                      📍 Studying in a private room
                    </div>
                  )}
                </div>
                <button
                  onClick={handleStopSession}
                  disabled={stopping}
                  className="w-full flex items-center justify-center gap-2 bg-red-500 hover:bg-red-600 text-white font-bold py-3.5 rounded-xl transition-transform hover:scale-[1.02] active:scale-[0.98]"
                >
                  {stopping ? <Loader2 className="animate-spin" /> : <Square size={20} />}
                  Stop Session
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex flex-col items-center justify-center text-center">
            <span className="text-gray-500 text-[11px] sm:text-xs uppercase font-bold mb-1">Today's Study Time</span>
            <span className="text-2xl font-bold text-blue-600">{formatTime(todayStudyTime)}</span>
          </div>
          <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex flex-col items-center justify-center text-center">
            <span className="text-gray-500 text-[11px] sm:text-xs uppercase font-bold mb-1">Active Students</span>
            <span className="text-2xl font-bold text-indigo-600">{activeStudents.length + (currentSession ? 1 : 0)}</span>
          </div>
        </div>"""

replacement = """    <div className="h-full flex flex-col bg-gray-50 overflow-y-auto pb-10 custom-scrollbar">
      <div className="p-4 max-w-3xl mx-auto w-full space-y-6">
        
        {/* Main Blue Card */}
        <div className="bg-gradient-to-b from-blue-500 to-indigo-600 rounded-3xl p-6 text-center text-white shadow-lg flex flex-col items-center relative overflow-hidden">
          <h2 className="text-3xl font-bold mb-2">Live Study Room</h2>
          <p className="text-blue-100 text-sm opacity-90 max-w-xs mb-4">
            Study together, set daily goals, and see your friends' screen time live.
          </p>
          
          <button className="bg-amber-400 hover:bg-amber-500 text-amber-950 text-xs font-bold px-4 py-1.5 rounded-full mb-6 flex items-center gap-2 transition-colors">
            <span className="text-sm">🔔</span> IMPORTANT: STUDY RULES
          </button>
          
          <div className="text-6xl sm:text-7xl font-black tracking-widest font-mono mb-2 drop-shadow-md">
            {formatTime(elapsedSeconds)}
          </div>
          <div className="text-blue-200 text-xs font-semibold uppercase tracking-widest mb-6">
            MY STUDY TIME • {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
          </div>

          <div className="w-full max-w-sm space-y-3">
            {!currentSession ? (
              <button
                onClick={handleStartSession}
                disabled={starting}
                className="w-full flex items-center justify-center gap-2 bg-[#10b981] hover:bg-[#059669] text-white font-bold py-3.5 rounded-2xl transition-transform hover:scale-[1.02] active:scale-[0.98] shadow-md"
              >
                {starting ? <Loader2 className="animate-spin" /> : <Play size={20} fill="currentColor" />}
                Start Session
              </button>
            ) : (
              <button
                onClick={handleStopSession}
                disabled={stopping}
                className="w-full flex items-center justify-center gap-2 bg-red-500 hover:bg-red-600 text-white font-bold py-3.5 rounded-2xl transition-transform hover:scale-[1.02] active:scale-[0.98] shadow-md"
              >
                {stopping ? <Loader2 className="animate-spin" /> : <Square size={20} fill="currentColor" />}
                Stop Session
              </button>
            )}
            
            <div className="flex gap-3">
              <button className="flex-1 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold py-3 rounded-2xl transition-colors flex items-center justify-center gap-2 text-sm backdrop-blur-sm">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><rect x="11" y="11" width="8" height="6" rx="1" ry="1"></rect></svg>
                PiP
              </button>
              <button className="flex-1 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold py-3 rounded-2xl transition-colors flex items-center justify-center gap-2 text-sm backdrop-blur-sm">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
                Notify
              </button>
            </div>
          </div>
        </div>

        {/* Today's Goals Mockup */}
        <div className="bg-white rounded-3xl p-5 shadow-sm border border-gray-100 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full border border-blue-200 flex items-center justify-center">
              <div className="w-4 h-4 rounded-full border-2 border-blue-500 flex items-center justify-center">
                <div className="w-1 h-1 rounded-full bg-blue-500"></div>
              </div>
            </div>
            <span className="text-xl font-bold text-gray-800">Today's Goals</span>
            <span className="bg-blue-50 text-blue-600 font-bold px-3 py-1 rounded-full text-sm">0</span>
          </div>
          <button className="text-gray-400 hover:text-gray-600">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
          </button>
        </div>"""

content = content.replace(target, replacement)

# We also need to fix the tabs style to match the screenshot
tabs_target = """        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab('global')}
              className={`flex-1 py-3 text-sm font-semibold transition-colors ${activeTab === 'global' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
            >
              Global Study Room
            </button>
            <button
              onClick={() => setActiveTab('friends')}
              className={`flex-1 py-3 text-sm font-semibold transition-colors ${activeTab === 'friends' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
            >
              Study with Friends
            </button>
          </div>

          <div className="p-4">"""

tabs_replacement = """        {/* Tabs */}
        <div className="bg-white rounded-full shadow-sm border border-gray-100 flex p-1.5 gap-1">
          <button
            onClick={() => setActiveTab('global')}
            className={`flex-1 py-3.5 px-4 text-sm font-bold rounded-full transition-colors ${activeTab === 'global' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-50'}`}
          >
            Global Study Room
          </button>
          <button
            onClick={() => setActiveTab('friends')}
            className={`flex-1 py-3.5 px-4 text-sm font-bold rounded-full transition-colors ${activeTab === 'friends' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-50'}`}
          >
            Study with Friends
          </button>
        </div>

        <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="p-5">"""

content = content.replace(tabs_target, tabs_replacement)

# And fix the active students list style
active_students_target = """                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-bold text-gray-900">Active Students</h3>
                  <span className="text-sm text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">{activeStudents.length} Online</span>
                </div>
                
                {loading ? (
                  <div className="flex justify-center py-8"><Loader2 className="animate-spin text-blue-500" /></div>
                ) : activeStudents.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <Users size={40} className="mx-auto mb-3 opacity-20" />
                    <p>No other students studying right now.</p>
                    <p className="text-sm mt-1">Be the one to inspire others!</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {activeStudents.map(student => (
                      <div key={student.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-xl border border-gray-100">
                        <img 
                          src={student.userPhotoURL || `https://ui-avatars.com/api/?name=${student.userName}`}
                          alt={student.userName}
                          className="w-10 h-10 rounded-full object-cover border border-gray-200"
                        />
                        <div className="flex-grow min-w-0">
                          <div className="flex items-center justify-between">
                            <span className="font-bold text-sm text-gray-900 truncate">{student.userName}</span>
                            <div className="flex items-center gap-1.5 bg-green-50 text-green-700 px-2 py-0.5 rounded-full text-[10px] sm:text-xs font-semibold">
                              <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                              Studying
                            </div>
                          </div>
                          <div className="flex items-center justify-between mt-1">
                            <span className="text-xs text-gray-500 truncate max-w-[150px]">{student.goal || 'Focusing...'}</span>
                            <span className="text-xs font-medium text-gray-700 flex items-center gap-1">
                              <Clock size={12} />
                              {formatTime(Math.floor((Date.now() - student.startTime) / 1000))}
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}"""

active_students_replacement = """                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                    <Users size={24} className="text-blue-500" />
                    Active Students
                  </h3>
                  <span className="text-sm font-semibold text-blue-600 bg-blue-50 px-4 py-1.5 rounded-full border border-blue-100">{activeStudents.length + (currentSession ? 1 : 0)} Online</span>
                </div>
                
                {loading ? (
                  <div className="flex justify-center py-8"><Loader2 className="animate-spin text-blue-500" /></div>
                ) : (
                  <div className="space-y-6">
                    {/* If current user is studying, show them at top */}
                    {currentSession && (
                      <div className="flex items-start justify-between">
                        <div className="flex items-start gap-4">
                          <div className="relative">
                            <img 
                              src={currentUserProfile.photoURL || `https://ui-avatars.com/api/?name=${currentUserProfile.name}`}
                              alt={currentUserProfile.name}
                              className="w-14 h-14 rounded-full object-cover border-2 border-white shadow-sm"
                            />
                            <div className="absolute -bottom-1 -right-1 bg-green-500 w-4 h-4 rounded-full border-2 border-white"></div>
                          </div>
                          <div>
                            <h4 className="text-lg font-bold text-gray-900 leading-tight uppercase">{currentUserProfile.name}</h4>
                            <div className="flex items-center gap-2 mt-1">
                              {currentSession.goal ? (
                                <span className="inline-flex items-center px-3 py-1 rounded-full border border-green-200 bg-white text-green-600 text-xs font-bold uppercase tracking-wide">
                                  <svg className="w-3 h-3 mr-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                  {currentSession.goal}
                                </span>
                              ) : (
                                <span className="inline-flex items-center px-3 py-1 rounded-full border border-blue-200 bg-white text-blue-600 text-xs font-bold uppercase tracking-wide">
                                  <span className="w-2 h-2 rounded-full border-2 border-blue-600 mr-1.5"></span>
                                  STUDYING
                                </span>
                              )}
                            </div>
                            <div className="flex gap-2 mt-2">
                              <span className="text-xl">🔥</span>
                              <span className="text-xl">👏</span>
                            </div>
                          </div>
                        </div>
                        <div className="flex flex-col items-end">
                          <span className="text-xl font-mono font-bold text-gray-800 tracking-wider">
                            {formatTime(elapsedSeconds)}
                          </span>
                          <div className="flex items-center gap-1.5 mt-1 text-green-600 font-bold text-xs uppercase tracking-wider">
                            <span className="w-2 h-2 rounded-full bg-green-500"></span>
                            STUDYING
                          </div>
                        </div>
                      </div>
                    )}

                    {activeStudents.map((student, idx) => (
                      <div key={student.id} className="flex items-start justify-between pt-6 border-t border-gray-50">
                        <div className="flex items-start gap-4">
                          <div className="relative">
                            <img 
                              src={student.userPhotoURL || `https://ui-avatars.com/api/?name=${student.userName}`}
                              alt={student.userName}
                              className="w-14 h-14 rounded-full object-cover border-2 border-white shadow-sm"
                            />
                            {idx === 0 ? (
                              <div className="absolute -top-2 -right-2 bg-yellow-400 text-white w-6 h-6 rounded-full flex items-center justify-center text-xs border-2 border-white shadow-sm"><svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M2 20h20v2H2zM12 2l5 8h4l-6 8H9l-6-8h4z"/></svg></div>
                            ) : (
                              <div className="absolute -top-2 -right-2 bg-gray-400 text-white w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold border-2 border-white shadow-sm">#{idx+1}</div>
                            )}
                            <div className="absolute -bottom-1 -right-1 bg-green-500 w-4 h-4 rounded-full border-2 border-white"></div>
                          </div>
                          <div>
                            <h4 className="text-lg font-bold text-gray-900 leading-tight">{student.userName}</h4>
                            <div className="flex items-center gap-2 mt-1">
                              {student.goal ? (
                                <span className="inline-flex items-center px-3 py-1 rounded-full border border-green-200 bg-white text-green-600 text-xs font-bold uppercase tracking-wide">
                                  <svg className="w-3 h-3 mr-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                  {student.goal}
                                </span>
                              ) : (
                                <span className="inline-flex items-center px-3 py-1 rounded-full border border-blue-200 bg-white text-blue-600 text-xs font-bold uppercase tracking-wide">
                                  <span className="w-2 h-2 rounded-full border-2 border-blue-600 mr-1.5"></span>
                                  STUDYING
                                </span>
                              )}
                            </div>
                            <div className="flex gap-2 mt-2">
                              <button className="text-xl hover:scale-110 transition-transform">🔥</button>
                              <button className="text-xl hover:scale-110 transition-transform">👏</button>
                            </div>
                          </div>
                        </div>
                        <div className="flex flex-col items-end">
                          <span className="text-xl font-mono font-bold text-gray-800 tracking-wider">
                            {formatTime(Math.floor((Date.now() - student.startTime) / 1000))}
                          </span>
                          <div className="flex items-center gap-1.5 mt-1 text-green-600 font-bold text-xs uppercase tracking-wider">
                            <span className="w-2 h-2 rounded-full bg-green-500"></span>
                            STUDYING
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}"""

content = content.replace(active_students_target, active_students_replacement)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
