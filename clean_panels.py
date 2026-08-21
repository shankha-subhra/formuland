import re

file_path = r"e:\New Projects\formuland\sections\formuland-home.liquid"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = '</div></div><div aria-labelledby="fct-tab-template--22898945491163__collection_tabs_home_YCgw3G-1"'
# The end marker: search for `</section>` which is right before the script tag.
end_marker = '</section>\n<script>\n  (function () {\n    var root = document.getElementById(\'fct-template--22898945491163__collection_tabs_home_YCgw3G\');'

exact_start = content.find(start_marker)
if exact_start == -1:
    # Try finding just `<div aria-labelledby="fct-tab-template--22898945491163__collection_tabs_home_YCgw3G-1"`
    exact_start = content.find('<div aria-labelledby="fct-tab-template--22898945491163__collection_tabs_home_YCgw3G-1"')

# Let's find the end manually using regex, since newlines or spaces might be different
end_match = re.search(r'</section>\s*<script>\s*\(function \(\) \{\s*var root = document\.getElementById\(\'fct-template--22898945491163__collection_tabs_home_YCgw3G\'\);', content)

if exact_start != -1 and end_match:
    exact_end = end_match.start()
    
    # We want to replace everything from exact_start to exact_end with `</div>\n</div>\n`
    # BUT wait! If exact_start is at `<div aria-labelledby...`, it means `</div></div>` is BEFORE exact_start, so we don't need to add it again!
    # Wait, earlier I saw: `1012: </div></div><div aria-labelledby="fct-tab-template--22898945491163__collection_tabs_home_YCgw3G-1"`
    # So `exact_start` points to `<div aria-labelledby...` if I just search for that. 
    # And what about the `</div></div>` at the very end of the manual HTML?
    # At line 1581: `</div></div>\n</section>`
    # The `</div></div>` closes `fct__wrapper` and the `fct` section.
    # Since my dynamic code has its own `</div>`? 
    # Let's see: `fct__wrapper` starts at 949.
    # `fct__tabs` div, `fct__nav` div, and the dynamic loop.
    # The dynamic loop creates a `fct__panel` div for each tag.
    # We need `</div>` for `fct__wrapper` and nothing else before `</section>`.
    
    new_content = content[:exact_start] + "</div>\n" + content[exact_end:]
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Successfully removed manual panels from index {exact_start} to {exact_end}.")
else:
    print(f"Start found: {exact_start != -1}, End found: {bool(end_match)}")
