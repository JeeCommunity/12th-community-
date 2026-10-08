with open('src/components/PostCard.tsx', 'r') as f:
    content = f.read()

# Add isDeleting state
content = content.replace("const [isReporting, setIsReporting] = useState(false);", 
"const [isReporting, setIsReporting] = useState(false);\n  const [isDeleting, setIsDeleting] = useState(false);\n  const [isToastVisible, setIsToastVisible] = useState(false);")

# Update handleDelete
content = content.replace('''  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this post?')) return;
    try {
      await deleteDoc(doc(db, 'posts', post.id));
    } catch (err) {
      console.error(err);
    }
  };''', '''  const handleDelete = async () => {
    try {
      await deleteDoc(doc(db, 'posts', post.id));
      setIsDeleting(false);
    } catch (err) {
      console.error(err);
    }
  };''')

# Update handleReport
content = content.replace('''  const handleReport = async () => {
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
  };''', '''  const handleReport = async (reason: string) => {
    try {
      await updateDoc(doc(db, 'posts', post.id), {
        reports: arrayUnion({ userId: currentUser.uid, reason }),
        reportsCount: increment(1)
      });
      setIsReporting(false);
      setShowMenu(false);
      setIsToastVisible(true);
      setTimeout(() => setIsToastVisible(false), 3000);
    } catch (err) {
      console.error(err);
    }
  };''')

# Fix delete button click to open modal
content = content.replace('''<button onClick={handleDelete} className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 flex items-center gap-2">
                      <Trash2 size={16} /> Delete
                    </button>''', '''<button onClick={() => { setIsDeleting(true); setShowMenu(false); }} className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 flex items-center gap-2">
                      <Trash2 size={16} /> Delete
                    </button>''')

# Replace select with buttons for reporting and add confirm modal
old_reporting = '''      {isReporting && (
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
      )}'''

new_reporting_and_deleting = '''      {isReporting && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm" onClick={() => setIsReporting(false)}>
          <div className="bg-white w-full max-w-sm rounded-xl shadow-xl p-6" onClick={e => e.stopPropagation()}>
            <h3 className="text-lg font-bold text-gray-900 mb-4">Report Post</h3>
            <p className="text-sm text-gray-600 mb-4">Why are you reporting this post?</p>
            <div className="flex flex-col gap-2 mb-6">
              {['Spam', 'Harassment', 'Inappropriate Content', 'Other'].map(reason => (
                <button 
                  key={reason}
                  onClick={() => handleReport(reason.toLowerCase())}
                  className="w-full text-left px-4 py-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  {reason}
                </button>
              ))}
            </div>
            <div className="flex justify-end gap-3">
              <button onClick={() => setIsReporting(false)} className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg w-full">Cancel</button>
            </div>
          </div>
        </div>
      )}

      {isDeleting && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm" onClick={() => setIsDeleting(false)}>
          <div className="bg-white w-full max-w-sm rounded-xl shadow-xl p-6" onClick={e => e.stopPropagation()}>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Delete Post</h3>
            <p className="text-gray-600 mb-6">Are you sure you want to delete this post? This action cannot be undone.</p>
            <div className="flex justify-end gap-3">
              <button onClick={() => setIsDeleting(false)} className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg">Cancel</button>
              <button onClick={handleDelete} className="px-4 py-2 bg-red-600 text-white hover:bg-red-700 rounded-lg font-medium">Delete</button>
            </div>
          </div>
        </div>
      )}

      {isToastVisible && (
        <div className="fixed bottom-4 left-1/2 -translate-x-1/2 bg-gray-900 text-white px-4 py-2 rounded-lg shadow-lg z-50 flex items-center gap-2 animate-in fade-in slide-in-from-bottom-4">
          <Flag size={16} /> Reported successfully
        </div>
      )}'''

content = content.replace(old_reporting, new_reporting_and_deleting)

with open('src/components/PostCard.tsx', 'w') as f:
    f.write(content)
