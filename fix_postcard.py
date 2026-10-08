with open('src/components/PostCard.tsx', 'r') as f:
    content = f.read()
    
# Let's write the whole file explicitly to avoid regex mess

full_content = """import { getAvatarUrl } from '../utils';
import { useState } from 'react';
import { doc, updateDoc, arrayUnion, arrayRemove, increment, deleteDoc } from 'firebase/firestore';
import { db, auth } from '../firebase';
import { Post, UserProfile } from '../types';
import { ThumbsUp, ThumbsDown, MessageCircle, Flag, MoreVertical, Bookmark, Sparkles, X, Pin, Trash2, Edit2 } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { Comments } from './Comments';

interface Props {
  key?: string | number;
  post: Post;
  currentUser: UserProfile;
  usersMap?: Record<string, UserProfile>;
  onCommentClick?: () => void;
  isDetailView?: boolean;
}

export function PostCard({ post, currentUser, usersMap, onCommentClick, isDetailView }: Props) {
  const [showComments, setShowComments] = useState(false);
  const [showMenu, setShowMenu] = useState(false);
  const [isImageModalOpen, setIsImageModalOpen] = useState(false);
  const [activeImageIndex, setActiveImageIndex] = useState(0);

  const [isEditing, setIsEditing] = useState(false);
  const [editedContent, setEditedContent] = useState(post.content);
  const [isReporting, setIsReporting] = useState(false);
  const [reportReason, setReportReason] = useState('');
  
  const isAdmin = auth.currentUser?.email === 'aistoryimage1999@gmail.com';
  const isAuthor = currentUser.uid === post.authorId;
  const canEditOrDelete = isAuthor || isAdmin;
  const imagesToRender = post.imageUrls || (post.imageUrl ? [post.imageUrl] : []);
  
  const isLiked = post.likes?.includes(currentUser.uid);
  const isDisliked = post.dislikes?.includes(currentUser.uid);
  const authorProfile = usersMap?.[post.authorId];
  const photoURL = authorProfile?.photoURL || post.authorPhotoURL;
  const authorName = authorProfile?.name || post.authorName;

  const handleEdit = async () => {
    if (!editedContent.trim()) return;
    try {
      await updateDoc(doc(db, 'posts', post.id), { content: editedContent.trim() });
      setIsEditing(false);
      setShowMenu(false);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this post?')) return;
    try {
      await deleteDoc(doc(db, 'posts', post.id));
    } catch (err) {
      console.error(err);
    }
  };

  const handlePin = async () => {
    try {
      await updateDoc(doc(db, 'posts', post.id), { isPinned: !post.isPinned });
      setShowMenu(false);
    } catch (err) {
      console.error(err);
    }
  };

  const handleReport = async () => {
    if (!reportReason) return;
    try {
      await updateDoc(doc(db, 'posts', post.id), {
        reports: arrayUnion({ userId: currentUser.uid, reason: reportReason }),
        reportsCount: increment(1)
      });
      setIsReporting(false);
      setShowMenu(false);
      alert('Post reported successfully.');
    } catch (err) {
      console.error(err);
    }
  };

  const handleLike = () => {
    const postRef = doc(db, 'posts', post.id);
    try {
      if (isLiked) {
        updateDoc(postRef, {
          likes: arrayRemove(currentUser.uid)
        });
      } else {
        updateDoc(postRef, {
          likes: arrayUnion(currentUser.uid),
          dislikes: arrayRemove(currentUser.uid)
        });
      }
    } catch (err) {
      console.error('Error updating like:', err);
    }
  };

  const handleDislike = () => {
    const postRef = doc(db, 'posts', post.id);
    try {
      if (isDisliked) {
        updateDoc(postRef, {
          dislikes: arrayRemove(currentUser.uid)
        });
      } else {
        updateDoc(postRef, {
          dislikes: arrayUnion(currentUser.uid),
          likes: arrayRemove(currentUser.uid)
        });
      }
    } catch (err) {
      console.error('Error updating dislike:', err);
    }
  };

  return (
    <div className="bg-white border-b border-gray-200 overflow-hidden last:border-b-0">
      {/* Header */}
      <div className="p-4 flex items-start justify-between">
        <div className="flex items-center gap-3">
          <img 
            src={getAvatarUrl(photoURL, authorName)}
            alt={authorName.split(' ')[0]}
            className="w-12 h-12 rounded-full object-cover"
          />
          <div className="flex flex-col">
            <span className="font-bold text-gray-900 uppercase tracking-wide">{authorName.split(' ')[0]}</span>
            <span className="text-sm text-gray-500">{formatDistanceToNow(post.createdAt)} ago</span>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <div className="relative">
            <button 
              onClick={() => setShowMenu(!showMenu)}
              className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-colors"
            >
              <MoreVertical size={20} />
            </button>
            
            {showMenu && (
              <div className="absolute right-0 mt-1 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-1 z-10">
                {isAdmin && (
                  <button onClick={handlePin} className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2">
                    <Pin size={16} className={post.isPinned ? "fill-current" : ""} /> {post.isPinned ? 'Unpin Post' : 'Pin Post'}
                  </button>
                )}
                {canEditOrDelete && (
                  <>
                    <button onClick={() => { setIsEditing(true); setShowMenu(false); }} className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2">
                      <Edit2 size={16} /> Edit
                    </button>
                    <button onClick={handleDelete} className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 flex items-center gap-2">
                      <Trash2 size={16} /> Delete
                    </button>
                  </>
                )}
                {!isAuthor && (
                  <button onClick={() => { setIsReporting(true); setShowMenu(false); }} className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2">
                    <Flag size={16} /> Report
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="px-4 pb-3">
        {post.isPinned && (
          <div className="flex items-center gap-1 text-xs font-bold text-blue-600 mb-2 bg-blue-50 w-fit px-2 py-1 rounded-full border border-blue-100">
            <Pin size={12} className="fill-current" /> Pinned
          </div>
        )}
        {isEditing ? (
          <div className="flex flex-col gap-2">
            <textarea
              value={editedContent}
              onChange={(e) => setEditedContent(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 min-h-[100px]"
            />
            <div className="flex justify-end gap-2">
              <button onClick={() => setIsEditing(false)} className="px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100 rounded-lg">Cancel</button>
              <button onClick={handleEdit} className="px-3 py-1.5 text-sm bg-blue-600 text-white hover:bg-blue-700 rounded-lg">Save</button>
            </div>
          </div>
        ) : post.content && (
          <p className="text-gray-800 whitespace-pre-wrap break-words">{post.content}</p>
        )}
      </div>

      {imagesToRender.length > 0 && (
        <div className={`w-full max-h-[500px] overflow-hidden bg-gray-100 mb-2 cursor-pointer ${imagesToRender.length > 1 ? 'grid grid-cols-2 gap-1' : ''}`}>
          {imagesToRender.map((imgUrl, idx) => (
             <img 
              key={idx}
              src={imgUrl} 
              alt="Post image" 
              className={`w-full h-auto object-cover ${imagesToRender.length === 1 ? 'max-h-[500px] object-contain' : 'aspect-square'}`}
              loading="lazy"
              onClick={() => { setActiveImageIndex(idx); setIsImageModalOpen(true); }}
            />
          ))}
        </div>
      )}

      {isImageModalOpen && imagesToRender.length > 0 && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/90 p-4" onClick={() => setIsImageModalOpen(false)}>
          <button 
            className="absolute top-4 right-4 text-white hover:text-gray-300 transition-colors p-2"
            onClick={(e) => { e.stopPropagation(); setIsImageModalOpen(false); }}
          >
            <X size={32} />
          </button>
          
          {imagesToRender.length > 1 && activeImageIndex > 0 && (
            <button 
               className="absolute left-4 top-1/2 -translate-y-1/2 text-white bg-black/50 p-2 rounded-full hover:bg-black/70"
               onClick={(e) => { e.stopPropagation(); setActiveImageIndex(prev => prev - 1); }}
            >
               <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m15 18-6-6 6-6"/></svg>
            </button>
          )}

          <img 
            src={imagesToRender[activeImageIndex]} 
            alt="Full screen view" 
            className="max-w-full max-h-[90vh] object-contain rounded-lg"
            onClick={(e) => e.stopPropagation()}
          />
          
          {imagesToRender.length > 1 && activeImageIndex < imagesToRender.length - 1 && (
            <button 
               className="absolute right-4 top-1/2 -translate-y-1/2 text-white bg-black/50 p-2 rounded-full hover:bg-black/70"
               onClick={(e) => { e.stopPropagation(); setActiveImageIndex(prev => prev + 1); }}
            >
               <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m9 18 6-6-6-6"/></svg>
            </button>
          )}
        </div>
      )}

      {/* Actions */}
      <div className="px-4 py-2 flex items-center justify-between border-t border-gray-100">
        <div className="flex items-center gap-6">
          <button 
            onClick={handleLike}
            className={`flex items-center gap-1.5 transition-colors ${isLiked ? 'text-blue-600' : 'text-gray-500 hover:text-blue-600'}`}
          >
            <ThumbsUp size={20} className={isLiked ? 'fill-current' : ''} />
            <span className="text-sm font-medium">{post.likes?.length || 0}</span>
          </button>
          <button 
            onClick={handleDislike}
            className={`flex items-center gap-1.5 transition-colors ${isDisliked ? 'text-red-500' : 'text-gray-500 hover:text-red-500'}`}
          >
            <ThumbsDown size={20} className={isDisliked ? 'fill-current' : ''} />
            <span className="text-sm font-medium">{post.dislikes?.length || 0}</span>
          </button>
          <button 
            onClick={() => {
              if (onCommentClick) {
                onCommentClick();
              } else {
                setShowComments(!showComments);
              }
            }}
            className="flex items-center gap-1.5 text-gray-500 hover:text-blue-600 transition-colors"
          >
            <MessageCircle size={20} />
            <span className="text-sm font-medium hidden sm:inline">Comment</span>
            <span className="text-sm font-medium">({post.commentsCount || 0})</span>
          </button>
          <button className="flex items-center gap-1.5 text-indigo-600 hover:text-indigo-700 transition-colors">
            <Sparkles size={20} />
            <span className="text-sm font-medium hidden sm:inline">AI Solve</span>
          </button>
        </div>
        <button className="text-gray-400 hover:text-gray-600 transition-colors">
          <Bookmark size={20} />
        </button>
      </div>

      {/* Comments Section */}
      {(showComments || isDetailView) && (
        <Comments postId={post.id} currentUser={currentUser} usersMap={usersMap} isDetailView={isDetailView} />
      )}

      {isReporting && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
          <div className="bg-white w-full max-w-sm rounded-xl shadow-xl p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Report Post</h3>
            <select
              value={reportReason}
              onChange={(e) => setReportReason(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-lg mb-4"
            >
              <option value="">Select a reason</option>
              <option value="spam">Spam</option>
              <option value="harassment">Harassment</option>
              <option value="inappropriate">Inappropriate Content</option>
              <option value="other">Other</option>
            </select>
            <div className="flex justify-end gap-3">
              <button onClick={() => setIsReporting(false)} className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg">Cancel</button>
              <button onClick={handleReport} disabled={!reportReason} className="px-4 py-2 bg-red-600 text-white hover:bg-red-700 disabled:opacity-50 rounded-lg">Report</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
"""

with open('src/components/PostCard.tsx', 'w') as f:
    f.write(full_content)
