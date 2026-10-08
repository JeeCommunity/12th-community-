import re
with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { doc, onSnapshot } from 'firebase/firestore';", "import { doc, getDoc } from 'firebase/firestore';")

content = content.replace('''  useEffect(() => {
    if (user) {
      const unsub = onSnapshot(doc(db, 'users', user.uid), (docSnap) => {
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
      });
      return () => unsub();
    } else if (user === null) {
      setProfile(null);
    }
  }, [user]);''', '''  useEffect(() => {
    if (user) {
      const fetchProfile = async () => {
        try {
          const docSnap = await getDoc(doc(db, 'users', user.uid));
          if (docSnap.exists()) {
            setProfile(docSnap.data() as UserProfile);
          } else {
            setProfile(null);
          }
        } catch (error) {
          console.error("Error fetching user profile:", error);
          setProfile(null);
        } finally {
          setLoadingAuth(false);
        }
      };
      fetchProfile();
    } else if (user === null) {
      setProfile(null);
    }
  }, [user]);''')

with open('src/App.tsx', 'w') as f:
    f.write(content)
