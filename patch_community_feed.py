import re

with open('src/components/CommunityFeed.tsx', 'r') as f:
    content = f.read()

# Add Share2 import
content = content.replace("import { Menu, X, Plus, Loader2, User, LogOut, ArrowLeft, MonitorPlay, Home } from 'lucide-react';", "import { Menu, X, Plus, Loader2, User, LogOut, ArrowLeft, MonitorPlay, Home, Share2 } from 'lucide-react';")

# Add ShareAppModal import
content = content.replace("import { LiveStudyRoom } from './LiveStudyRoom';", "import { LiveStudyRoom } from './LiveStudyRoom';\nimport { ShareAppModal } from './ShareAppModal';")

# Add state
content = content.replace("  const [activeStudentsCount, setActiveStudentsCount] = useState(0);", "  const [activeStudentsCount, setActiveStudentsCount] = useState(0);\n  const [isShareModalOpen, setIsShareModalOpen] = useState(false);")

# Add Share option in menu
target_menu_item = """              <button 
                onClick={() => {
                  setIsMenuOpen(false);
                  onEditProfile();
                }}
                className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-50 font-medium text-gray-700 flex items-center gap-3 transition-colors"
              >
                <User size={20} className="text-gray-500" />
                Edit Profile
              </button>"""

replacement_menu_item = """              <button 
                onClick={() => {
                  setIsMenuOpen(false);
                  onEditProfile();
                }}
                className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-50 font-medium text-gray-700 flex items-center gap-3 transition-colors"
              >
                <User size={20} className="text-gray-500" />
                Edit Profile
              </button>
              <button 
                onClick={() => {
                  setIsMenuOpen(false);
                  setIsShareModalOpen(true);
                }}
                className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-50 font-medium text-gray-700 flex items-center gap-3 transition-colors"
              >
                <Share2 size={20} className="text-gray-500" />
                Share App
              </button>"""

content = content.replace(target_menu_item, replacement_menu_item)

# Add ShareModal render
target_render = """      {activeView === 'study' ? ("""

replacement_render = """      {isShareModalOpen && <ShareAppModal onClose={() => setIsShareModalOpen(false)} />}
      {activeView === 'study' ? ("""

content = content.replace(target_render, replacement_render)

with open('src/components/CommunityFeed.tsx', 'w') as f:
    f.write(content)
