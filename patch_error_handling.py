import re
with open('src/components/CommunityFeed.tsx', 'r') as f:
    content = f.read()

content = content.replace('''    const unsub = onSnapshot(q, (snapshot) => {
      setActiveStudentsCount(snapshot.size);
    });''', '''    const unsub = onSnapshot(q, (snapshot) => {
      setActiveStudentsCount(snapshot.size);
    }, (error) => {
      console.error("Firestore quota or permission error:", error);
    });''')

content = content.replace('''    const unsub = onSnapshot(q, (snapshot) => {
      const fetched: Post[] = [];
      snapshot.forEach((doc) => fetched.push({ id: doc.id, ...doc.data() } as Post));
      setPosts(fetched);
      setLoading(false);
    });''', '''    const unsub = onSnapshot(q, (snapshot) => {
      const fetched: Post[] = [];
      snapshot.forEach((doc) => fetched.push({ id: doc.id, ...doc.data() } as Post));
      setPosts(fetched);
      setLoading(false);
    }, (error) => {
      console.error("Firestore error fetching posts:", error);
      setLoading(false);
    });''')

content = content.replace('''    const usersUnsub = onSnapshot(collection(db, 'users'), (snapshot) => {
      const map: Record<string, UserProfile> = {};
      snapshot.forEach((doc) => {
        map[doc.id] = doc.data() as UserProfile;
      });
      setUsersMap(map);
    });''', '''    const usersUnsub = onSnapshot(collection(db, 'users'), (snapshot) => {
      const map: Record<string, UserProfile> = {};
      snapshot.forEach((doc) => {
        map[doc.id] = doc.data() as UserProfile;
      });
      setUsersMap(map);
    }, (error) => {
      console.error("Firestore error fetching users:", error);
    });''')

with open('src/components/CommunityFeed.tsx', 'w') as f:
    f.write(content)
