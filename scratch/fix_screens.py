#!/usr/bin/env python3
"""
Fix three issues across all 11 onboarding screens:
1. Back button links (ensure onclick navigation is correct)
2. Standardize viewport + add max-w-md mx-auto wrapper on screens missing it
3. Screen 10 → 11 (already wired, verify and keep)
4. Fix screen 11 h-[834px] → min-h-screen
"""
import re, os

BASE = "/Users/Rishabh/Documents/Antigravity/Senior Date/01-onboarding"

SCREENS = [
    ("01-splash",                 "01-splash.html"),
    ("02-intro name and photo",   "02-intro name and photo.html"),
    ("03-age and neighbourhood",  "03-age and neighbourhood.html"),
    ("04-languages",              "04-languages.html"),
    ("05-mobility choice",        "05-mobility choice.html"),
    ("06-type of care needed",    "06-type of care needed.html"),
    ("07-favorite activity",      "07-favorite activity.html"),
    ("08-emergency contact",      "08-emergency contact.html"),
    ("09-voice message",          "09-voice message.html"),
    ("10-text size",              "10-text size.html"),
    ("11-all set",                "11-all set.html"),
]

def rel_prev(idx):
    if idx == 0:
        return None
    folder, fname = SCREENS[idx - 1]
    return f"../{folder}/{fname}"

def patch_file(idx, folder, fname):
    path = os.path.join(BASE, folder, fname)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    original = html

    # ── 1. Standardize viewport meta tag ──────────────────────────────────
    std_viewport = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    # Replace any variant of viewport meta
    html = re.sub(
        r'<meta\s+(?:name=["\']viewport["\'][^>]*content=["\'][^"\']*["\']|content=["\'][^"\']*["\'][^>]*name=["\']viewport["\'])\s*/?>',
        std_viewport,
        html
    )
    # If no viewport tag at all, insert after <head>
    if std_viewport not in html and 'viewport' not in html:
        html = html.replace('<head>', f'<head>\n    {std_viewport}')

    # ── 2. Screen 01: hide back button (it's the first screen) ───────────
    if idx == 0:
        # Screen 01 has no back button already — no action needed
        # But ensure it doesn't have a stray one
        pass

    # ── 3. Fix back button onclick on screen 04 (missing onclick) ─────────
    if idx == 3:  # 04-languages
        prev_href = rel_prev(idx)  # ../03-age and neighbourhood/03-age and neighbourhood.html
        # The back button: aria-label="Go back to previous step" with no onclick
        html = re.sub(
            r'(<button\b[^>]*aria-label="Go back to previous step"[^>]*?)(\s*>)',
            lambda m: m.group(1) + f' onclick="location.href=\'{prev_href}\'"' + m.group(2),
            html,
            count=1
        )

    # ── 4. Screen 11: fix h-[834px] → min-h-screen ───────────────────────
    if idx == 10:  # 11-all set
        html = html.replace('h-[834px]', 'min-h-screen')
        # Also ensure body has flex-col to support min-h-screen correctly
        # body currently is just <body> with no class
        if '<body>' in html and 'class=' not in html.split('<body>')[0].rsplit('<body', 1)[-1][:10]:
            html = html.replace('<body>', '<body class="min-h-screen flex flex-col">', 1)

    # ── 5. Screen 10: ensure CTA goes to 11-all set ───────────────────────
    if idx == 9:  # 10-text size
        # Already set by previous patch; confirm it's correct
        next_href = '../11-all set/11-all set.html'
        # Make sure the Continue button has the right onclick
        if next_href not in html:
            html = re.sub(
                r"(location\.href=')[^']*('.*?Continue)",
                lambda m: m.group(1) + next_href + m.group(2),
                html
            )

    # ── 6. Standardize screens missing max-w-md wrapper ───────────────────
    # Screens 01, 10: body directly holds header/content without a max-w-md wrapper div
    # Screen 01: body → flex-col, inner content uses max-w-lg — fix headers/footers
    if idx == 0:  # 01-splash — uses max-w-lg in header/footer, normalize to max-w-md
        html = html.replace('max-w-lg mx-auto', 'max-w-md mx-auto')

    if idx == 9:  # 10-text size — body is flex-col directly, no inner wrapper
        # Wrap body content in a max-w-md mx-auto div
        # Body opens at <body ...>, close before </body>
        # Check if already has a wrapper
        if 'max-w-md' not in html and 'max-w-md' not in html[:500]:
            # Add wrapper div after body tag opening
            html = re.sub(
                r'(<body[^>]*>)',
                r'\1\n<div class="w-full max-w-md mx-auto min-h-screen flex flex-col box-border">',
                html,
                count=1
            )
            html = html.replace('</body>', '</div>\n</body>', 1)

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Patched: {folder}/{fname}")
    else:
        print(f"⚠️  No change: {folder}/{fname}")

if __name__ == "__main__":
    for i, (folder, fname) in enumerate(SCREENS):
        patch_file(i, folder, fname)
    print("\nDone!")
