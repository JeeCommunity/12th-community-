import re
with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

content = content.replace('''    const q = query(
      collection(db, 'roomMessages'),
      where('roomId', '==', activeRoom.id),
      orderBy('createdAt', 'asc')
    );
    const unsub = onSnapshot(q, (snapshot) => {
      const msgs: RoomMessage[] = [];
      snapshot.forEach(docSnap => msgs.push({ id: docSnap.id, ...docSnap.data() } as RoomMessage));
      setRoomMessages(msgs);
    }, (error) => {''', '''    const q = query(
      collection(db, 'roomMessages'),
      where('roomId', '==', activeRoom.id),
      orderBy('createdAt', 'desc'),
      limit(50)
    );
    const unsub = onSnapshot(q, (snapshot) => {
      const msgs: RoomMessage[] = [];
      snapshot.forEach(docSnap => msgs.push({ id: docSnap.id, ...docSnap.data() } as RoomMessage));
      setRoomMessages(msgs.reverse());
    }, (error) => {''')

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
