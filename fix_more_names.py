def process_file(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        content = content.replace("alt={currentUser.name}", "alt={currentUser.name.split(' ')[0]}")
        content = content.replace("{currentUser.name}", "{currentUser.name.split(' ')[0]}")
        
        with open(filepath, 'w') as f:
            f.write(content)
    except FileNotFoundError:
        pass

process_file('src/components/CreatePost.tsx')
process_file('src/App.tsx')
