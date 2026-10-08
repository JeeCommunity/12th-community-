import React, { useEffect, useState } from 'react';
import { onAuthStateChanged, User } from 'firebase/auth';
import { doc, getDoc, updateDoc, setDoc } from 'firebase/firestore';
import { auth, db } from './firebase';
import { UserProfile } from './types';
import { Login } from './components/Login';
import { GlobalChat } from './components/GlobalChat';
import { Loader2 } from 'lucide-react';

export default function App() {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loadingAuth, setLoadingAuth] = useState(true);

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, async (currentUser) => {
      setUser(currentUser);
      if (currentUser) {
        try {
          const docSnap = await getDoc(doc(db, 'users', currentUser.uid));
          if (docSnap.exists()) {
            setProfile(docSnap.data() as UserProfile);
            await updateDoc(doc(db, 'users', currentUser.uid), { isOnline: true });
          } else {
            const newProfile = {
              uid: currentUser.uid,
              displayName: currentUser.displayName || 'Anonymous',
              email: currentUser.email || '',
              photoURL: currentUser.photoURL || `https://api.dicebear.com/7.x/avataaars/svg?seed=${currentUser.uid}`,
              isOnline: true,
              lastSeen: Date.now()
            };
            
            await setDoc(doc(db, 'users', currentUser.uid), newProfile);
            setProfile(newProfile);
          }
        } catch (error) {
          console.error("Error fetching user profile:", error);
          setProfile(null);
        }
      } else {
        if (user) {
          await updateDoc(doc(db, 'users', user.uid), { isOnline: false, lastSeen: Date.now() }).catch(console.error);
        }
        setProfile(null);
      }
      setLoadingAuth(false);
    });

    return () => unsub();
  }, [user]);

  useEffect(() => {
    const handleBeforeUnload = () => {
      if (user) {
        updateDoc(doc(db, 'users', user.uid), { isOnline: false, lastSeen: Date.now() }).catch(console.error);
      }
    };
    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
  }, [user]);

  if (loadingAuth) {
    return (
      <div className="min-h-screen bg-[#0A0A0A] flex items-center justify-center">
        <Loader2 className="w-10 h-10 animate-spin text-blue-500" />
      </div>
    );
  }

  if (!user || !profile) {
    return <Login />;
  }

  return <GlobalChat userProfile={profile} />;
}
