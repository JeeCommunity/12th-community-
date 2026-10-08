import re
with open('src/components/Comments.tsx', 'r') as f:
    content = f.read()

content = re.sub(r'    const unsub = onSnapshot\(q, \(snapshot\) => \{.*?return \(\) => unsub\(\);\n  \}, \[postId\]\);', '''    const fetchComments = async () => {
      try {
        const snapshot = await getDocs(q);
        const fetched: Comment[] = [];
        snapshot.forEach((d) => fetched.push({ id: d.id, ...d.data() } as Comment));
        setComments(fetched);
      } catch (error) {
        console.error("Firestore error fetching comments:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchComments();
  }, [postId]);''', content, flags=re.DOTALL)

content = content.replace("import { collection, query, where, orderBy, onSnapshot, addDoc, updateDoc, doc, increment } from 'firebase/firestore';", "import { collection, query, where, orderBy, addDoc, updateDoc, doc, increment, getDocs } from 'firebase/firestore';")

with open('src/components/Comments.tsx', 'w') as f:
    f.write(content)
