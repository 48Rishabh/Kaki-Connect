import re
import os

BASE = "/Users/Rishabh/Documents/Antigravity/Senior Date/04-volunteer"

SCREENS = [
    ("01-volunteer_1_welcome_overview", "code.html"),
    ("02-volunteer_2_open_requests_feed", "code.html"),
    ("03-volunteer_2_outing_details_route", "code.html"),
    ("04-volunteer_3_match_confirmed_meeting_plan", "code.html"),
    ("05-volunteer_4_live_outing_check_in", "code.html"),
    ("06-volunteer_5_safety_guidelines_protocols", "code.html"),
]

FRAME_STYLE = """<style id="kaki-phone-frame">
  html { background: #e8eaf0; }
  body {
    background: #e8eaf0 !important;
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
    box-shadow: 0 0 40px rgba(0,0,0,0.12) !important;
    box-sizing: border-box !important;
  }
</style>"""

def add_class(attr_str, new_class):
    if 'class="' in attr_str:
        return attr_str.replace('class="', f'class="{new_class} ', 1)
    elif "class='" in attr_str:
        return attr_str.replace("class='", f"class='{new_class} ", 1)
    return f' class="{new_class}"' + attr_str

for i, (folder, fname) in enumerate(SCREENS):
    path = os.path.join(BASE, folder, fname)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # 1. Inject phone frame CSS
    if 'kaki-phone-frame' not in html or '<style' not in html:
        html = html.replace("</head>", FRAME_STYLE + "\n</head>", 1)
    
    # 2. Add phone frame class
    # For screens 01, 02 which have <div class="... max-w-md ..."> right after body
    # For others which have <header> right after body, wrap them
    body_first = re.search(r'<body[^>]*>\s*(?:<!--[^>]*-->\s*)*<([a-z]+)', html)
    if body_first:
        first_tag = body_first.group(1)
        if first_tag == 'div':
            if 'kaki-phone-frame' not in html:
                html = re.sub(
                    r'(<body[^>]*>\s*(?:<!--[^-]*(?:--(?!>)[^-]*)*-->\s*)*<div\b)([^>]*>)',
                    lambda m: m.group(1) + add_class(m.group(2), 'kaki-phone-frame'),
                    html,
                    count=1
                )
        else:
            if 'class="kaki-phone-frame"' not in html:
                html = re.sub(
                    r'(<body[^>]*>)(\s*)',
                    r'\1\2<div class="kaki-phone-frame">\n',
                    html,
                    count=1
                )
                html = html.replace('</body>', '</div>\n</body>', 1)

    # 3. Wire navigation
    # Screen 1 -> 2
    if i == 0:
        html = re.sub(
            r'(<button[^>]*Find Open Outings[^<]*</button>)',
            lambda m: m.group(1).replace('<button', '<button onclick="location.href=\'../02-volunteer_2_open_requests_feed/code.html\'"'),
            html
        )
    # Screen 2 -> 3
    elif i == 1:
        html = re.sub(
            r'(onclick="window.scrollTo\([^)]*\)")',
            r'onclick="location.href=\'../03-volunteer_2_outing_details_route/code.html\'"',
            html,
            count=1
        )
    # Screen 3 -> 4
    elif i == 2:
        html = re.sub(
            r'(onclick="alert\([^)]*\)")',
            r'onclick="location.href=\'../04-volunteer_3_match_confirmed_meeting_plan/code.html\'"',
            html
        )
    # Screen 4 -> 5
    elif i == 3:
        # Check-in CTA or something similar
        html = re.sub(
            r'(<button[^>]*bg-primary[^>]*>[\s\S]*?Check In Now[\s\S]*?</button>)',
            lambda m: m.group(1).replace('<button', '<button onclick="location.href=\'../05-volunteer_4_live_outing_check_in/code.html\'"'),
            html
        )
    # Screen 5 -> 6
    elif i == 4:
        html = re.sub(
            r'(<button[^>]*bg-primary[^>]*>[\s\S]*?Finish Outing[\s\S]*?</button>)',
            lambda m: m.group(1).replace('<button', '<button onclick="location.href=\'../06-volunteer_5_safety_guidelines_protocols/code.html\'"'),
            html
        )

    # Make back buttons use window.history.back() if they don't have onclick
    html = re.sub(
        r'(<button[^>]*aria-label="[^"]*(?:Back|overview|Go Back)[^"]*"[^>]*)(>)',
        lambda m: m.group(1) + ('' if 'onclick' in m.group(1) else ' onclick="window.history.back()"') + '>',
        html,
        flags=re.IGNORECASE
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Patched {folder}")

