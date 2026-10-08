import React, { useState, useEffect, useRef } from 'react';
import { collection, query, where, orderBy, onSnapshot, addDoc, updateDoc, doc, arrayRemove, arrayUnion, setDoc, getDoc } from 'firebase/firestore';
import { ref, uploadBytesResumable, getDownloadURL } from 'firebase/storage';
import { signOut } from 'firebase/auth';
import { db, storage, auth } from '../firebase';
import { UserProfile, ChatMessage } from '../types';
import { Send, LogOut, Loader2, Image as ImageIcon, X, Sparkles, Users } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface Props {
  userProfile: UserProfile;
}

export function GlobalChat({ userProfile }: Props) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [typingUsers, setTypingUsers] = useState<string[]>([]);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const typingTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const GLOBAL_ROOM_ID = 'global';

  useEffect(() => {
    // Initialize global room if it doesn't exist to store typing status
    const initGlobalRoom = async () => {
      const roomRef = doc(db, 'rooms', GLOBAL_ROOM_ID);
      const snap = await getDoc(roomRef);
      if (!snap.exists()) {
        await setDoc(roomRef, {
          name: 'Global Chat',
          typing: []
        });
      }
    };
    initGlobalRoom();

    // Listen to messages
    const q = query(
      collection(db, 'messages'),
      where('roomId', '==', GLOBAL_ROOM_ID),
      orderBy('createdAt', 'asc')
    );

    const unsubMessages = onSnapshot(q, (snapshot) => {
      const fetched: ChatMessage[] = [];
      snapshot.forEach(d => fetched.push({ id: d.id, ...d.data() } as ChatMessage));
      setMessages(fetched);
      setLoading(false);
      setTimeout(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    });

    // Listen to room updates (typing indicators)
    const unsubRoom = onSnapshot(doc(db, 'rooms', GLOBAL_ROOM_ID), (docSnap) => {
      if (docSnap.exists()) {
        const data = docSnap.data();
        const typing = (data.typing || []).filter((name: string) => name !== userProfile.displayName);
        setTypingUsers(typing);
      }
    });

    return () => {
      unsubMessages();
      unsubRoom();
    };
  }, [userProfile.displayName]);

  const handleTyping = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setNewMessage(e.target.value);
    
    if (e.target.value.trim() === '') {
      updateDoc(doc(db, 'rooms', GLOBAL_ROOM_ID), { typing: arrayRemove(userProfile.displayName) }).catch(console.error);
      if (typingTimeoutRef.current) clearTimeout(typingTimeoutRef.current);
      return;
    }

    updateDoc(doc(db, 'rooms', GLOBAL_ROOM_ID), { typing: arrayUnion(userProfile.displayName) }).catch(console.error);
    
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
    }
    typingTimeoutRef.current = setTimeout(() => {
      updateDoc(doc(db, 'rooms', GLOBAL_ROOM_ID), { typing: arrayRemove(userProfile.displayName) }).catch(console.error);
    }, 2000);
  };

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if ((!newMessage.trim() && !imageFile) || sending) return;
    setSending(true);

    try {
      const now = Date.now();
      let imageUrl = '';

      if (imageFile) {
        const fileRef = ref(storage, `rooms/${GLOBAL_ROOM_ID}/${now}_${imageFile.name}`);
        const uploadTask = uploadBytesResumable(fileRef, imageFile);
        
        await new Promise<void>((resolve, reject) => {
          uploadTask.on('state_changed', 
            (snapshot) => {
              const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
              setUploadProgress(progress);
            },
            (error) => reject(error),
            async () => {
              imageUrl = await getDownloadURL(uploadTask.snapshot.ref);
              resolve();
            }
          );
        });
      }

      const msgText = newMessage.trim();

      await addDoc(collection(db, 'messages'), {
        roomId: GLOBAL_ROOM_ID,
        text: msgText,
        imageUrl: imageUrl || null,
        senderId: userProfile.uid,
        senderName: userProfile.displayName,
        senderPhotoURL: userProfile.photoURL,
        createdAt: now,
        readBy: [userProfile.uid]
      });

      await updateDoc(doc(db, 'rooms', GLOBAL_ROOM_ID), {
        lastMessage: imageFile ? '📷 Image' : msgText,
        lastMessageTime: now,
        typing: arrayRemove(userProfile.displayName)
      });

      setNewMessage('');
      setImageFile(null);
      setUploadProgress(0);
      if (fileInputRef.current) fileInputRef.current.value = '';
    } catch (err) {
      console.error(err);
    } finally {
      setSending(false);
    }
  };

  const formatTime = (ts: number) => {
    return new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex flex-col h-screen bg-[#0A0A0A] text-neutral-100 max-w-5xl mx-auto border-x border-neutral-800/50 relative shadow-2xl overflow-hidden">
      <header className="px-6 py-4 border-b border-neutral-800/50 flex justify-between items-center bg-[#0A0A0A]/90 backdrop-blur-xl sticky top-0 z-20">
        <div className="flex items-center gap-4">
          <div className="relative">
            <img 
              src={userProfile.photoURL} 
              alt={userProfile.displayName} 
              className="w-10 h-10 rounded-xl object-cover bg-neutral-800 border border-neutral-700/50 shadow-lg"
            />
            <div className="absolute -bottom-1 -right-1 w-3.5 h-3.5 bg-green-500 border-2 border-[#0A0A0A] rounded-full" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white leading-tight flex items-center gap-2">
              Global Chat
              <Sparkles className="w-4 h-4 text-blue-500" />
            </h1>
            <p className="text-xs text-neutral-400 font-medium">Hello, {userProfile.displayName}</p>
          </div>
        </div>
        <button
          onClick={() => signOut(auth)}
          className="text-neutral-400 hover:text-white bg-neutral-900 hover:bg-neutral-800 border border-neutral-800 px-4 py-2 rounded-xl transition-all font-medium flex items-center gap-2 text-sm active:scale-95"
        >
          <LogOut className="w-4 h-4" />
          <span className="hidden sm:inline">Sign Out</span>
        </button>
      </header>

      <main className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6 custom-scrollbar relative">
        {loading ? (
          <div className="flex justify-center p-12">
            <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
          </div>
        ) : messages.length === 0 ? (
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex flex-col items-center justify-center h-full text-center space-y-4 opacity-50"
          >
            <div className="w-20 h-20 bg-neutral-900 border border-neutral-800 rounded-full flex items-center justify-center mb-2 shadow-2xl">
              <Users className="w-8 h-8 text-neutral-500" />
            </div>
            <h2 className="text-2xl font-bold text-white">Welcome to Global Chat</h2>
            <p className="text-sm max-w-sm text-neutral-400">Say hello to the community! Messages are real-time and visible to everyone here.</p>
          </motion.div>
        ) : (
          <div className="space-y-6 pb-4">
            <AnimatePresence initial={false}>
              {messages.map((msg, index) => {
                const isMe = msg.senderId === userProfile.uid;
                const showAvatar = index === 0 || messages[index - 1].senderId !== msg.senderId;
                
                return (
                  <motion.div 
                    initial={{ opacity: 0, y: 10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    key={msg.id} 
                    className={`flex ${isMe ? 'justify-end' : 'justify-start'} ${showAvatar ? 'mt-6' : 'mt-1'}`}
                  >
                    <div className={`flex gap-3 max-w-[85%] sm:max-w-[75%] ${isMe ? 'flex-row-reverse' : 'flex-row'}`}>
                      {showAvatar ? (
                        <div className="relative flex-shrink-0 mt-auto mb-1">
                          <img 
                            src={msg.senderPhotoURL} 
                            alt={msg.senderName} 
                            className="w-8 h-8 rounded-full object-cover bg-neutral-800 border border-neutral-700"
                          />
                        </div>
                      ) : (
                        <div className="w-8 flex-shrink-0" />
                      )}
                      
                      <div className={`flex flex-col ${isMe ? 'items-end' : 'items-start'}`}>
                        {showAvatar && (
                          <span className="text-xs font-semibold text-neutral-400 mb-1 ml-1 mr-1">
                            {isMe ? 'You' : msg.senderName}
                          </span>
                        )}
                        <div 
                          className={`group relative flex flex-col ${
                            isMe 
                              ? 'bg-blue-600 text-white rounded-2xl rounded-br-sm' 
                              : 'bg-neutral-800 text-neutral-100 rounded-2xl rounded-bl-sm border border-neutral-700/50'
                          }`}
                        >
                          {msg.imageUrl && (
                            <div className="p-1">
                              <img src={msg.imageUrl} alt="Shared attachment" className="max-w-full rounded-xl object-contain max-h-64" />
                            </div>
                          )}
                          {msg.text && (
                            <p className="px-4 py-2.5 break-words whitespace-pre-wrap leading-relaxed">
                              {msg.text}
                            </p>
                          )}
                        </div>
                        <span className="text-[10px] font-medium text-neutral-500 mt-1 mx-1 flex items-center gap-1">
                          {formatTime(msg.createdAt)}
                        </span>
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      {/* Typing Indicator */}
      <AnimatePresence>
        {typingUsers.length > 0 && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="absolute bottom-24 left-8 bg-neutral-900 border border-neutral-800 px-4 py-2 rounded-full text-xs text-neutral-400 flex items-center gap-2 shadow-xl z-30"
          >
            <div className="flex gap-1">
              <span className="w-1.5 h-1.5 bg-neutral-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
              <span className="w-1.5 h-1.5 bg-neutral-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
              <span className="w-1.5 h-1.5 bg-neutral-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
            {typingUsers.join(', ')} typing...
          </motion.div>
        )}
      </AnimatePresence>

      <footer className="p-4 bg-[#0A0A0A] border-t border-neutral-800/50 z-20">
        
        {imageFile && (
          <div className="mb-3 flex items-center gap-3 bg-neutral-900 border border-neutral-800 p-2 rounded-xl">
            <div className="w-10 h-10 bg-neutral-800 rounded-lg flex items-center justify-center flex-shrink-0">
              <ImageIcon className="w-5 h-5 text-blue-400" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-white truncate">{imageFile.name}</p>
              <p className="text-xs text-neutral-500">{(imageFile.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
            <button onClick={() => setImageFile(null)} className="p-2 text-neutral-400 hover:text-red-400 bg-neutral-800 rounded-lg">
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        <form onSubmit={handleSend} className="flex gap-2 items-end">
          <input
            type="file"
            accept="image/*"
            ref={fileInputRef}
            className="hidden"
            onChange={e => {
              if (e.target.files && e.target.files[0]) {
                setImageFile(e.target.files[0]);
              }
            }}
          />
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="p-3.5 bg-neutral-900 border border-neutral-800 text-neutral-400 hover:text-blue-400 hover:bg-neutral-800 rounded-2xl transition-all flex-shrink-0"
          >
            <ImageIcon className="w-6 h-6" />
          </button>
          
          <div className="flex-1 relative">
            <textarea
              value={newMessage}
              onChange={handleTyping}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend(e);
                }
              }}
              placeholder="Message..."
              className="w-full bg-neutral-900 border border-neutral-800 rounded-2xl px-5 py-4 text-white focus:outline-none focus:border-blue-500 transition-colors resize-none custom-scrollbar min-h-[56px] max-h-[120px]"
              rows={1}
              maxLength={2000}
            />
            {sending && uploadProgress > 0 && (
              <div className="absolute bottom-1 left-4 right-4 h-1 bg-neutral-800 rounded-full overflow-hidden">
                <div className="h-full bg-blue-500 transition-all duration-300" style={{ width: `${uploadProgress}%` }} />
              </div>
            )}
          </div>
          
          <button
            type="submit"
            disabled={(!newMessage.trim() && !imageFile) || sending}
            className="bg-blue-600 hover:bg-blue-500 text-white h-[56px] w-[56px] rounded-2xl flex items-center justify-center disabled:opacity-50 disabled:hover:bg-blue-600 transition-all flex-shrink-0 active:scale-95 shadow-lg shadow-blue-500/20"
          >
            {sending && uploadProgress === 0 ? <Loader2 className="w-6 h-6 animate-spin" /> : <Send className="w-6 h-6 ml-1" />}
          </button>
        </form>
      </footer>
    </div>
  );
}
