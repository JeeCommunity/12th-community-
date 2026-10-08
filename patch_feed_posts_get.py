import re
with open('src/components/CommunityFeed.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { collection, query, orderBy, onSnapshot, where, limit, getDocs, getCountFromServer } from 'firebase/firestore';",
"import { collection, query, orderBy, where, limit, getDocs, getCountFromServer } from 'firebase/firestore';")

content = re.sub(r'    const q = query\(collection\(db, \'posts\'\), orderBy\(\'createdAt\', \'desc\'\), limit\(20\)\);\n    const unsub = onSnapshot\(q, \(snapshot\) => \{\n      const fetched: Post\[\] = \[\];\n      snapshot\.forEach\(\(doc\) => fetched\.push\(\{ id: doc\.id, \.\.\.doc\.data\(\) \} as Post\)\);\n      setPosts\(fetched\);\n      setLoading\(false\);\n    \}, \(error\) => \{\n      console\.error\("Firestore error fetching posts:", error\);\n      setLoading\(false\);\n    \}\);\n    return \(\) => unsub\(\);', '''    const fetchPosts = async () => {
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
    fetchPosts();''', content)

with open('src/components/CommunityFeed.tsx', 'w') as f:
    f.write(content)
