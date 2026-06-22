import os
import re

# We will replace unsplash image urls with our catalog images.
# Exclude lines that have class="hero-bg" or class="hero-image-bg" to be safe.

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

images = [f"img/36046_page-{i:04d}.jpg" for i in range(1, 12)]
img_idx = 0

def get_next_image():
    global img_idx
    img = images[img_idx % len(images)]
    img_idx += 1
    return img

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to replace <img src="https://images.unsplash.com/..." ...>
    # but skip if it contains class="hero-bg" or class="hero-image-bg"
    # Actually, the user said "Keep the current homepage hero cover image unchanged."
    # Let's keep all hero images unchanged just in case, since they are usually background/banners,
    # and the prompt says "Replace generic stock product images".
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if '<img src="https://images.unsplash.com/' in line:
            if 'class="hero-bg"' in line or 'class="hero-image-bg"' in line:
                # Keep hero images
                new_lines.append(line)
            else:
                # Replace the unsplash URL with a catalog image
                # The src attribute could be extracted and replaced
                new_src = get_next_image()
                # Use regex to replace the src attribute value
                new_line = re.sub(r'src="https://images\.unsplash\.com/[^"]+"', f'src="{new_src}"', line)
                # also remove any style="filter: hue-rotate(...);" because it's not needed for actual catalog images
                new_line = re.sub(r'\s*style="filter:\s*hue-rotate[^"]+"', '', new_line)
                new_lines.append(new_line)
        else:
            new_lines.append(line)
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

print("Replacements completed.")
