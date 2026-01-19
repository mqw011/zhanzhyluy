import os
from PIL import Image
import json

# Paths
BASE_DIR = os.getcwd() # Should be /home/wrld/zhzh/zhanzhyluy-site
SOURCE_DIRS = [
    os.path.join(BASE_DIR, 'БАЛАБАҚША ЖАБДЫҚТАРЫ'),
    os.path.join(BASE_DIR, 'Жан жылуы фото')
]
DEST_DIR = os.path.join(BASE_DIR, 'img/gallery')

# Helpers
def main():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    count = 1
    processed_files = []

    print("Starting image processing...")

    for s_dir in SOURCE_DIRS:
        if not os.path.exists(s_dir):
            print(f"Directory not found: {s_dir}")
            continue

        for root, dirs, files in os.walk(s_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    src_path = os.path.join(root, file)
                    
                    # Create a simple name
                    new_filename = f"gallery-{count}.webp"
                    dest_path = os.path.join(DEST_DIR, new_filename)
                    
                    try:
                        with Image.open(src_path) as img:
                            # Convert to RGB for JPEG/WEBP
                            if img.mode in ("rgba", "p"):
                                img = img.convert("RGB")
                            
                            # Limit size for web
                            img.thumbnail((1200, 1200))
                            
                            # Save as WEBP
                            img.save(dest_path, 'WEBP', quality=80)
                            
                            processed_files.append(new_filename)
                            print(f"Converted: {file} -> {new_filename}")
                            count += 1
                    except Exception as e:
                        print(f"Failed to process {file}: {e}")

    # Output JS data file
    js_output_path = os.path.join(BASE_DIR, 'js', 'gallery-data.js')
    with open(js_output_path, 'w', encoding='utf-8') as f:
        f.write(f"const galleryImages = {json.dumps(processed_files, indent=2)};")
    
    print(f"Done. Processed {len(processed_files)} images.")
    print(f"Data saved to {js_output_path}")

if __name__ == "__main__":
    main()
