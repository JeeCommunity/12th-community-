with open('src/components/CommunityFeed.tsx', 'r') as f:
    content = f.read()

# Replace the wrong ending
wrong_ending = """        </>
      )}
    </div>
  );
}"""

correct_ending = """        </div>
      )}
      </>
      )}
    </div>
  );
}"""

content = content.replace(wrong_ending, correct_ending)
with open('src/components/CommunityFeed.tsx', 'w') as f:
    f.write(content)
