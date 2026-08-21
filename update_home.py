import json
import re

file_path = r"e:\New Projects\formuland\sections\formuland-home.liquid"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace tabs
tabs_start_marker = '<div aria-label="Formula brands" class="fct__tabs" role="tablist">'
tabs_end_marker = '</div><div class="fct__nav">'

if tabs_start_marker in content and tabs_end_marker in content:
    start_idx = content.find(tabs_start_marker) + len(tabs_start_marker)
    end_idx = content.find(tabs_end_marker)
    
    tabs_liquid = '''
  {% for block in section.blocks %}
    {% if block.type == 'featured_collection' %}
      <button aria-controls="fct-panel-{{ block.id }}" aria-selected="{% if forloop.first %}true{% else %}false{% endif %}" class="fct__tab" data-fct-tab="{{ forloop.index0 }}" id="fct-tab-{{ block.id }}" role="tab" type="button">{{ block.settings.title }}</button>
    {% endif %}
  {% endfor %}
'''
    content = content[:start_idx] + tabs_liquid + content[end_idx:]

# 2. Replace panels
panels_start_marker = '</div><div aria-labelledby="fct-tab-template--22898945491163__collection_tabs_home_YCgw3G-0" class="fct__panel"'
panels_end_marker = '<div aria-hidden="true" class="fct__progress">'

# Find the start of the first panel. Note: The exact string might vary due to formatting, so we use regex or look for first <div aria-labelledby... class="fct__panel"
panels_match = re.search(r'</div>\s*<div aria-labelledby="[^"]*" class="fct__panel" data-fct-panel="0"', content)
if panels_match:
    start_idx = panels_match.end() - len(panels_match.group(0)) + 6 # Keep the </div> from <div class="fct__nav">...</div>
    
    end_idx = content.find(panels_end_marker)
    
    panels_liquid = '''
{% for block in section.blocks %}
  {% if block.type == 'featured_collection' %}
    <div aria-labelledby="fct-tab-{{ block.id }}" class="fct__panel" data-fct-panel="{{ forloop.index0 }}" {% unless forloop.first %}hidden=""{% endunless %} id="fct-panel-{{ block.id }}" role="tabpanel">
      <div class="fct__slider" data-fct-slider="">
        {% assign collection = collections[block.settings.collection] %}
        {% for product in collection.products limit: 10 %}
          <a class="fct__card" href="{{ product.url }}">
            <div class="fct__card-media">
              {% if product.compare_at_price > product.price %}
                <span class="fct__badge">Sale</span>
              {% endif %}
              <img alt="{{ product.title | escape }}" height="640" loading="lazy" sizes="320px" src="{{ product.featured_image | img_url: '640x' }}" srcset="{{ product.featured_image | img_url: '320x' }} 320w, {{ product.featured_image | img_url: '640x' }} 640w" width="640"/>
            </div>
            <h3 class="fct__card-title">{{ product.title }}</h3>
            <div class="fct__card-row">
              <span class="fct__rating">
                <span class="fct__rating-stars" role="img">
                  <span style="color: #13322b;"><svg aria-hidden="true" focusable="false" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.5l2.95 6.36 6.96.66-5.24 4.63 1.53 6.82L12 17.4l-6.2 3.57 1.53-6.82-5.24-4.63 6.96-.66L12 2.5z" fill="currentColor"></path></svg></span>
                  <span style="color: #13322b;"><svg aria-hidden="true" focusable="false" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.5l2.95 6.36 6.96.66-5.24 4.63 1.53 6.82L12 17.4l-6.2 3.57 1.53-6.82-5.24-4.63 6.96-.66L12 2.5z" fill="currentColor"></path></svg></span>
                  <span style="color: #13322b;"><svg aria-hidden="true" focusable="false" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.5l2.95 6.36 6.96.66-5.24 4.63 1.53 6.82L12 17.4l-6.2 3.57 1.53-6.82-5.24-4.63 6.96-.66L12 2.5z" fill="currentColor"></path></svg></span>
                  <span style="color: #13322b;"><svg aria-hidden="true" focusable="false" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.5l2.95 6.36 6.96.66-5.24 4.63 1.53 6.82L12 17.4l-6.2 3.57 1.53-6.82-5.24-4.63 6.96-.66L12 2.5z" fill="currentColor"></path></svg></span>
                  <span style="color: #13322b;"><svg aria-hidden="true" focusable="false" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.5l2.95 6.36 6.96.66-5.24 4.63 1.53 6.82L12 17.4l-6.2 3.57 1.53-6.82-5.24-4.63 6.96-.66L12 2.5z" fill="currentColor"></path></svg></span>
                </span>
              </span>
              <span class="fct__price">
                {{ product.price | money }}
                {% if product.compare_at_price > product.price %}
                  <s>{{ product.compare_at_price | money }}</s>
                {% endif %}
              </span>
            </div>
          </a>
        {% else %}
          <p>No products found in this collection.</p>
        {% endfor %}
      </div>
    </div>
  {% endif %}
{% endfor %}
'''
    content = content[:start_idx] + panels_liquid + content[end_idx:]

# 3. Update Schema
schema_start = content.find('{% schema %}')
schema_end = content.find('{% endschema %}')

if schema_start != -1 and schema_end != -1:
    schema_json_str = content[schema_start+12:schema_end].strip()
    try:
        schema_obj = json.loads(schema_json_str)
        
        schema_obj['blocks'] = [
            {
                "type": "featured_collection",
                "name": "Collection Tab",
                "settings": [
                    {
                        "type": "text",
                        "id": "title",
                        "label": "Tab Title"
                    },
                    {
                        "type": "collection",
                        "id": "collection",
                        "label": "Collection"
                    }
                ]
            }
        ]
        
        new_schema_str = "{% schema %}\n" + json.dumps(schema_obj, indent=2) + "\n{% endschema %}"
        content = content[:schema_start] + new_schema_str + content[schema_end+13:]
    except json.JSONDecodeError as e:
        print(f"Error parsing schema JSON: {e}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Modification complete.")
