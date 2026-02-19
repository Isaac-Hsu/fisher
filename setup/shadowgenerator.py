# generates files with all fish pngs 

import os
import requests
from bs4 import BeautifulSoup
from PIL import Image

url = "https://dankmemer.lol/fishing/creatures"
outpath = "images"

overlay_path = "overlay.png" # 114x114
background_path = "background.png"  # 114x114

headers = {"User-Agent": "Mozilla/5.0"}

os.makedirs(outpath, exist_ok=True)

# Load static images once
overlay = Image.open(overlay_path).convert("RGBA")
background = Image.open(background_path).convert("RGBA")

img_size = 114
fish_size = 96
offset = (img_size - fish_size) // 2  # 9

# Fetch page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    page.wait_for_selector("img")
    
    html = page.content()
    browser.close()
    
soup = BeautifulSoup(html, "html.parser")


for img in soup.find_all("img"):
    src = img.get("src")
    name = img.get("alt")
    
    if not src or not name or not src.endswith(".png"):
        continue
        
    print(f"Processing {name}")
    
    creature_dir = os.path.join(outpath, name)
    os.makedirs(creature_dir, exist_ok=True)
    
    # Download image
    raw = requests.get(src).content
    if use_local:
        pulled = Image.open(os.path.join(creature_dir, "tmp.png")).convert("RGBA")
    else:
        pulled = Image.open(io.BytesIO(requests.get(src).content)).convert("RGBA")
        
    # resize fish img to 96x96
    pulled = pulled.resize((fish_size, fish_size), Image.LANCZOS)
    
    # turns fish img black 
    pixels = pulled.load()
    for y in range(fish_size):
        for x in range(fish_size):
            r, g, b, a = pixels[x, y]
            if a > 0:
                pixels[x, y] = (0, 0, 0, a)
                
    # puts layers together
    final = Image.new("RGBA", (img_size, img_size))
    final.paste(background, (0, 0), background)
    final.paste(pulled, (offset, offset), pulled)
    final.paste(overlay, (0, 0), overlay)
    
    # save result
    final.save(os.path.join(creature_dir, f"{name}.png"))

print("finished execution")
