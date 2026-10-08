with open('src/App.tsx', 'r') as f:
    content = f.read()

target = """  return (
    <div className="flex flex-col h-[100dvh] bg-gray-50">
      <div className="flex-grow overflow-hidden relative">
        {activeTab === 'community' ? (
          <CommunityFeed 
            currentUserProfile={profile} 
            onEditProfile={() => setIsEditingProfile(true)}
          />
        ) : (
          <LiveStudyRoom 
            currentUserProfile={profile}
          />
        )}
      </div>

      {/* Bottom Navigation */}
      <div className="h-[60px] flex-shrink-0 bg-white border-t border-gray-200 flex items-center justify-around z-50 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] pb-safe">
        <button
          onClick={() => setActiveTab('community')}
          className={`flex flex-col items-center justify-center w-full h-full space-y-1 transition-colors ${
            activeTab === 'community' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-900'
          }`}
        >
          <Users size={24} />
          <span className="text-[10px] font-medium">Community</span>
        </button>
        <button
          onClick={() => setActiveTab('study')}
          className={`flex flex-col items-center justify-center w-full h-full space-y-1 transition-colors ${
            activeTab === 'study' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-900'
          }`}
        >
          <BookOpen size={24} />
          <span className="text-[10px] font-medium">Live Study Room</span>
        </button>
      </div>
    </div>
  );"""

replacement = """  return (
    <div className="flex flex-col h-[100dvh] bg-gray-50">
      <div className="flex-grow overflow-hidden relative">
        <CommunityFeed 
          currentUserProfile={profile} 
          onEditProfile={() => setIsEditingProfile(true)}
        />
      </div>
    </div>
  );"""

content = content.replace(target, replacement)

with open('src/App.tsx', 'w') as f:
    f.write(content)
