import re
with open('src/components/CommunityFeed.tsx', 'r') as f:
    content = f.read()

content = content.replace('''export function CommunityFeed({ currentUserProfile, onEditProfile }: Props) {''', '''let globalUsersCache: Record<string, UserProfile> | null = null;

export function CommunityFeed({ currentUserProfile, onEditProfile }: Props) {''')

content = content.replace('''    const fetchUsers = async () => {
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
    fetchUsers();''', '''    const fetchUsers = async () => {
      if (globalUsersCache) {
        setUsersMap(globalUsersCache);
        return;
      }
      try {
        const snapshot = await getDocs(collection(db, 'users'));
        const map: Record<string, UserProfile> = {};
        snapshot.forEach((doc) => {
          map[doc.id] = doc.data() as UserProfile;
        });
        globalUsersCache = map;
        setUsersMap(map);
      } catch (error) {
        console.error("Firestore error fetching users:", error);
      }
    };
    fetchUsers();''')

with open('src/components/CommunityFeed.tsx', 'w') as f:
    f.write(content)
