import os
import json

def get_file_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext == '.pdf':
        return 'pdf'
    elif ext in ['.doc', '.docx']:
        return 'word'
    elif ext in ['.xls', '.xlsx']:
        return 'excel'
    elif ext in ['.jpg', '.jpeg', '.png']:
        return 'image'
    return 'other'

def build_tree(root_dir):
    tree = []
    # Sort to ensure order (numbered folders appear logically)
    items = sorted(os.listdir(root_dir))
    
    for item in items:
        # Skip system/hidden files and specific site files
        if item.startswith('.'): continue
        if item.startswith('~$'): continue # Word temp files
        if item.endswith('.tmp'): continue # Temp files
        if item in ['index.html', 'docs.html', 'events.html', 'photos.html', 'css', 'js', 'img', 'README.md', 'generate_docs_data.py', 'process_media.py', 'process_photos.py', 'process_photos_v2.py', 'LICENSE']: continue
        
        path = os.path.join(root_dir, item)
        
        if os.path.isdir(path):
            node = {
                'name': item,
                'type': 'folder',
                'path': path,
                'children': build_tree(path)
            }
            # Only add folder if it has children (optional, but keeps tree clean)
            if node['children']: 
                tree.append(node)
        else:
            node = {
                'name': item,
                'type': 'file',
                'fileType': get_file_type(item),
                'path': path
            }
            tree.append(node)
            
    return tree

# Roots we specifically care about to top-level order
top_roots = [
    "1.Білім беру ұйымының жалпы сипаттамасы",
    "2.Кадрлық құрамға талдау",
    "3.Тәрбиеленушілер контингенті",
    "4.Оқу –әдістемелік жұмыс",
    "5.ПЕДАГОГТАРДЫҢ ҚҰЖЖАТТАРЫ 2025-2026",
    "6.Ақпараттық ресурстар",
    "7.Тәрбиеленушілердің білімін бағалау",
    "ӨЗІН-ӨЗІ БАҒАЛАУ",
    "Мекеме құжаттары"
]

full_tree = []

# Scan the specific roots first to maintain order
for folder_name in top_roots:
    if os.path.exists(folder_name):
        node = {
            'name': folder_name,
            'type': 'folder',
            'path': folder_name,
            'children': build_tree(folder_name)
        }
        full_tree.append(node)

# Write to JS file
js_content = f"const docsData = {json.dumps(full_tree, indent=2, ensure_ascii=False)};"

os.makedirs('js', exist_ok=True)
with open('js/docs-data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("js/docs-data.js created successfully.")
