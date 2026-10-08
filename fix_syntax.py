with open('src/components/CreatePost.tsx', 'r') as f:
    content = f.read()

content = content.replace('''  };
      reader.readAsDataURL(file);
    });
  };

  const handleFileSelect''', '''  };

  const handleFileSelect''')

with open('src/components/CreatePost.tsx', 'w') as f:
    f.write(content)
