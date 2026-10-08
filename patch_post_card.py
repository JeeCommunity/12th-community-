import re

with open('src/components/PostCard.tsx', 'r') as f:
    content = f.read()

# Add FileText and Download imports
content = content.replace(
    "import { Heart, MessageSquare, Share2, MoreVertical, Flag, Trash2, ArrowRight } from 'lucide-react';",
    "import { Heart, MessageSquare, Share2, MoreVertical, Flag, Trash2, ArrowRight, FileText, Download } from 'lucide-react';"
)

target = """      {post.imageUrl && (
        <div className="px-4 pb-3">
          <img 
            src={post.imageUrl} 
            alt="Post content" 
            className="rounded-2xl w-full max-h-[400px] object-cover border border-gray-100"
          />
        </div>
      )}"""

replacement = """      {post.imageUrl && (
        <div className="px-4 pb-3">
          <img 
            src={post.imageUrl} 
            alt="Post content" 
            className="rounded-2xl w-full max-h-[400px] object-cover border border-gray-100"
          />
        </div>
      )}
      {post.fileUrl && (
        <div className="px-4 pb-3">
          {post.fileType?.startsWith('image/') ? (
            <img 
              src={post.fileUrl} 
              alt="Attached content" 
              className="rounded-2xl w-full max-h-[400px] object-cover border border-gray-100"
            />
          ) : (
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-2xl border border-gray-200">
              <div className="flex items-center gap-3 overflow-hidden">
                <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-xl flex items-center justify-center shrink-0">
                  <FileText size={24} />
                </div>
                <div className="truncate">
                  <div className="text-sm font-semibold text-gray-900 truncate">{post.fileName || 'Attached File'}</div>
                  <div className="text-xs text-gray-500 uppercase">{(post.fileType || '').split('/')[1] || 'FILE'}</div>
                </div>
              </div>
              <a 
                href={post.fileUrl} 
                download={post.fileName || 'download'}
                className="p-2.5 bg-white text-blue-600 hover:bg-blue-50 rounded-full shadow-sm border border-gray-200 transition-colors shrink-0"
              >
                <Download size={18} />
              </a>
            </div>
          )}
        </div>
      )}"""

content = content.replace(target, replacement)

with open('src/components/PostCard.tsx', 'w') as f:
    f.write(content)
