import re
with open('src/components/AdminPanel.tsx', 'r') as f:
    content = f.read()

content = content.replace('''import { collection, query, onSnapshot, doc, updateDoc, deleteDoc } from 'firebase/firestore';''', 
'''import { collection, query, onSnapshot, doc, updateDoc, deleteDoc, getDocs } from 'firebase/firestore';''')

content = content.replace('''    const q = query(collection(db, 'users'));
    const unsub = onSnapshot(q, (snapshot) => {
      const fetched: UserProfile[] = [];
      snapshot.forEach((doc) => fetched.push(doc.data() as UserProfile));
      setUsers(fetched);
      setLoading(false);
    }, (error) => {
      console.error("Firestore error fetching users:", error);
      setLoading(false);
    });

    return () => unsub();''', '''    const fetchUsers = async () => {
      try {
        const q = query(collection(db, 'users'));
        const snapshot = await getDocs(q);
        const fetched: UserProfile[] = [];
        snapshot.forEach((doc) => fetched.push(doc.data() as UserProfile));
        setUsers(fetched);
        setLoading(false);
      } catch (error) {
        console.error("Firestore error fetching users:", error);
        setLoading(false);
      }
    };
    fetchUsers();''')

content = content.replace('''      const q = query(collection(db, 'posts'));
      const unsub = onSnapshot(q, (snapshot) => {
        const fetched: Post[] = [];
        snapshot.forEach((doc) => {
          const post = { id: doc.id, ...doc.data() } as Post;
          if (post.reports && post.reports.length > 0) {
            fetched.push(post);
          }
        });
        setReportedPosts(fetched);
        setLoading(false);
      }, (error) => {
        console.error("Firestore error fetching reports:", error);
        setLoading(false);
      });
      return () => unsub();''', '''      const fetchReports = async () => {
        try {
          const q = query(collection(db, 'posts'));
          const snapshot = await getDocs(q);
          const fetched: Post[] = [];
          snapshot.forEach((doc) => {
            const post = { id: doc.id, ...doc.data() } as Post;
            if (post.reports && post.reports.length > 0) {
              fetched.push(post);
            }
          });
          setReportedPosts(fetched);
          setLoading(false);
        } catch (error) {
          console.error("Firestore error fetching reports:", error);
          setLoading(false);
        }
      };
      fetchReports();''')


with open('src/components/AdminPanel.tsx', 'w') as f:
    f.write(content)
