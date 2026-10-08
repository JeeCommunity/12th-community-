import re

with open('src/components/PostCard.tsx', 'r') as f:
    content = f.read()

# Imports
content = content.replace("import { db } from '../firebase';", "import { db, auth } from '../firebase';\nimport { deleteDoc } from 'firebase/firestore';")
content = content.replace("import { ThumbsUp, ThumbsDown, MessageCircle, Flag, MoreVertical, Bookmark, Sparkles, X } from 'lucide-react';", "import { ThumbsUp, ThumbsDown, MessageCircle, Flag, MoreVertical, Bookmark, Sparkles, X, Pin, Trash2, Edit2 } from 'lucide-react';")

# State
state_insert = """
  const [isEditing, setIsEditing] = useState(false);
  const [editedContent, setEditedContent] = useState(post.content);
  const [isReporting, setIsReporting] = useState(false);
  const [reportReason, setReportReason] = useState('');
  
  const isAdmin = auth.currentUser?.email === 'aistoryimage1999@gmail.com';
  const isAuthor = currentUser.uid === post.authorId;
  const canEditOrDelete = isAuthor || isAdmin;
"""
content = content.replace(
    "  const [activeImageIndex, setActiveImageIndex] = useState(0);\n",
    "  const [activeImageIndex, setActiveImageIndex] = useState(0);\n" + state_insert
)

# Handlers
handlers = """
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
"""

content = content.replace(
    "  const handleLike = () => {",
    handlers + "\n  const handleLike = () => {"
)

# Menu
menu_jsx = """
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
"""

content = re.sub(
    r"\s*<div className=\"relative\">\s*<button\s*onClick=\{\(\) => setShowMenu\(!showMenu\)\}.*?</button>\s*</div>",
    menu_jsx,
    content,
    flags=re.DOTALL
)

# Render editing or content
content_render = """
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
"""
content = re.sub(
    r"\s*\{\/\* Content \*\/\}\s*<div className=\"px-4 pb-3\">\s*\{post\.content && \(\s*<p className=\"text-gray-800 whitespace-pre-wrap break-words\">\{post\.content\}</p>\s*\)\}\s*</div>",
    content_render,
    content,
    flags=re.DOTALL
)

# Add Report Modal at the end
report_modal = """
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
"""
content = content.replace("    </div>\n  );\n}", report_modal + "    </div>\n  );\n}")

with open('src/components/PostCard.tsx', 'w') as f:
    f.write(content)
