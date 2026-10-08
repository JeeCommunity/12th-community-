import re

with open('src/components/CommunityFeed.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    "<LiveStudyRoom currentUserProfile={currentUserProfile} />",
    "<LiveStudyRoom currentUserProfile={currentUserProfile} usersMap={usersMap} />"
)

with open('src/components/CommunityFeed.tsx', 'w') as f:
    f.write(content)
