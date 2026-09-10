import re
import os

BASE = "/Users/Rishabh/Documents/Antigravity/Senior Date/04-volunteer"
SCREENS = [
    "01-volunteer_1_welcome_overview",
    "02-volunteer_2_open_requests_feed",
    "03-volunteer_2_outing_details_route",
    "04-volunteer_3_match_confirmed_meeting_plan",
    "05-volunteer_4_live_outing_check_in",
    "06-volunteer_5_safety_guidelines_protocols",
]

FRAME_STYLE = """<style id="kaki-phone-frame">
  html { background: #f8fafc; }
  body {
    background: #f8fafc !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    min-height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
  }
  .kaki-phone-frame {
    width: 100% !important;
    max-width: 420px !important;
    min-height: 100vh !important;
    margin: 0 auto !important;
    position: relative !important;
    background: #ffffff !important;
    box-shadow: 0 0 40px rgba(0,0,0,0.12) !important;
    box-sizing: border-box !important;
    overflow-x: hidden !important;
  }
</style>"""

def add_phone_frame(html):
    # 1. Add viewport
    if 'name="viewport"' not in html:
        html = html.replace('<head>', '<head>\n<meta name="viewport" content="width=device-width, initial-scale=1.0">', 1)
        
    # 2. Add style block
    if '<style id="kaki-phone-frame">' not in html:
        html = html.replace('</head>', FRAME_STYLE + '\n</head>', 1)
    else:
        html = re.sub(r'<style id="kaki-phone-frame">.*?</style>', FRAME_STYLE, html, flags=re.DOTALL)
        
    # 3. Strip any max-w-screen-md or max-w-lg and replace with max-w-md
    html = re.sub(r'max-w-screen-md|max-w-lg', 'max-w-md', html)

    # 4. Apply container
    # Check if we already wrapped it via <div class="kaki-phone-frame">
    body_content_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if body_content_match:
        body_content = body_content_match.group(1)
        if 'kaki-phone-frame' not in body_content:
            # Need to wrap everything inside body
            html = re.sub(r'(<body[^>]*>)', r'\1\n<div class="kaki-phone-frame">', html, count=1)
            html = html.replace('</body>', '</div>\n</body>')
    return html

for i, folder in enumerate(SCREENS):
    path = os.path.join(BASE, folder, "code.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Apply frame styling
    html = add_phone_frame(html)

    # Specific Fixes
    if i == 0:
        # Screen 1 -> 2 button
        html = re.sub(
            r'<button class="[^"]*"[^>]*>\s*<span class="">View Open Requests[\s\S]*?</button>',
            '<button onclick="location.href=\'../02-volunteer_2_open_requests_feed/code.html\'" class="w-full bg-primary hover:bg-primary-container text-on-primary py-3.5 px-6 rounded-full font-headline-sm text-headline-sm font-semibold flex items-center justify-center gap-2 shadow-md hover:shadow-lg tactile-press transition-all duration-200"><span class="">View Open Requests (4 Nearby)</span><span class="material-symbols-outlined text-xl" data-icon="arrow_forward">arrow_forward</span></button>',
            html
        )
        # Back arrow Screen 1 -> root
        html = re.sub(r'(aria-label="Go Back"[^>]*)(>)', r'\1 onclick="location.href=\'../../index.html\'"\2', html)
        html = re.sub(r'onclick="[^"]*"\s*onclick=', 'onclick=', html) # cleanup if duplicate

    elif i == 1:
        # Back arrow Screen 2 -> Screen 1
        html = re.sub(
            r'(aria-label="Back to Overview"[^>]*?)(onclick="[^"]*")([^>]*>)',
            r'\1\3', html
        )
        html = re.sub(
            r'(aria-label="Back to Overview"[^>]*)(>)',
            r'\1 onclick="location.href=\'../01-volunteer_1_welcome_overview/code.html\'"\2', html
        )

    elif i == 2:
        # Back arrow Screen 3 -> Screen 2
        html = re.sub(
            r'(aria-label="Go Back"[^>]*?)(onclick="[^"]*")([^>]*>)',
            r'\1\3', html
        )
        html = re.sub(
            r'(aria-label="Go Back"[^>]*)(>)',
            r'\1 onclick="location.href=\'../02-volunteer_2_open_requests_feed/code.html\'"\2', html
        )

    elif i == 3:
        # Back arrow Screen 4 -> Screen 3
        html = re.sub(
            r'(aria-label="Go Back"[^>]*?)(onclick="[^"]*")([^>]*>)',
            r'\1\3', html
        )
        html = re.sub(
            r'(aria-label="Go Back"[^>]*)(>)',
            r'\1 onclick="location.href=\'../03-volunteer_2_outing_details_route/code.html\'"\2', html
        )

    elif i == 4:
        # Back arrow Screen 5 -> Screen 4
        # Wait, the back button might be aria-label="Back"
        html = re.sub(
            r'(aria-label="Back"[^>]*?)(onclick="[^"]*")([^>]*>)',
            r'\1\3', html
        )
        html = re.sub(
            r'(aria-label="Back"[^>]*)(>)',
            r'\1 onclick="location.href=\'../04-volunteer_3_match_confirmed_meeting_plan/code.html\'"\2', html
        )

    elif i == 5:
        # Back arrow Screen 6 -> Screen 5
        html = re.sub(
            r'(aria-label="Go Back"[^>]*?)(onclick="[^"]*")([^>]*>)',
            r'\1\3', html
        )
        html = re.sub(
            r'(aria-label="Go Back"[^>]*)(>)',
            r'\1 onclick="location.href=\'../05-volunteer_4_live_outing_check_in/code.html\'"\2', html
        )
        
    # Clean up double onclicks
    html = re.sub(r'onclick="[^"]*"\s*onclick="([^"]*)"', r'onclick="\1"', html)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
        
print("Bugs fixed successfully!")
