import re

# Read the generated color ASCII art
with open('ascii_art_color_output.txt', 'r', encoding='utf-8') as f:
    ascii_art = f.read()

# Read the current README
with open('README.md', 'r', encoding='utf-8') as f:
    readme_content = f.read()

# The ASCII art is currently inside a ``` block at the top of the README.
# We want to replace it with ```ansi\n<ascii_art>\n```

# Find the first ``` block
new_readme = re.sub(
    r'```[\s\S]*?```', 
    f'```ansi\n{ascii_art.strip()}\n```', 
    readme_content, 
    count=1
)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_readme)

print("README updated with colored ASCII art!")
