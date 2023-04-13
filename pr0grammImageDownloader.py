import os
import requests


image_sources = []

def downloadImages():
    save_dir = r'C:\Users\ASUS\OneDrive\Desktop\articleInfo\pr0gramm_images'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # download and save images
    i = 0
    for img_source in image_sources:
        save_path = os.path.join(save_dir, f"image{i}.jpg")
        response = requests.get(img_source)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        i += 1