import re

with open('src/components/PostCard.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    "  const [isImageModalOpen, setIsImageModalOpen] = useState(false);",
    "  const [isImageModalOpen, setIsImageModalOpen] = useState(false);\n  const [activeImageIndex, setActiveImageIndex] = useState(0);\n  const imagesToRender = post.imageUrls || (post.imageUrl ? [post.imageUrl] : []);"
)

new_image_jsx = """      {imagesToRender.length > 0 && (
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
      )}"""

content = re.sub(
    r"      \{post\.imageUrl && \(\s*<div className=\"w-full max-h-\[500px\] overflow-hidden bg-gray-100 mb-2 cursor-pointer\" onClick=\{\(\) => setIsImageModalOpen\(true\)\}>\s*<img \s*src=\{post\.imageUrl\} \s*alt=\"Post image\" \s*className=\"w-full h-auto object-contain max-h-\[500px\]\"\s*loading=\"lazy\"\s*/>\s*</div>\s*\)\}",
    new_image_jsx,
    content
)

new_modal_jsx = """      {isImageModalOpen && imagesToRender.length > 0 && (
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
      )}"""

content = re.sub(
    r"      \{isImageModalOpen && post\.imageUrl && \(\s*<div className=\"fixed inset-0 z-\[100\] flex items-center justify-center bg-black/90 p-4\" onClick=\{\(\) => setIsImageModalOpen\(false\)\}>\s*<button \s*className=\"absolute top-4 right-4 text-white hover:text-gray-300 transition-colors p-2\"\s*onClick=\{\(e\) => \{ e\.stopPropagation\(\); setIsImageModalOpen\(false\); \}\}\s*>\s*<X size=\{32\} />\s*</button>\s*<img \s*src=\{post\.imageUrl\} \s*alt=\"Full screen view\" \s*className=\"max-w-full max-h-\[90vh\] object-contain rounded-lg\"\s*onClick=\{\(e\) => e\.stopPropagation\(\)\}\s*/>\s*</div>\s*\)\}",
    new_modal_jsx,
    content
)

with open('src/components/PostCard.tsx', 'w') as f:
    f.write(content)
