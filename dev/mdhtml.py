import markdown
import os

with open('index.md', 'r') as f:
    text = f.read()
    html = markdown.markdown(text)

with open('rendered.html', 'w') as f:
    f.write(html)
