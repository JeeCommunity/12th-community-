import re

with open('src/firebase.ts', 'r') as f:
    content = f.read()

content = content.replace(
    "import { getFirestore } from 'firebase/firestore';",
    "import { getFirestore } from 'firebase/firestore';\nimport { getStorage } from 'firebase/storage';"
)

content += "\nexport const storage = getStorage(app);\n"

with open('src/firebase.ts', 'w') as f:
    f.write(content)
