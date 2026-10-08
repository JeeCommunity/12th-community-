import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

handlers = """  const handleAddGoal = async () => {
    if (!newGoalTitle.trim()) return;
    try {
      await addDoc(collection(db, 'dailyGoals'), {
        userId: currentUserProfile.uid,
        title: newGoalTitle.trim(),
        createdAt: Date.now(),
        status: 'pending',
        timeSpent: 0
      });
      setNewGoalTitle('');
    } catch (err) {
      console.error(err);
    }
  };

  const updateGoalStatus = async (goalId: string, status: 'pending' | 'completed' | 'failed') => {
    try {
      await updateDoc(doc(db, 'dailyGoals', goalId), { status });
    } catch (err) {
      console.error(err);
    }
  };

  const deleteGoal = async (goalId: string) => {
    try {
      await deleteDoc(doc(db, 'dailyGoals', goalId));
    } catch (err) {
      console.error(err);
    }
  };

  const clearAllGoals = async () => {
    try {
      for (const goal of dailyGoals) {
        await deleteDoc(doc(db, 'dailyGoals', goal.id));
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleStartGoal = async (goalTitle: string) => {
    if (starting || currentSession) return;
    setStarting(true);
    try {
      await addDoc(collection(db, 'studySessions'), {
        userId: currentUserProfile.uid,
        userName: currentUserProfile.name,
        userPhotoURL: currentUserProfile.photoURL || '',
        startTime: Date.now(),
        status: 'studying',
        goal: goalTitle,
        roomId: activeRoom ? activeRoom.id : null,
      });
      setStudyGoal('');
    } catch (err) {
      console.error('Error starting session:', err);
    } finally {
      setStarting(false);
    }
  };
"""

content = content.replace("  const handleStartSession = async () => {", handlers + "\n  const handleStartSession = async () => {")

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
