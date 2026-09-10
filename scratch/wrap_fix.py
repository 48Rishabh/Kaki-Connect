#!/usr/bin/env python3
"""
Fix the screens where body > header: ensure kaki-phone-frame div wraps all body content.
Screens affected: 01-splash, 02-intro, 05-mobility, 07-favorite, 10-text-size
"""
import re, os

BASE = "/Users/Rishabh/Documents/Antigravity/Senior Date/01-onboarding"

# Screens where body's first real element is <header> (not <div> or <main>)
WRAP_SCREENS = [
    ("01-splash",               "01-splash.html"),
    ("02-intro name and photo", "02-intro name and photo.html"),
    ("05-mobility choice",      "05-mobility choice.html"),
    ("07-favorite activity",    "07-favorite activity.html"),
    ("10-text size",            "10-text size.html"),
]

def patch_file(folder, fname):
    path = os.path.join(BASE, folder, fname)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    original = html

    # Only act if the kaki-phone-frame class is NOT yet on a structural element
    # (it's in the style block only, not applied to a div/header/main)
    structural_uses = [line for line in html.split('\n') 
                       if 'kaki-phone-frame' in line and 
                       not line.strip().startswith('.kaki') and
                       not '<style' in line]
    
    if structural_uses:
        print(f"⏭  Already wrapped: {folder}/{fname}")
        return

    # Insert <div class="kaki-phone-frame"> right after <body ...>
    # and </div> right before </body>
    html = re.sub(
        r'(<body[^>]*>)(\s*)',
        r'\1\2<div class="kaki-phone-frame">\n',
        html,
        count=1
    )
    html = html.replace('</body>', '</div>\n</body>', 1)

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Wrapped: {folder}/{fname}")
    else:
        print(f"⚠️  No change: {folder}/{fname}")

if __name__ == "__main__":
    for folder, fname in WRAP_SCREENS:
        patch_file(folder, fname)
    print("\nDone!")
