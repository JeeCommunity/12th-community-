with open('src/components/CommunityFeed.tsx', 'r') as f:
    content = f.read()

# We need to change the root div from:
# <div className="h-full bg-gray-50 flex flex-col font-sans relative overflow-y-auto custom-scrollbar">
# to:
# <div className="h-full bg-gray-50 flex flex-col font-sans relative">
content = content.replace(
    'className="h-full bg-gray-50 flex flex-col font-sans relative overflow-y-auto custom-scrollbar"',
    'className="h-full bg-gray-50 flex flex-col font-sans relative"'
)

# And change Tabs to not be sticky:
content = content.replace(
    '<div className="bg-white border-b border-gray-200 px-4 flex items-center gap-6 sticky top-16 z-30">',
    '<div className="bg-white border-b border-gray-200 px-4 flex items-center gap-6 shrink-0">'
)

# Status Bar to not be sticky (it wasn't sticky anyway, but let's make sure it's shrink-0):
content = content.replace(
    '<div className="bg-white border-b border-gray-200 px-4 py-4 flex items-center overflow-x-auto no-scrollbar">',
    '<div className="bg-white border-b border-gray-200 px-4 py-4 flex items-center overflow-x-auto no-scrollbar shrink-0">'
)

# Change Main Content to have overflow-y-auto:
content = content.replace(
    '<main className="flex-grow w-full max-w-3xl mx-auto p-0 sm:p-4 flex flex-col pb-24">',
    '<main className="flex-grow w-full max-w-3xl mx-auto p-0 sm:p-4 flex flex-col pb-24 overflow-y-auto custom-scrollbar relative">'
)

with open('src/components/CommunityFeed.tsx', 'w') as f:
    f.write(content)
