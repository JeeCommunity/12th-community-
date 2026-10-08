import re
with open('src/components/CommunityFeed.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { collection, query, orderBy, onSnapshot, where } from 'firebase/firestore';", 
"import { collection, query, orderBy, onSnapshot, where, limit } from 'firebase/firestore';")

content = content.replace('''  useEffect(() => {
    const q = query(collection(db, 'posts'), orderBy('createdAt', 'desc'));
    const unsub = onSnapshot(q, (snapshot) => {''', '''  useEffect(() => {
    const q = query(collection(db, 'posts'), orderBy('createdAt', 'desc'), limit(50));
    const unsub = onSnapshot(q, (snapshot) => {''')

with open('src/components/CommunityFeed.tsx', 'w') as f:
    f.write(content)
