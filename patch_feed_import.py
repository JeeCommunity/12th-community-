with open('src/components/CommunityFeed.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { collection, query, orderBy, onSnapshot } from 'firebase/firestore';", 
"import { collection, query, orderBy, onSnapshot, where } from 'firebase/firestore';")

content = content.replace('''  useEffect(() => {
    import('firebase/firestore').then(({ query, collection, where, onSnapshot }) => {
      const q = query(collection(db, 'studySessions'), where('status', '==', 'studying'));
      onSnapshot(q, (snapshot) => {
        setActiveStudentsCount(snapshot.size);
      });
    });
  }, []);''', '''  useEffect(() => {
    const q = query(collection(db, 'studySessions'), where('status', '==', 'studying'));
    const unsub = onSnapshot(q, (snapshot) => {
      setActiveStudentsCount(snapshot.size);
    });
    return () => unsub();
  }, []);''')

with open('src/components/CommunityFeed.tsx', 'w') as f:
    f.write(content)
