import re

with open('src/components/LiveStudyRoom.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    "interface Props {\n  currentUserProfile: UserProfile;\n}",
    "interface Props {\n  currentUserProfile: UserProfile;\n  usersMap?: Record<string, UserProfile>;\n}"
)

content = content.replace(
    "export function LiveStudyRoom({ currentUserProfile }: Props) {",
    "export function LiveStudyRoom({ currentUserProfile, usersMap = {} }: Props) {"
)

# Fix getAvatarUrl calls in LiveStudyRoom
content = re.sub(
    r"src=\{getAvatarUrl\(student\.userPhotoURL, student\.userName\)\}",
    r"src={getAvatarUrl(usersMap[student.userId]?.photoURL || student.userPhotoURL, usersMap[student.userId]?.name || student.userName)}",
    content
)
content = re.sub(
    r"src=\{getAvatarUrl\(p\.userPhotoURL, p\.userName\)\}",
    r"src={getAvatarUrl(usersMap[p.userId]?.photoURL || p.userPhotoURL, usersMap[p.userId]?.name || p.userName)}",
    content
)

# And fix alt attributes just in case
content = re.sub(
    r"alt=\{student\.userName\.split\(' '\)\[0\]\}",
    r"alt={(usersMap[student.userId]?.name || student.userName).split(' ')[0]}",
    content
)
content = re.sub(
    r"alt=\{p\.userName\.split\(' '\)\[0\]\}",
    r"alt={(usersMap[p.userId]?.name || p.userName).split(' ')[0]}",
    content
)
content = re.sub(
    r"\{student\.userName\.split\(' '\)\[0\]\}",
    r"{(usersMap[student.userId]?.name || student.userName).split(' ')[0]}",
    content
)
content = re.sub(
    r"\{p\.userName\.split\(' '\)\[0\]\}",
    r"{(usersMap[p.userId]?.name || p.userName).split(' ')[0]}",
    content
)



with open('src/components/LiveStudyRoom.tsx', 'w') as f:
    f.write(content)
