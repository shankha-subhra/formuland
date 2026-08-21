import re

with open(r'e:\New Projects\formuland\sections\formuland-home.liquid', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'role="tabpanel"' in line:
        print(f"Line {i+1}: panel start")
    if 'class="fct__progress"' in line:
        print(f"Line {i+1}: progress start")
    if 'data-fct-panel="7"' in line:
        print(f"Line {i+1}: Panel 7 start")
