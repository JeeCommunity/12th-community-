import re
with open('src/components/CommunityFeed.tsx', 'r') as f:
    content = f.read()

content = content.replace('''  useEffect(() => {
    const q = query(collection(db, 'posts'), orderBy('createdAt', 'desc'), limit(20));
    const unsub = onSnapshot(q, (snapshot) => {
      const fetched: Post[] = [];
      snapshot.forEach((doc) => fetched.push({ id: doc.id, ...doc.data() } as Post));
      setPosts(fetched);
      setLoading(false);
    }, (error) => {
      console.error("Firestore error fetching posts:", error);
      setLoading(false);
    });
    return () => {
      unsub();
    };
  }, []);''', '''  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const q = query(collection(db, 'posts'), orderBy('createdAt', 'desc'), limit(20));
        const snapshot = await getDocs(q);
        const fetched: Post[] = [];
        snapshot.forEach((doc) => fetched.push({ id: doc.id, ...doc.data() } as Post));
        setPosts(fetched);
      } catch (error) {
        console.error("Firestore error fetching posts:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchPosts();
  }, []);''')

content = content.replace("import { collection, query, orderBy, where, limit, getDocs, getCountFromServer } from 'firebase/firestore';", "import { collection, query, orderBy, where, limit, getDocs, getCountFromServer, onSnapshot } from 'firebase/firestore';")

with open('src/components/CommunityFeed.tsx', 'w') as f:
    f.write(content)
