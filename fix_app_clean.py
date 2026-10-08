with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("  const [activeTab, setActiveTab] = useState<'community' | 'study'>('community');\n", "")
content = content.replace("import { LiveStudyRoom } from './components/LiveStudyRoom';\n", "")
content = content.replace("import { Loader2, Users, BookOpen } from 'lucide-react';\n", "import { Loader2 } from 'lucide-react';\n")

with open('src/App.tsx', 'w') as f:
    f.write(content)
