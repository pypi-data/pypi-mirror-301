import os
import requests
from urllib.parse import urlparse
from markdown import markdown
from bs4 import BeautifulSoup
from PIL import Image

def download_image(url, output_dir):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.basename(urlparse(url).path)
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return filepath
    return None

def convert_to_bw(image_path):
    with Image.open(image_path) as img:
        bw_img = img.convert('L')
        bw_img.save(image_path)

def resize_image(image_path, max_size):
    with Image.open(image_path) as img:
        img.thumbnail(max_size)
        img.save(image_path)

def process_images(content, output_dir, convert_bw=False, max_size=None):
    html = markdown(content)
    soup = BeautifulSoup(html, 'html.parser')
    
    img_tags = soup.find_all('img')
    
    for img in img_tags:
        src = img.get('src')
        if src and src.startswith(('http://', 'https://')):
            img_dir = os.path.join(output_dir, f"img-{os.path.splitext(os.path.basename(output_dir))[0]}")
            os.makedirs(img_dir, exist_ok=True)
            
            local_path = download_image(src, img_dir)
            if local_path:
                if convert_bw:
                    convert_to_bw(local_path)
                if max_size:
                    resize_image(local_path, max_size)
                
                relative_path = os.path.relpath(local_path, output_dir)
                content = content.replace(f']({src})', f']({relative_path})')
                content += f"\n\n<!-- Original image source: {src} -->\n"
    
    return content

def process_markdown_file(input_file, output_dir, convert_bw=False, max_size=None):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    processed_content = process_images(content, output_dir, convert_bw, max_size)
    
    output_file = os.path.join(output_dir, os.path.basename(input_file))
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(processed_content)
    
    return output_file