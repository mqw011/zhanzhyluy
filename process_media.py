import os
from PIL import Image
import json
import shutil

# Paths
BASE_DIR = os.getcwd() # /home/wrld/zhzh/zhanzhyluy-site
DEST_DIR = os.path.join(BASE_DIR, 'img/gallery')
VIDEO_SRC_DIR = os.path.join(BASE_DIR, 'img/video')

# Mapping source folders to Display Categories
FOLDERS_MAP = [
    ('БАЛАБАҚША ЖАБДЫҚТАРЫ', 'Балабақша жабдықтары', 'equip'),
    ('Жан жылуы фото/ДАМЫТУ ОРТА', 'Дамыту орта', 'dev'),
    ('Жан жылуы фото/ТАБИҒАТ БҰРЫШЫ', 'Табиғат бұрышы', 'nature'),
    ('Жан жылуы фото/ҰЛТТЫҚ БҰРЫШ', 'Ұлттық бұрыш', 'national')
]

def main():
    # 1. Process Photos
    # Clean and recreate dest dir to remove stale files
    if os.path.exists(DEST_DIR):
        # Only remove files, keep the directory structure if possible or just wipe it
        # shutil.rmtree(DEST_DIR) 
        # Actually, let's just ensure it exists. Removing might kill manual additions if any.
        # But for this script, we want a clean state usually.
        # Let's trust the previous logic.
        shutil.rmtree(DEST_DIR)
    os.makedirs(DEST_DIR)

    gallery_data = {} 

    print("Starting smart gallery processing...")

    for rel_path, category_title, prefix in FOLDERS_MAP:
        source_path = os.path.join(BASE_DIR, rel_path)
        
        if not os.path.exists(source_path):
            print(f"Skipping missing folder: {rel_path}")
            continue
            
        print(f"Processing category: {category_title}...")
        gallery_data[category_title] = []
        
        count = 1
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
                            img.thumbnail((1200, 1200))
                            img.save(dest_file_path, 'WEBP', quality=80)
                            gallery_data[category_title].append(new_filename)
                            count += 1
                    except Exception as e:
                        print(f"Error converting {file}: {e}")

    # 2. Process Videos
    # We will just list them. We generally don't convert videos in this simple script 
    # unless we have ffmpeg bindings, which is complex. We'll just list filenames.
    # Assuming they are already in img/video and web-ready (mp4).
    video_list = []
    if os.path.exists(VIDEO_SRC_DIR):
        print("Processing videos...")
        for file in os.listdir(VIDEO_SRC_DIR):
            if file.lower().endswith(('.mp4', '.webm', '.mov')):
                # Just use the raw filename, we assume the user put them there
                # Or we could rename them for consistency, but let's keep it simple
                video_list.append(file)
    
    # Write Data
    js_output_path = os.path.join(BASE_DIR, 'js', 'gallery-data.js')
    with open(js_output_path, 'w', encoding='utf-8') as f:
        # We export two variables
        f.write(f"const galleryCategories = {json.dumps(gallery_data, indent=2, ensure_ascii=False)};\n")
        f.write(f"const galleryVideos = {json.dumps(video_list, indent=2, ensure_ascii=False)};")

    print(f"Done. Gallery data regenerated. Found {len(video_list)} videos.")

if __name__ == "__main__":
    main()
