export interface UserProfile {
  uid: string;
  displayName: string;
  photoURL: string;
  email: string;
  isOnline?: boolean;
  lastSeen?: number;
}

export interface ChatRoom {
  id: string;
  name: string;
  createdBy: string;
  members: string[]; // max 3
  typing?: string[]; // uids of people typing
  createdAt: number;
  lastMessage?: string;
  lastMessageTime?: number;
}

export interface ChatMessage {
  id: string;
  roomId: string;
  text: string;
  imageUrl?: string;
  senderId: string;
  senderName: string;
  senderPhotoURL: string;
  createdAt: number;
  readBy?: string[]; // uids who have read it
  replyToId?: string; // id of message being replied to
  reactions?: Record<string, string[]>; // emoji: [uids]
}
