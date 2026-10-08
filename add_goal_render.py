import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

target = r"\{\/\* Today's Goals Mockup \*\/\}[\s\S]*?<\/button>\n        <\/div>"

render_code = """
        {/* Today's Goals */}
        <div className="bg-white rounded-3xl p-5 shadow-sm border border-gray-100 flex flex-col transition-all">
          <div className="flex items-center justify-between cursor-pointer" onClick={() => setIsGoalsExpanded(!isGoalsExpanded)}>
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full border border-blue-200 flex items-center justify-center">
                <div className="w-4 h-4 rounded-full border-2 border-blue-500 flex items-center justify-center">
                  <div className="w-1 h-1 rounded-full bg-blue-500"></div>
                </div>
              </div>
              <span className="text-xl font-bold text-gray-800">Today's Goals</span>
              <span className="bg-blue-50 text-blue-600 font-bold px-3 py-1 rounded-full text-sm">{dailyGoals.length}</span>
            </div>
            <button className="text-gray-400 hover:text-gray-600 p-2">
              {isGoalsExpanded ? <ChevronUp size={24} /> : <ChevronDown size={24} />}
            </button>
          </div>
          
          {isGoalsExpanded && (
            <div className="mt-6 border-t border-gray-100 pt-6">
              <div className="flex items-center justify-between mb-4">
                <span className="text-gray-600 font-medium">Manage your goals for today</span>
                <button onClick={clearAllGoals} className="text-gray-400 hover:text-red-500 text-sm font-medium transition-colors">
                  Clear All
                </button>
              </div>
              
              <div className="flex gap-2 mb-6">
                <input
                  type="text"
                  placeholder="Add a study goal..."
                  value={newGoalTitle}
                  onChange={(e) => setNewGoalTitle(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleAddGoal()}
                  className="flex-grow bg-white border border-gray-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button 
                  onClick={handleAddGoal}
                  className="bg-blue-300 hover:bg-blue-400 text-blue-900 w-12 h-12 rounded-xl flex items-center justify-center transition-colors shadow-sm shrink-0"
                >
                  <Plus size={24} />
                </button>
              </div>
              
              <div className="space-y-3">
                {dailyGoals.map(goal => {
                  const isActive = currentSession?.goal === goal.title;
                  const timeSpent = (todayGoalTimes[goal.title] || 0) + (isActive ? Math.floor((now - currentSession.startTime) / 1000) : 0);
                  
                  return (
                    <div key={goal.id} className="bg-white border border-gray-100 rounded-2xl p-4 shadow-sm flex flex-col gap-3">
                      <div className="flex items-center justify-between">
                        <span className={`text-lg font-bold ${goal.status === 'completed' ? 'text-green-600 line-through' : goal.status === 'failed' ? 'text-red-500 line-through' : 'text-gray-800'}`}>
                          {goal.title}
                        </span>
                        {isActive && <span className="bg-green-100 text-green-700 text-[10px] font-black px-2 py-0.5 rounded-full uppercase tracking-wider animate-pulse">ACTIVE</span>}
                      </div>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <button 
                            onClick={() => isActive ? handleStopSession() : handleStartGoal(goal.title)}
                            disabled={!isActive && currentSession !== null}
                            className={`w-10 h-10 rounded-full flex items-center justify-center transition-colors ${isActive ? 'bg-red-100 text-red-600 hover:bg-red-200' : currentSession ? 'bg-gray-100 text-gray-400' : 'bg-blue-100 text-blue-600 hover:bg-blue-200'}`}
                          >
                            {isActive ? <Square size={16} fill="currentColor" /> : <Play size={16} fill="currentColor" className="ml-1" />}
                          </button>
                          <div className="flex flex-col">
                            <span className="text-xl font-mono font-bold text-gray-800">{formatTime(timeSpent)}</span>
                            <span className="text-xs text-gray-400 font-medium uppercase tracking-wider">{new Date(goal.createdAt).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
                          </div>
                        </div>
                        
                        <div className="flex items-center gap-2">
                          <button 
                            onClick={() => updateGoalStatus(goal.id, goal.status === 'completed' ? 'pending' : 'completed')}
                            className={`w-10 h-10 rounded-full flex items-center justify-center border transition-colors ${goal.status === 'completed' ? 'bg-green-500 text-white border-green-500' : 'bg-gray-50 text-gray-400 border-gray-200 hover:bg-gray-100 hover:text-green-500'}`}
                          >
                            <Check size={18} />
                          </button>
                          <button 
                            onClick={() => updateGoalStatus(goal.id, goal.status === 'failed' ? 'pending' : 'failed')}
                            className={`w-10 h-10 rounded-full flex items-center justify-center border transition-colors ${goal.status === 'failed' ? 'bg-red-500 text-white border-red-500' : 'bg-gray-50 text-gray-400 border-gray-200 hover:bg-gray-100 hover:text-red-500'}`}
                          >
                            <XIcon size={18} />
                          </button>
                          <button 
                            onClick={() => deleteGoal(goal.id)}
                            className="w-10 h-10 rounded-full flex items-center justify-center border border-gray-200 bg-gray-50 text-gray-400 hover:bg-red-50 hover:text-red-500 hover:border-red-200 transition-colors"
                          >
                            <Trash2 size={18} />
                          </button>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>"""

content = re.sub(target, render_code, content)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
