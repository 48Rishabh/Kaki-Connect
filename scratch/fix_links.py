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

def make_back_anchor(html, href):
    # Find any back button: aria-label="Go Back" or aria-label="Back to Overview" or aria-label="Back"
    # Replace <button ...> with <a href="..." ...>
    # Replace </button> with </a> for that button.
    # Also add pointer-events-none to the inner span.
    
    # Let's do this by finding the button tag and the closing tag
    pattern = r'(<button)([^>]*aria-label="(?:Go Back|Back to Overview|Back)"[^>]*>)([\s\S]*?)(</button>)'
    
    def replacer(m):
        attrs = m.group(2)
        # remove type="button"
        attrs = re.sub(r'\s*type="button"', '', attrs)
        # remove onclick="location.href='...'"
        attrs = re.sub(r'\s*onclick="[^"]*"', '', attrs)
        # remove onclick=location.href=...
        attrs = re.sub(r'\s*onclick=location\.href=[^\s>]*', '', attrs)
        # add href
        # the backslash might be escaped in the file, like onclick="location.href=\'...\'"
        attrs = re.sub(r'\\\'', "'", attrs) # Just cleanup
        
        inner_html = m.group(3)
        # Add pointer-events-none to span
        inner_html = re.sub(r'(<span[^>]*)class="([^"]*)"', r'\1class="\2 pointer-events-none"', inner_html)
        # if span has no class, add it
        if 'class="' not in inner_html and '<span' in inner_html:
            inner_html = inner_html.replace('<span', '<span class="pointer-events-none"')
            
        return f'<a href="{href}"{attrs}{inner_html}</a>'
        
    return re.sub(pattern, replacer, html, flags=re.IGNORECASE)

for i, folder in enumerate(SCREENS):
    path = os.path.join(BASE, folder, "code.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Fix Back Buttons
    if i == 0: href = "../../index.html"
    elif i == 1: href = "../01-volunteer_1_welcome_overview/code.html"
    elif i == 2: href = "../02-volunteer_2_open_requests_feed/code.html"
    elif i == 3: href = "../03-volunteer_2_outing_details_route/code.html"
    elif i == 4: href = "../04-volunteer_3_match_confirmed_meeting_plan/code.html"
    elif i == 5: href = "../05-volunteer_4_live_outing_check_in/code.html"
    
    html = make_back_anchor(html, href)
    
    # 2. Fix "I Can Help" buttons in Screen 2
    if i == 1:
        pattern = r'(<button)([^>]*>[\s\S]*?I Can Help[\s\S]*?)(</button>)'
        def repl_i_can_help(m):
            attrs = m.group(2)
            # Remove onclick
            attrs = re.sub(r'\s*onclick="[^"]*"', '', attrs)
            attrs = re.sub(r'\s*type="button"', '', attrs)
            return f'<a href="../03-volunteer_2_outing_details_route/code.html"{attrs}</a>'
        html = re.sub(pattern, repl_i_can_help, html, flags=re.IGNORECASE)

    # 3. Clean up the View Open Requests button in Screen 1 just in case it had escaped quotes
    if i == 0:
        html = re.sub(r'onclick="location\.href=\\\'([^\\\']*)\\\'"', r'onclick="location.href=\'\1\'"', html)

    # Clean up any leftover escaped quotes in all onclicks globally just in case
    html = re.sub(r'onclick="location\.href=\\\'([^\\\']*)\\\'"', r'onclick="location.href=\'\1\'"', html)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

print("Back arrows and I Can Help buttons fixed.")

