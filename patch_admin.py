import re
with open('src/components/AdminPanel.tsx', 'r') as f:
    content = f.read()

content = content.replace('''    if (activeTab === 'reports') {
      const q = query(collection(db, 'posts'));
      const unsub = onSnapshot(q, (snapshot) => {
        const fetched: Post[] = [];
        snapshot.forEach((doc) => {
          const post = { id: doc.id, ...doc.data() } as Post;
          if (post.reports && post.reports.length > 0) {
            fetched.push(post);
          }
        });
        fetched.sort((a, b) => (b.reportsCount || 0) - (a.reportsCount || 0));
        setReportedPosts(fetched);
      });
      return () => unsub();
    }''', '''    if (activeTab === 'reports') {
      const fetchReports = async () => {
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
          fetched.sort((a, b) => (b.reportsCount || 0) - (a.reportsCount || 0));
          setReportedPosts(fetched);
        } catch (error) {
          console.error("Firestore error fetching reports:", error);
        }
      };
      fetchReports();
    }''')

content = content.replace('''  useEffect(() => {
    const q = query(collection(db, 'users'));
    const unsub = onSnapshot(q, (snapshot) => {
      const fetched: UserProfile[] = [];
      snapshot.forEach((doc) => fetched.push(doc.data() as UserProfile));
      setUsers(fetched);
      setLoading(false);
    }, (error) => {
      console.error("Firestore error fetching users:", error);
      setLoading(false);
    });
    return () => unsub();
  }, []);''', '''  useEffect(() => {
    const fetchUsers = async () => {
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
    fetchUsers();
  }, []);''')

with open('src/components/AdminPanel.tsx', 'w') as f:
    f.write(content)
