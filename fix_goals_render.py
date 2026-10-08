import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

target = """                            <div className="flex items-center gap-2 mt-1">
                              {student.currentGoal ? (
                                <span className="inline-flex items-center px-3 py-1 rounded-full border border-gray-200 bg-white text-gray-600 text-xs font-bold uppercase tracking-wide">
                                  <svg className="w-3 h-3 mr-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                  {student.currentGoal}
                                </span>
                              ) : (
                                <span className="inline-flex items-center px-3 py-1 rounded-full border border-gray-200 bg-gray-50 text-gray-400 text-xs font-medium italic tracking-wide">
                                  No goals set
                                </span>
                              )}
                            </div>"""

replacement = """                            <div className="flex flex-wrap items-center gap-2 mt-1">
                              {(() => {
                                const userGoals = allDailyGoals[student.userId] || [];
                                const hasActiveGoalNotInList = student.currentGoal && !userGoals.find(g => g.title === student.currentGoal);
                                
                                if (userGoals.length === 0 && !student.currentGoal) {
                                  return (
                                    <span className="inline-flex items-center px-3 py-1 rounded-full border border-gray-200 bg-gray-50 text-gray-400 text-xs font-medium italic tracking-wide">
                                      No goals set
                                    </span>
                                  );
                                }
                                
                                return (
                                  <>
                                    {hasActiveGoalNotInList && (
                                      <span className="inline-flex items-center px-3 py-1 rounded-full border border-blue-200 bg-blue-50 text-blue-700 text-xs font-bold uppercase tracking-wide shadow-sm">
                                        <svg className="w-3 h-3 mr-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                        {student.currentGoal}
                                      </span>
                                    )}
                                    {userGoals.map((g, i) => {
                                      const isActive = student.isStudying && student.currentGoal === g.title;
                                      return (
                                        <span key={i} className={`inline-flex items-center px-3 py-1 rounded-full border text-xs font-bold uppercase tracking-wide ${isActive ? 'border-blue-200 bg-blue-50 text-blue-700 shadow-sm' : g.status === 'completed' ? 'border-green-200 bg-green-50 text-green-700 line-through opacity-70' : g.status === 'failed' ? 'border-red-200 bg-red-50 text-red-700 line-through opacity-70' : 'border-gray-200 bg-white text-gray-600'}`}>
                                          {isActive ? (
                                            <div className="w-2 h-2 rounded-full bg-blue-500 mr-1.5 animate-pulse"></div>
                                          ) : (
                                            <svg className="w-3 h-3 mr-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                          )}
                                          {g.title}
                                        </span>
                                      );
                                    })}
                                  </>
                                );
                              })()}
                            </div>"""

content = content.replace(target, replacement)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
