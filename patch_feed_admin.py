import re

with open('src/components/CommunityFeed.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    "import { ShareAppModal } from './ShareAppModal';",
    "import { ShareAppModal } from './ShareAppModal';\nimport { AdminPanel } from './AdminPanel';\nimport { Shield } from 'lucide-react';"
)

content = content.replace(
    "const [activeView, setActiveView] = useState<'feed' | 'study'>('feed');",
    "const [activeView, setActiveView] = useState<'feed' | 'study' | 'admin'>('feed');"
)

admin_button = """
              {auth.currentUser?.email === 'aistoryimage1999@gmail.com' && (
                <button 
                  onClick={() => {
                    setIsMenuOpen(false);
                    setActiveView('admin');
                  }}
                  className={`w-full text-left px-4 py-3 rounded-lg font-medium flex items-center gap-3 transition-colors ${activeView === 'admin' ? 'bg-red-50 text-red-700' : 'hover:bg-gray-50 text-gray-700'}`}
                >
                  <Shield size={20} className={activeView === 'admin' ? 'text-red-600' : 'text-gray-500'} />
                  Admin Panel
                </button>
              )}
              <button 
"""

content = content.replace(
    "              <button \n                onClick={() => {\n                  setIsMenuOpen(false);\n                  onEditProfile();",
    admin_button + "                onClick={() => {\n                  setIsMenuOpen(false);\n                  onEditProfile();"
)

render_block = """
      {activeView === 'admin' ? (
        <div className="flex-grow overflow-hidden relative">
          <AdminPanel onBack={() => setActiveView('feed')} />
        </div>
      ) : activeView === 'study' ? (
"""

content = content.replace(
    "      {activeView === 'study' ? (",
    render_block
)

with open('src/components/CommunityFeed.tsx', 'w') as f:
    f.write(content)
