#!/usr/bin/env python3
"""
Two fixes across all 11 onboarding screens:
1. Screen 9: add onclick to the "Complete" CTA → navigate to 10-text size
   Also wire "Skip voice greeting" to the same destination
2. All screens: inject a global <style> block that enforces the 420px phone frame
   and a light desktop backdrop — without touching any existing classes or markup
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

# The phone-frame CSS injected into every screen's <head>
# Uses a marker comment so we don't double-inject on re-run
FRAME_MARKER = "/* kaki-phone-frame */"
FRAME_STYLE = f"""<style id="kaki-phone-frame">
  {FRAME_MARKER}
  /* Desktop backdrop — the grey surround visible on wide monitors */
  html {{ background: #e8eaf0; }}
  /* Override any body background that would bleed outside the frame */
  body {{
    background: #e8eaf0 !important;
    display: flex !important;
    justify-content: center !important;
    align-items: flex-start !important;
    min-height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
  }}
  /* The first child div of body becomes the phone frame */
  body > div:first-of-type {{
    width: 100% !important;
    max-width: 420px !important;
    min-height: 100vh !important;
    margin: 0 auto !important;
    position: relative !important;
    box-shadow: 0 0 40px rgba(0,0,0,0.12) !important;
    box-sizing: border-box !important;
    /* Preserve the screen's own background color via inherit */
  }}
</style>"""

def patch_file(idx, folder, fname):
    path = os.path.join(BASE, folder, fname)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    original = html

    # ── 1. Inject phone-frame style (idempotent) ─────────────────────────
    if FRAME_MARKER not in html:
        # Insert just before </head>
        html = html.replace("</head>", FRAME_STYLE + "\n</head>", 1)

    # ── 2. Screen 09: fix dead "Complete" CTA button ──────────────────────
    if idx == 8:  # 09-voice message
        next_href = "../10-text size/10-text size.html"

        # Fix the primary "Complete" button — add onclick
        html = re.sub(
            r'(<button[^>]*min-h-\[60px\][^>]*)(type="button">)',
            lambda m: m.group(1) + f'onclick="location.href=\'{next_href}\'" ' + m.group(2),
            html,
            count=1
        )

        # Also fix the "Skip voice greeting for now" button
        html = re.sub(
            r'(Skip voice greeting for now.*?</button>)',
            lambda m: re.sub(
                r'(<button[^>]*underline[^>]*)(type="button">)',
                lambda n: n.group(1) + f'onclick="location.href=\'{next_href}\'" ' + n.group(2),
                m.group(0)
            ),
            html,
            count=1,
            flags=re.DOTALL
        )

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
