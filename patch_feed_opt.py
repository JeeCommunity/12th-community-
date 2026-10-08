import re
with open('src/components/CommunityFeed.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { collection, query, orderBy, onSnapshot, where, limit, getDocs } from 'firebase/firestore';",
"import { collection, query, orderBy, onSnapshot, where, limit, getDocs, getCountFromServer } from 'firebase/firestore';")

content = content.replace('''  useEffect(() => {
    const q = query(collection(db, 'studySessions'), where('status', '==', 'studying'));
    const unsub = onSnapshot(q, (snapshot) => {
      setActiveStudentsCount(snapshot.size);
    }, (error) => {
      console.error("Firestore quota or permission error:", error);
    });
    return () => unsub();
  }, []);''', '''  useEffect(() => {
    const fetchCount = async () => {
      try {
        const q = query(collection(db, 'studySessions'), where('status', '==', 'studying'));
        const snapshot = await getCountFromServer(q);
        setActiveStudentsCount(snapshot.data().count);
      } catch (error) {
        console.error("Firestore quota error:", error);
      }
    };
    fetchCount();
    const interval = setInterval(fetchCount, 60000);
    return () => clearInterval(interval);
  }, []);''')

content = re.sub(r'    const fetchUsers = async \(\) => \{.*?\n    fetchUsers\(\);\n', '', content, flags=re.DOTALL)

with open('src/components/CommunityFeed.tsx', 'w') as f:
    f.write(content)
