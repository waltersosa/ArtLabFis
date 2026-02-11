import shutil
from pathlib import Path

# Copy the file with a simpler name
src = Path(r'c:\Articulo\figures\Hardware connection diagram of the proposed prototype.png.jpg')
dst = Path(r'c:\Articulo\figures\hardware_connection.jpg')

if src.exists():
    shutil.copy2(src, dst)
    print(f"✓ Copied: {src.name} -> {dst.name}")
else:
    print(f"✗ Source file not found: {src}")

# Update the template.tex file
template_path = Path(r'c:\Articulo\template.tex')
with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_ref = 'figures/Hardware connection diagram of the proposed prototype.png.jpg'
new_ref = 'figures/hardware_connection.jpg'

if old_ref in content:
    content = content.replace(old_ref, new_ref)
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Updated template.tex: {old_ref} -> {new_ref}")
else:
    print(f"✗ Old reference not found in template.tex")

print("\nDone!")
