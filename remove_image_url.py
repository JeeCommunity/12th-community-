import re

with open('src/components/CreatePost.tsx', 'r') as f:
    content = f.read()

target = """          {showImageInput && (
            <div className="mt-2 flex items-center gap-2 bg-gray-50 p-2 rounded-lg border border-gray-200">
              <input
                type="url"
                value={imageUrl}
                onChange={(e) => setImageUrl(e.target.value)}
                placeholder="Paste image URL here..."
                className="flex-grow bg-transparent border-none outline-none text-sm px-2"
              />
              <button 
                onClick={() => { setImageUrl(''); setShowImageInput(false); }}
                className="text-gray-400 hover:text-gray-600 p-1"
              >
                <X size={16} />
              </button>
            </div>
          )}"""

content = content.replace(target, "")

with open('src/components/CreatePost.tsx', 'w') as f:
    f.write(content)
