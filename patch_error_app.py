import re
with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace('''      const unsub = onSnapshot(doc(db, 'users', user.uid), (docSnap) => {
        if (docSnap.exists()) {
          setProfile(docSnap.data() as UserProfile);
        } else {
          setProfile(null);
        }
        setLoadingAuth(false);
      }, (error) => {
        console.error("Error fetching user profile:", error);
        setProfile(null);
        setLoadingAuth(false);
      });''', '''      const unsub = onSnapshot(doc(db, 'users', user.uid), (docSnap) => {
        if (docSnap.exists()) {
          setProfile(docSnap.data() as UserProfile);
        } else {
          setProfile(null);
        }
        setLoadingAuth(false);
      }, (error) => {
        console.error("Error fetching user profile:", error);
        setProfile(null);
        setLoadingAuth(false);
      });''')

with open('src/App.tsx', 'w') as f:
    f.write(content)
