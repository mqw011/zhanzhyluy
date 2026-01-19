import os
from PIL import Image
import json
import shutil

# Paths
BASE_DIR = os.getcwd() # /home/wrld/zhzh/zhanzhyluy-site
DEST_DIR = os.path.join(BASE_DIR, 'img/gallery')

# Mapping source folders to Display Categories
# (Source Path relative to BASE_DIR, Category Title, Filename Prefix)
FOLDERS_MAP = [
    ('БАЛАБАҚША ЖАБДЫҚТАРЫ', 'Балабақша жабдықтары', 'equip'),
    ('Жан жылуы фото/ДАМЫТУ ОРТА', 'Дамыту орта', 'dev'),
    ('Жан жылуы фото/ТАБИҒАТ БҰРЫШЫ', 'Табиғат бұрышы', 'nature'),
    ('Жан жылуы фото/ҰЛТТЫҚ БҰРЫШ', 'Ұлттық бұрыш', 'national')
]

def main():
    # Clean and recreate dest dir to remove stale files
    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)
    os.makedirs(DEST_DIR)

    gallery_data = {} # { "Category Title": ["filename1.webp", "filename2.webp"] }

    print("Starting smart gallery processing...")

    for rel_path, category_title, prefix in FOLDERS_MAP:
        source_path = os.path.join(BASE_DIR, rel_path)
        
        if not os.path.exists(source_path):
            print(f"Skipping missing folder: {rel_path}")
            continue
            
        print(f"Processing category: {category_title}...")
        gallery_data[category_title] = []
        
        count = 1
        # Walk just this directory (non-recursive usually better for this specific structure unless subfolders needed)
        # using os.walk to capture files in the specific folder
        for root, dirs, files in os.walk(source_path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    src_file_path = os.path.join(root, file)
                    
                    new_filename = f"{prefix}-{count}.webp"
                    dest_file_path = os.path.join(DEST_DIR, new_filename)
                    
                    try:
                        with Image.open(src_file_path) as img:
                            if img.mode in ("rgba", "p"):
                                img = img.convert("RGB")
                            
                            # Limit size
                            img.thumbnail((1200, 1200))
                            
                            img.save(dest_file_path, 'WEBP', quality=80)
                            
                            gallery_data[category_title].append(new_filename)
                            count += 1
                    except Exception as e:
                        print(f"Error converting {file}: {e}")
    
    # Write Data
    js_output_path = os.path.join(BASE_DIR, 'js', 'gallery-data.js')
    with open(js_output_path, 'w', encoding='utf-8') as f:
        f.write(f"const galleryCategories = {json.dumps(gallery_data, indent=2, ensure_ascii=False)};")

    print("Done. Gallery data regenerated.")

if __name__ == "__main__":
    main()
