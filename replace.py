import re

with open('src/components/CommunityFeed.tsx', 'r') as f:
    content = f.read()

target = """      )}

      {/* Tabs */}"""

replacement = """      )}

      {activeView === 'study' ? (
        <div className="flex-grow overflow-hidden relative">
          <LiveStudyRoom currentUserProfile={currentUserProfile} />
        </div>
      ) : (
        <>
          {/* Tabs */}"""

new_content = content.replace(target, replacement)

# Add closing tag before the last </div>
last_div = new_content.rfind('</div>')
last_div = new_content.rfind('</div>', 0, last_div)
# Let's just do a regex replace for the end of the file
new_content = re.sub(r'(?s)(        </div>\n      \)}\n    </div>\n  \);\n})$', r'        </div>\n      )}\n      </>\n      )}\n    </div>\n  );\n}', new_content)

with open('src/components/CommunityFeed.tsx', 'w') as f:
    f.write(new_content)
