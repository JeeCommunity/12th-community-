import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

target = """                            <div className="flex flex-wrap items-center gap-2 mt-1">
                              {(() => {
                                const userGoals = allDailyGoals[student.userId] || [];
                                const hasActiveGoalNotInList = student.currentGoal && !userGoals.find(g => g.title === student.currentGoal);
                                
                                if (userGoals.length === 0 && !student.currentGoal) {"""

replacement = """                            <div className="flex flex-wrap items-center gap-2 mt-1">
                              {(() => {
                                const userGoals = allDailyGoals[student.userId] || [];
                                const effectiveGoal = student.currentGoal === 'Focusing on studies' ? '' : student.currentGoal;
                                const hasActiveGoalNotInList = effectiveGoal && !userGoals.find(g => g.title === effectiveGoal);
                                
                                if (userGoals.length === 0 && !effectiveGoal) {"""

content = content.replace(target, replacement)


target2 = """                                        {student.currentGoal}
                                      </span>
                                    )}
                                    {userGoals.map((g, i) => {
                                      const isActive = student.isStudying && student.currentGoal === g.title;"""

replacement2 = """                                        {effectiveGoal}
                                      </span>
                                    )}
                                    {userGoals.map((g, i) => {
                                      const isActive = student.isStudying && effectiveGoal === g.title;"""

content = content.replace(target2, replacement2)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
