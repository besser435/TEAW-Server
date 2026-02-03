import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# ["towny_intdf","eventwar_tokens","0","War Tokens"]
eventwar_pattern = re.compile(
    r'(\["[^"]+","eventwar_tokens",")([^"]*)(")',
)

for filename in os.listdir(CONFIG_DIR):
    path = os.path.join(CONFIG_DIR, filename)

    if not os.path.isfile(path):
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content, count = eventwar_pattern.subn(r'\g<1>0\3', content)

    if count > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {filename} ({count} replacement)")
