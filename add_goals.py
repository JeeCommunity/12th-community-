import re

with open('src/types.ts', 'r') as f:
    content = f.read()

goal_type = """
export interface DailyGoal {
  id: string;
  userId: string;
  title: string;
  createdAt: number;
  status: 'pending' | 'completed' | 'failed';
  timeSpent: number;
}
"""

if "export interface DailyGoal" not in content:
    content += goal_type

with open('src/types.ts', 'w') as f:
    f.write(content)
