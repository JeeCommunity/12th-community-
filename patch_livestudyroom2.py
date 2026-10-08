import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

# Imports
content = content.replace("import { db } from '../firebase';", "import { db, auth } from '../firebase';")
content = content.replace("GripHorizontal, ChevronRight, ChevronLeft, MoreHorizontal } from 'lucide-react';", "GripHorizontal, ChevronRight, ChevronLeft, MoreHorizontal, Edit2 } from 'lucide-react';")

# State
state_insert = """
  const [editingMessageId, setEditingMessageId] = useState<string | null>(null);
  const [editingMessageContent, setEditingMessageContent] = useState('');
  const [openMessageMenuId, setOpenMessageMenuId] = useState<string | null>(null);
  
  const isAdmin = auth.currentUser?.email === 'aistoryimage1999@gmail.com';
"""
content = content.replace(
    "  const [activeRoom, setActiveRoom] = useState<StudyRoom | null>(null);",
    "  const [activeRoom, setActiveRoom] = useState<StudyRoom | null>(null);\n" + state_insert
)

# Handlers
handlers = """
  const handleEditMessage = async (msgId: string) => {
    if (!editingMessageContent.trim()) return;
    try {
      await updateDoc(doc(db, 'roomMessages', msgId), { text: editingMessageContent.trim() });
      setEditingMessageId(null);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteMessage = async (msgId: string) => {
    if (!confirm('Are you sure you want to delete this message?')) return;
    try {
      await deleteDoc(doc(db, 'roomMessages', msgId));
    } catch (err) {
      console.error(err);
    }
  };
"""
content = content.replace(
    "  const handleSendMessage = async (e: React.FormEvent) => {",
    handlers + "\n  const handleSendMessage = async (e: React.FormEvent) => {"
)

# Render
msg_render = """
                              <div key={msg.id} className={`flex flex-col ${msg.userId === currentUserProfile.uid ? 'items-end' : 'items-start'} relative group`}>
                                <div className="flex items-center gap-2 mb-0.5">
                                  <span className="text-[10px] text-gray-500 px-1">{msg.userName.split(' ')[0]}</span>
                                  {(msg.userId === currentUserProfile.uid || isAdmin) && (
                                    <div className="relative">
                                      <button onClick={() => setOpenMessageMenuId(openMessageMenuId === msg.id ? null : msg.id)} className="opacity-0 group-hover:opacity-100 transition-opacity text-gray-400 hover:text-gray-600">
                                        <MoreHorizontal size={14} />
                                      </button>
                                      {openMessageMenuId === msg.id && (
                                        <div className="absolute top-4 right-0 bg-white rounded-lg shadow-md border border-gray-100 z-10 w-24 overflow-hidden">
                                          <button onClick={() => { setEditingMessageId(msg.id); setEditingMessageContent(msg.text); setOpenMessageMenuId(null); }} className="w-full text-left px-3 py-1.5 text-[11px] hover:bg-gray-50 text-gray-700 flex items-center gap-1.5"><Edit2 size={12} /> Edit</button>
                                          <button onClick={() => { handleDeleteMessage(msg.id); setOpenMessageMenuId(null); }} className="w-full text-left px-3 py-1.5 text-[11px] hover:bg-red-50 text-red-600 flex items-center gap-1.5"><Trash2 size={12} /> Delete</button>
                                        </div>
                                      )}
                                    </div>
                                  )}
                                </div>
                                {editingMessageId === msg.id ? (
                                  <div className="flex flex-col gap-1 w-full max-w-[85%]">
                                    <textarea
                                      value={editingMessageContent}
                                      onChange={(e) => setEditingMessageContent(e.target.value)}
                                      className="w-full p-2 border border-blue-300 rounded-lg text-sm bg-white text-gray-800 resize-none min-h-[40px] focus:outline-none focus:ring-1 focus:ring-blue-400"
                                    />
                                    <div className="flex justify-end gap-1">
                                      <button onClick={() => setEditingMessageId(null)} className="px-2 py-0.5 text-[10px] bg-gray-100 rounded text-gray-600 hover:bg-gray-200">Cancel</button>
                                      <button onClick={() => handleEditMessage(msg.id)} className="px-2 py-0.5 text-[10px] bg-blue-500 rounded text-white hover:bg-blue-600">Save</button>
                                    </div>
                                  </div>
                                ) : (
                                  <div className={`px-3 py-2 rounded-2xl max-w-[85%] text-sm ${msg.userId === currentUserProfile.uid ? 'bg-blue-600 text-white rounded-br-none' : 'bg-white border border-gray-200 text-gray-800 rounded-bl-none shadow-sm'}`}>
                                    {msg.text}
                                  </div>
                                )}
                              </div>
"""

content = re.sub(
    r"\s*<div key=\{msg\.id\} className=\{\`flex flex-col \$\{msg\.userId === currentUserProfile\.uid \? 'items-end' : 'items-start'\}\`\}>\s*<span className=\"text-\[10px\] text-gray-500 mb-0\.5 px-1\">\{msg\.userName\.split\(' '\)\[0\]\}</span>\s*<div className=\{\`px-3 py-2 rounded-2xl max-w-\[85%\] text-sm \$\{msg\.userId === currentUserProfile\.uid \? 'bg-blue-600 text-white rounded-br-none' : 'bg-white border border-gray-200 text-gray-800 rounded-bl-none shadow-sm'\}\`\}>\s*\{msg\.text\}\s*</div>\s*</div>",
    msg_render,
    content,
    flags=re.DOTALL
)

with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
