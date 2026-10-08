import re

with open('src/components/CreatePost.tsx', 'r') as f:
    content = f.read()

# Add new icons
content = content.replace(
    "import { Image as ImageIcon, X } from 'lucide-react';",
    "import { Image as ImageIcon, X, Paperclip, File, FileText } from 'lucide-react';"
)

# Add new state variables
state_vars_old = """  const [imageUrl, setImageUrl] = useState('');
  const [showImageInput, setShowImageInput] = useState(false);"""

state_vars_new = """  const [imageUrl, setImageUrl] = useState('');
  const [showImageInput, setShowImageInput] = useState(false);
  const [selectedFile, setSelectedFile] = useState<{name: string, type: string, data: string} | null>(null);
  const [isUploading, setIsUploading] = useState(false);"""

content = content.replace(state_vars_old, state_vars_new)

# Add file handler
file_handler = """  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.size > 800 * 1024) {
      alert("File is too large! Maximum size is 800KB due to database limits.");
      return;
    }

    const reader = new FileReader();
    reader.onloadend = () => {
      setSelectedFile({
        name: file.name,
        type: file.type,
        data: reader.result as string
      });
    };
    reader.readAsDataURL(file);
  };"""

content = content.replace("  const handlePost = async () => {", file_handler + "\n\n  const handlePost = async () => {")

# Update handlePost condition
content = content.replace(
    "if (!content.trim() && !imageUrl.trim()) return;",
    "if (!content.trim() && !imageUrl.trim() && !selectedFile) return;"
)
content = content.replace(
    "disabled={!content.trim() && !imageUrl.trim()}",
    "disabled={!content.trim() && !imageUrl.trim() && !selectedFile || isUploading}"
)

# Update postData
post_data_old = """      content: content.trim(),
      imageUrl: imageUrl.trim() || null,"""

post_data_new = """      content: content.trim(),
      imageUrl: imageUrl.trim() || null,
      fileUrl: selectedFile?.data || null,
      fileName: selectedFile?.name || null,
      fileType: selectedFile?.type || null,"""

content = content.replace(post_data_old, post_data_new)

# Update resetting state
reset_state_old = """    setContent('');
    setImageUrl('');
    setShowImageInput(false);
    if (onSuccess) onSuccess();"""

reset_state_new = """    setIsUploading(true);
    try {
      await addDoc(collection(db, 'posts'), postData);
      setContent('');
      setImageUrl('');
      setShowImageInput(false);
      setSelectedFile(null);
      if (onSuccess) onSuccess();
    } catch (err) {
      console.error('Error creating post:', err);
      alert('Failed to create post. The file might be too large.');
    } finally {
      setIsUploading(false);
    }"""

content = content.replace(reset_state_old, reset_state_new)

# Remove the try-catch for addDoc that is now handled
content = content.replace("""    try {
      await addDoc(collection(db, 'posts'), postData);
    } catch (err) {
      console.error('Error creating post:', err);
      // alert('Failed to create post. Please try again.');
    }""", "")

# Update render to show selected file and attach button
buttons_old = """      <div className="pt-4 mt-2 flex items-center justify-between">
        <button
          onClick={() => setShowImageInput(!showImageInput)}
          className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${showImageInput ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-200'}`}
        >
          <ImageIcon size={18} />
          <span className="hidden sm:inline">Add Image URL</span>
        </button>
        <button
          onClick={handlePost}"""

buttons_new = """
          {selectedFile && (
            <div className="mt-3 flex items-center justify-between p-3 bg-gray-50 rounded-xl border border-gray-200">
              <div className="flex items-center gap-3 overflow-hidden">
                <div className="w-10 h-10 bg-blue-100 text-blue-600 rounded-lg flex items-center justify-center shrink-0">
                  {selectedFile.type.startsWith('image/') ? <ImageIcon size={20} /> : <FileText size={20} />}
                </div>
                <div className="truncate">
                  <div className="text-sm font-semibold text-gray-900 truncate">{selectedFile.name}</div>
                  <div className="text-xs text-gray-500 uppercase">{selectedFile.type.split('/')[1] || 'FILE'}</div>
                </div>
              </div>
              <button 
                onClick={() => setSelectedFile(null)}
                className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-colors shrink-0"
              >
                <X size={18} />
              </button>
            </div>
          )}
        </div>
      </div>
      <div className="pt-4 mt-2 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <label className="flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium transition-colors text-gray-600 hover:bg-gray-200 cursor-pointer">
            <Paperclip size={18} />
            <span className="hidden sm:inline">Attach File</span>
            <input 
              type="file" 
              className="hidden" 
              accept="image/*,.pdf,.doc,.docx"
              onChange={handleFileSelect}
            />
          </label>
        </div>
        <button
          onClick={handlePost}"""

content = content.replace(buttons_old, buttons_new)

# Note: we need to also remove the "Add Image URL" button from the old code and replace it with just the file upload. 
# But let's check if the replacement actually worked properly. 

with open('src/components/CreatePost.tsx', 'w') as f:
    f.write(content)
