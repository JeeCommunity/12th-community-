import re

with open('src/components/ProfileSetup.tsx', 'r') as f:
    content = f.read()

new_handle_image = """  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5242880) {
        setError("Image is too large. Please select an image under 5MB.");
        return;
      }
      
      const reader = new FileReader();
      reader.onloadend = () => {
        // Compress image before saving
        const img = new Image();
        img.onload = () => {
          const canvas = document.createElement('canvas');
          const MAX_WIDTH = 256;
          const MAX_HEIGHT = 256;
          let width = img.width;
          let height = img.height;

          if (width > height) {
            if (width > MAX_WIDTH) {
              height *= MAX_WIDTH / width;
              width = MAX_WIDTH;
            }
          } else {
            if (height > MAX_HEIGHT) {
              width *= MAX_HEIGHT / height;
              height = MAX_HEIGHT;
            }
          }

          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext('2d');
          if (ctx) {
            ctx.drawImage(img, 0, 0, width, height);
            // Compress to JPEG with 0.7 quality
            const dataUrl = canvas.toDataURL('image/jpeg', 0.7);
            setPhotoURL(dataUrl);
          } else {
            setPhotoURL(reader.result as string);
          }
        };
        img.src = reader.result as string;
      };
      reader.readAsDataURL(file);
    }
  };"""

content = re.sub(
    r"  const handleImageChange = \(e: React\.ChangeEvent<HTMLInputElement>\) => \{.*?    \}\n  \};\n",
    new_handle_image + "\n",
    content,
    flags=re.DOTALL
)

with open('src/components/ProfileSetup.tsx', 'w') as f:
    f.write(content)
