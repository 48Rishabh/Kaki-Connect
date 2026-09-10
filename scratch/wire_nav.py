#!/usr/bin/env python3
"""
Wire navigation, back buttons, and fix progress bars across all 11 onboarding screens.
"""
import re, os

BASE = "/Users/Rishabh/Documents/Antigravity/Senior Date/01-onboarding"

# Relative paths from each screen's folder to adjacent screens
# Each screen is at: BASE/NN-name/NN-name.html
# Navigation is file-relative, so prefix is "../" for sibling folders
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

# Progress bar widths for screens that have one (screens 2-10)
# Screen index (0-based) → width string
PROGRESS = {
    1:  "11%",   # screen 02
    2:  "22%",   # screen 03
    3:  "33%",   # screen 04
    4:  "44%",   # screen 05
    5:  "56%",   # screen 06
    6:  "67%",   # screen 07
    7:  "78%",   # screen 08
    8:  "89%",   # screen 09
    9:  "100%",  # screen 10
}

def rel_next(idx):
    """Relative href from screen idx to next screen (idx+1)."""
    if idx + 1 >= len(SCREENS):
        return "../../02-discovery/discovery.html"
    folder, fname = SCREENS[idx + 1]
    return f"../{folder}/{fname}"

def rel_prev(idx):
    """Relative href from screen idx to previous screen (idx-1)."""
    if idx == 0:
        return None
    folder, fname = SCREENS[idx - 1]
    return f"../{folder}/{fname}"

def patch_file(idx, folder, fname):
    path = os.path.join(BASE, folder, fname)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    original = html

    # ── 1. Fix progress bar width ──────────────────────────────────────────
    if idx in PROGRESS:
        # Match the inner fill div: style="width: XX%;" or style="width:XX%;"
        new_width = PROGRESS[idx]
        html = re.sub(
            r'(<div[^>]*bg-primary[^>]*h-full[^>]*style=")[^"]*(")',
            lambda m: m.group(1) + f"width: {new_width};" + m.group(2),
            html
        )
        # Also handle reversed attribute order
        html = re.sub(
            r'(style=")[^"]*("[^>]*bg-primary[^>]*h-full)',
            lambda m: m.group(1) + f"width: {new_width};" + m.group(2),
            html
        )

    next_href = rel_next(idx)
    prev_href = rel_prev(idx)

    # ── 2. Wire primary CTA button → next screen ──────────────────────────
    # Strategy: find <button> or <a> that contains the primary CTA text,
    # and convert/update its href or add onclick.
    # We'll wrap/replace with <a> tags for reliability.

    # Screen-specific CTA text patterns
    cta_texts = {
        0:  "Get Started",
        1:  "Continue",
        2:  "Continue",
        3:  "Continue",
        4:  "Continue",
        5:  "Continue",
        6:  "Continue",
        7:  "Confirm",    # "Confirm & Continue"
        8:  "Continue",   # voice message — main "Continue" button
        9:  "Continue",   # text size
        10: "Get Started", # all set
    }

    cta_text = cta_texts.get(idx, "Continue")

    # For screen 01 (splash): already an <a>, just update href
    if idx == 0:
        html = re.sub(
            r'(<a\b[^>]*(?:Get Started)[^>]*>)',
            lambda m: re.sub(r'href="[^"]*"', f'href="{next_href}"', m.group(0)) if 'href=' in m.group(0) else m.group(0).replace('<a ', f'<a href="{next_href}" '),
            html
        )
        # The anchor wraps "Get Started", so find href="#connect" or similar and replace
        html = html.replace('href="#connect"', f'href="{next_href}"')

    else:
        # For screens with <button> primary CTAs: inject onclick navigation
        # Find the primary button by looking for the full-width primary bg-primary pill that contains cta_text
        # Replace type="button" with onclick="location.href='...'" on that button

        # Pattern: large primary bg-primary rounded-full button containing the CTA text
        # We'll add onclick to the button element. Find it carefully.

        def add_onclick(m):
            btn_tag = m.group(1)
            if 'onclick' not in btn_tag:
                btn_tag = btn_tag.replace('type="button"', f'onclick="location.href=\'{next_href}\'" type="button"')
                # If no type="button", insert before the closing >
                if 'onclick' not in btn_tag:
                    btn_tag = btn_tag.rstrip('>') + f' onclick="location.href=\'{next_href}\'">'
            return btn_tag + m.group(2)

        # Screen 10 (text size) uses bg-brand-600 instead of bg-primary
        if idx == 9:
            pattern = r'(<button[^>]*bg-brand-600[^>]*>)((?:(?!<button|</button>).)*?' + re.escape(cta_text) + r')'
        elif idx == 10:
            # 11-all set: button with bg-secondary-container "Get Started"
            pattern = r'(<button[^>]*bg-secondary-container[^>]*>)((?:(?!<button|</button>).)*?' + re.escape(cta_text) + r')'
        else:
            # General: full-width bg-primary rounded-full button
            pattern = r'(<button[^>]*w-full[^>]*bg-primary[^>]*>)((?:(?!<button|</button>).)*?' + re.escape(cta_text) + r')'

        html = re.sub(pattern, add_onclick, html, count=1, flags=re.DOTALL)

        # Screen 3 (04-languages) has flex-1 instead of w-full — try alternate
        if idx == 3 and cta_text not in html.split('onclick')[1] if 'onclick' in html else True:
            pattern2 = r'(<button[^>]*flex-1[^>]*bg-primary[^>]*>)((?:(?!<button|</button>).)*?' + re.escape(cta_text) + r')'
            html = re.sub(pattern2, add_onclick, html, count=1, flags=re.DOTALL)

    # ── 3. Wire back buttons → previous screen ────────────────────────────
    if prev_href:
        def add_back_onclick(m):
            btn_tag = m.group(0)
            if 'onclick' not in btn_tag and 'href' not in btn_tag:
                btn_tag = btn_tag.replace('type="button"', f'onclick="location.href=\'{prev_href}\'" type="button"')
            return btn_tag

        # Match back buttons: aria-label="Go back" or aria-label="Go Back"
        html = re.sub(
            r'<button[^>]*aria-label="Go [Bb]ack"[^>]*>',
            add_back_onclick,
            html
        )

    # ── 4. Screen 11: wire the "See Outings"/"Get Started" button ─────────
    # Already handled above via the CTA logic (idx == 10 → next_href = discovery)

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Patched: {folder}/{fname}")
    else:
        print(f"⚠️  No change: {folder}/{fname}")

def update_root_index():
    """Ensure root index.html redirects to the first screen."""
    root = "/Users/Rishabh/Documents/Antigravity/Senior Date/index.html"
    first_folder, first_fname = SCREENS[0]
    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=01-onboarding/{first_folder}/{first_fname}">
    <title>KakiConnect Prototype</title>
</head>
<body>
    <p>Redirecting... <a href="01-onboarding/{first_folder}/{first_fname}">Click here if not redirected.</a></p>
</body>
</html>"""
    with open(root, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Root index.html → 01-onboarding/{first_folder}/{first_fname}")

if __name__ == "__main__":
    for i, (folder, fname) in enumerate(SCREENS):
        patch_file(i, folder, fname)
    update_root_index()
    print("\nDone! All screens patched.")
