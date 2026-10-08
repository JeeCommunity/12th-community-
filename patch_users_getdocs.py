import re
with open('src/components/CommunityFeed.tsx', 'r') as f:
    content = f.read()

content = content.replace('''import { collection, query, orderBy, onSnapshot, where, limit } from 'firebase/firestore';''', 
'''import { collection, query, orderBy, onSnapshot, where, limit, getDocs } from 'firebase/firestore';''')

content = content.replace('''    const usersUnsub = onSnapshot(collection(db, 'users'), (snapshot) => {
      const map: Record<string, UserProfile> = {};
      snapshot.forEach((doc) => {
        map[doc.id] = doc.data() as UserProfile;
      });
      setUsersMap(map);
    }, (error) => {
      console.error("Firestore error fetching users:", error);
    });''', '''    const fetchUsers = async () => {
      try {
        const snapshot = await getDocs(collection(db, 'users'));
        const map: Record<string, UserProfile> = {};
        snapshot.forEach((doc) => {
          map[doc.id] = doc.data() as UserProfile;
        });
        setUsersMap(map);
      } catch (error) {
        console.error("Firestore error fetching users:", error);
      }
    };
    fetchUsers();''')

content = content.replace('''    return () => {
      unsub();
      usersUnsub();
    };''', '''    return () => {
      unsub();
    };''')

with open('src/components/CommunityFeed.tsx', 'w') as f:
    f.write(content)
