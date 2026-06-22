const fs = require('fs');
const path = require('path');

const dir = './';
const htmlFiles = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

const images = [];
for (let i = 1; i <= 11; i++) {
    images.push(`img/36046_page-${String(i).padStart(4, '0')}.jpg`);
}

let imgIdx = 0;
function getNextImage() {
    const img = images[imgIdx % images.length];
    imgIdx++;
    return img;
}

for (const file of htmlFiles) {
    const filePath = path.join(dir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    
    const lines = content.split('\n');
    const newLines = [];
    
    for (let line of lines) {
        if (line.includes('<img src="https://images.unsplash.com/')) {
            if (line.includes('class="hero-bg"') || line.includes('class="hero-image-bg"')) {
                // Keep hero images
                newLines.push(line);
            } else {
                const newSrc = getNextImage();
                let newLine = line.replace(/src="https:\/\/images\.unsplash\.com\/[^"]+"/, `src="${newSrc}"`);
                newLine = newLine.replace(/\s*style="filter:\s*hue-rotate[^"]+"/, '');
                newLines.push(newLine);
            }
        } else {
            newLines.push(line);
        }
    }
    
    fs.writeFileSync(filePath, newLines.join('\n'), 'utf8');
}

console.log('Images replaced successfully.');
