import re
with open('src/components/AdminPanel.tsx', 'r') as f:
    content = f.read()

content = content.replace('''      const unsub = onSnapshot(q, (snapshot) => {
        const fetched: Post[] = [];
        snapshot.forEach((doc) => {
          const post = { id: doc.id, ...doc.data() } as Post;
          if (post.reports && post.reports.length > 0) {
            fetched.push(post);
          }
        });
        setReportedPosts(fetched);
        setLoading(false);
      });''', '''      const unsub = onSnapshot(q, (snapshot) => {
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
      });''')

content = content.replace('''    const unsub = onSnapshot(q, (snapshot) => {
      const fetched: UserProfile[] = [];
      snapshot.forEach((doc) => fetched.push(doc.data() as UserProfile));
      setUsers(fetched);
      setLoading(false);
    });''', '''    const unsub = onSnapshot(q, (snapshot) => {
      const fetched: UserProfile[] = [];
      snapshot.forEach((doc) => fetched.push(doc.data() as UserProfile));
      setUsers(fetched);
      setLoading(false);
    }, (error) => {
      console.error("Firestore error fetching users:", error);
      setLoading(false);
    });''')

with open('src/components/AdminPanel.tsx', 'w') as f:
    f.write(content)

with open('src/components/Comments.tsx', 'r') as f:
    content = f.read()

content = content.replace('''    const unsub = onSnapshot(q, (snapshot) => {
      const fetched: Comment[] = [];
      snapshot.forEach((d) => fetched.push({ id: d.id, ...d.data() } as Comment));
      setComments(fetched);
      setLoading(false);
    });''', '''    const unsub = onSnapshot(q, (snapshot) => {
      const fetched: Comment[] = [];
      snapshot.forEach((d) => fetched.push({ id: d.id, ...d.data() } as Comment));
      setComments(fetched);
      setLoading(false);
    }, (error) => {
      console.error("Firestore error fetching comments:", error);
      setLoading(false);
    });''')

with open('src/components/Comments.tsx', 'w') as f:
    f.write(content)
