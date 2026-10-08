import re
with open('src/components/CommunityFeed.tsx', 'r') as f:
    content = f.read()

# Check if usersMap is used anywhere else that might be failing.
print(re.findall(r'usersMap', content))
