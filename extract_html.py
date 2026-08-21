import json

with open(r'C:\Users\shank\.gemini\antigravity-ide\brain\0e9124c3-9624-4201-a34f-786032180434\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in reversed(lines):
    data = json.loads(line)
    if data.get('type') == 'USER_INPUT':
        content = data['content']
        html_start = content.find('<div id="shopify-section-header"')
        if html_start != -1:
            html_content = content[html_start:]
            end_req = html_content.find('</USER_REQUEST>')
            if end_req != -1:
                html_content = html_content[:end_req]
            
            with open('sections/formuland-header.liquid', 'w', encoding='utf-8') as out:
                out.write(html_content.strip())
            print('Successfully wrote to sections/formuland-header.liquid')
            break
