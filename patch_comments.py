import re
with open('src/components/Comments.tsx', 'r') as f:
    content = f.read()

content = content.replace('''import { collection, query, where, orderBy, onSnapshot, addDoc, updateDoc, doc, increment, deleteDoc, arrayRemove, arrayUnion } from 'firebase/firestore';''', 
'''import { collection, query, where, orderBy, onSnapshot, addDoc, updateDoc, doc, increment, deleteDoc, arrayRemove, arrayUnion, limit } from 'firebase/firestore';''')

content = content.replace('''    const q = query(
      collection(db, 'comments'),
      where('postId', '==', postId),
      orderBy('createdAt', 'asc')
    );''', '''    const q = query(
      collection(db, 'comments'),
      where('postId', '==', postId),
      orderBy('createdAt', 'asc'),
      limit(50)
    );''')

with open('src/components/Comments.tsx', 'w') as f:
    f.write(content)
