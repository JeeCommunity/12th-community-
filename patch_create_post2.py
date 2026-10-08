import re

with open('src/components/CreatePost.tsx', 'r') as f:
    content = f.read()

target = """        <button
          onClick={() => setShowImageInput(!showImageInput)}
          className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${showImageInput ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-200'}`}
        >
          <ImageIcon size={18} />
          <span className="hidden sm:inline">Add Image URL</span>
        </button>"""

replacement = """        <div className="flex items-center gap-2">
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
        </div>"""

content = content.replace(target, replacement)

target2 = """          {imageUrl && (
            <div className="mt-3 relative rounded-lg overflow-hidden max-h-[300px]">
              <img src={imageUrl} alt="Preview" className="w-full h-auto object-cover" onError={() => alert('Invalid image URL')} />
              <button 
                onClick={() => setImageUrl('')}
                className="absolute top-2 right-2 p-1.5 bg-black/50 hover:bg-black/70 text-white rounded-full transition-colors"
              >
                <X size={16} />
              </button>
            </div>
          )}"""

replacement2 = """          {imageUrl && (
            <div className="mt-3 relative rounded-lg overflow-hidden max-h-[300px]">
              <img src={imageUrl} alt="Preview" className="w-full h-auto object-cover" onError={() => alert('Invalid image URL')} />
              <button 
                onClick={() => setImageUrl('')}
                className="absolute top-2 right-2 p-1.5 bg-black/50 hover:bg-black/70 text-white rounded-full transition-colors"
              >
                <X size={16} />
              </button>
            </div>
          )}
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
          )}"""

content = content.replace(target2, replacement2)

with open('src/components/CreatePost.tsx', 'w') as f:
    f.write(content)
