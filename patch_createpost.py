with open('src/components/CreatePost.tsx', 'r') as f:
    content = f.read()

compression_code = """
  const compressImage = (file: File): Promise<string> => {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          const canvas = document.createElement('canvas');
          let width = img.width;
          let height = img.height;
          const max_size = 1200;
          
          if (width > height) {
            if (width > max_size) {
              height *= max_size / width;
              width = max_size;
            }
          } else {
            if (height > max_size) {
              width *= max_size / height;
              height = max_size;
            }
          }
          
          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext('2d');
          if (ctx) {
            ctx.drawImage(img, 0, 0, width, height);
            resolve(canvas.toDataURL('image/jpeg', 0.7));
          } else {
            resolve(e.target?.result as string);
          }
        };
        img.src = e.target?.result as string;
      };
      reader.readAsDataURL(file);
    });
  };

  const handleImageSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = (Array.from(e.target.files || []) as File[]).slice(0, 3 - images.length);
    
    for (const file of files) {
      if (file.size > 10 * 1024 * 1024) {
        alert("Image is too large! Maximum size is 10MB.");
        continue;
      }
      const compressedData = await compressImage(file);
      setImages(prev => [...prev, { name: file.name, data: compressedData }]);
    }
  };
"""

# Replace the existing handleImageSelect
import re
content = re.sub(
    r"const handleImageSelect = \(e: React\.ChangeEvent<HTMLInputElement>\) => \{.*?\};",
    compression_code,
    content,
    flags=re.DOTALL
)

# Fix PDF size limit
content = content.replace("10 * 1024 * 1024", "700 * 1024")
content = content.replace("max 10MB", "max 700KB")
content = content.replace("Maximum size is 10MB", "Maximum size is 700KB (Storage limits)")

with open('src/components/CreatePost.tsx', 'w') as f:
    f.write(content)
