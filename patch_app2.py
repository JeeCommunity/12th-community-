import re
with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { doc, onSnapshot } from 'firebase/firestore';", "import { doc, getDoc } from 'firebase/firestore';")

content = re.sub(r'  useEffect\(\(\) => \{\n    if \(user\) \{\n      const unsub = onSnapshot\(doc\(db, \'users\', user\.uid\), \(docSnap\) => \{\n        if \(docSnap\.exists\(\)\) \{\n          setProfile\(docSnap\.data\(\) as UserProfile\);\n        \} else \{\n          setProfile\(null\);\n        \}\n        setLoadingAuth\(false\);\n      \}, \(error\) => \{\n        console\.error\("Error fetching user profile:", error\);\n        setProfile\(null\);\n        setLoadingAuth\(false\);\n      \}\);\n      return \(\) => unsub\(\);\n    \}\n  \}, \[user\]\);', '''  useEffect(() => {
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
    }
  }, [user]);''', content)

with open('src/App.tsx', 'w') as f:
    f.write(content)
