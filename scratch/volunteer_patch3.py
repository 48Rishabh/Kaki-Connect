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

# Standard Nav generation function
def get_nav(active_tab):
    def get_tab(name, icon, href, is_active):
        if is_active:
            return f"""<a href="{href}" class="flex flex-col items-center justify-center bg-primary text-on-primary rounded-full px-4 py-1.5 font-bold shadow-sm active:scale-95 transition-transform duration-150 ease-out"><span class="material-symbols-outlined text-[22px]" style="font-variation-settings: 'FILL' 1;">{icon}</span><span class="font-label-sm text-label-sm font-bold tracking-tight">{name}</span></a>"""
        else:
            return f"""<a href="{href}" class="flex flex-col items-center justify-center text-on-surface-variant px-spacing-sm py-spacing-2xs hover:bg-surface-container-highest hover:text-on-surface active:scale-95 transition-transform duration-150 ease-out"><span class="material-symbols-outlined text-[22px]">{icon}</span><span class="font-label-sm text-label-sm">{name}</span></a>"""

    s2_href = "../02-volunteer_2_open_requests_feed/code.html"
    s4_href = "../04-volunteer_3_match_confirmed_meeting_plan/code.html"
    s6_href = "../06-volunteer_5_safety_guidelines_protocols/code.html"

    t1 = get_tab("Missions", "volunteer_activism", s2_href, active_tab == "Missions")
    t2 = get_tab("Check-in", "how_to_reg", s4_href, active_tab == "Check-in")
    t3 = get_tab("Community", "diversity_1", s6_href, active_tab == "Community")
    t4 = get_tab("Profile", "person", "#", False)

    return f"""<nav class="fixed bottom-0 left-0 w-full z-50 flex justify-around items-center bg-surface-container-low border-t border-outline-variant/20 shadow-lg max-w-md mx-auto right-0 px-gutter-mobile py-spacing-xs pb-safe">
  {t1}
  {t2}
  {t3}
  {t4}
</nav>"""

for i, folder in enumerate(SCREENS):
    path = os.path.join(BASE, folder, "code.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Determine active tab
    if i in [0, 1, 2]: active_tab = "Missions"
    elif i in [3, 4]: active_tab = "Check-in"
    elif i == 5: active_tab = "Community"

    # Replace existing bottom nav (using <nav...>...</nav> or the <div...><button...Missions...</div> at bottom)
    # Screens 1-6 might have slightly different markup for bottom nav
    # Let's target the nav block directly if it's <nav>
    nav_pattern = r'<nav[^>]*bottom-0[^>]*>.*?</nav>'
    if re.search(nav_pattern, html, flags=re.DOTALL):
        html = re.sub(nav_pattern, get_nav(active_tab), html, flags=re.DOTALL)
    else:
        # Some screens use a div fixed bottom-0 left-0 ... right-0 with buttons. e.g. <div class="... fixed bottom-0 ...">
        div_nav_pattern = r'<div[^>]*fixed bottom-0[^>]*>.*?</div>\n? *</div>\n*$'
        # Or look for the block containing "Check-in Tab" or "Missions" at the very end of the file.
        # It's safer to just look for the wrapper of those tabs.
        tab_wrap_pattern = r'<div[^>]*fixed bottom-0[^>]*>.*?Missions.*?</div>'
        html = re.sub(tab_wrap_pattern, get_nav(active_tab), html, flags=re.DOTALL)

    # -------------------------------------------------------------
    # Screen specific wiring
    # -------------------------------------------------------------
    if i == 0: # Screen 1 -> 2
        # Back arrow to root
        html = re.sub(
            r'(aria-label="Go Back"[^>]*)onclick="[^"]*"',
            r'\1',
            html, flags=re.IGNORECASE
        )
        html = re.sub(
            r'(aria-label="Go Back"[^>]*)(>)',
            r'\1 onclick="location.href=\'../../index.html\'"\2',
            html, flags=re.IGNORECASE
        )
        # View open Requests
        html = re.sub(
            r'(<button[^>]*)(onclick="[^"]*")([^>]*>[\s\S]*?View Open Requests[\s\S]*?</button>)',
            r'\1\3',
            html, flags=re.IGNORECASE
        )
        html = re.sub(
            r'(<button[^>]*)(>[\s\S]*?View Open Requests[\s\S]*?</button>)',
            r'\1 onclick="location.href=\'../02-volunteer_2_open_requests_feed/code.html\'"\2',
            html, flags=re.IGNORECASE
        )

    elif i == 1: # Screen 2 -> 3
        # Back arrow to 1
        html = re.sub(
            r'(aria-label="Back to Overview"[^>]*)onclick="[^"]*"',
            r'\1',
            html, flags=re.IGNORECASE
        )
        html = re.sub(
            r'(aria-label="Back to Overview"[^>]*)(>)',
            r'\1 onclick="location.href=\'../01-volunteer_1_welcome_overview/code.html\'"\2',
            html, flags=re.IGNORECASE
        )
        # "I can help" -> Screen 3
        html = re.sub(
            r'(<button[^>]*I Can Help.*?)(onclick="[^"]*")([^>]*>)',
            r'\1\3',
            html, flags=re.IGNORECASE|re.DOTALL
        )
        html = re.sub(
            r'(<button)([^>]*I Can Help.*?)(>)',
            r'\1 onclick="location.href=\'../03-volunteer_2_outing_details_route/code.html\'"\2\3',
            html, flags=re.IGNORECASE|re.DOTALL
        )

    elif i == 2: # Screen 3 -> 4
        # Back arrow to 2
        html = re.sub(
            r'(<button[^>]*)(onclick="window.history.back\(\)")([^>]*>.*?<span[^>]*>arrow_back)',
            r'\1\3',
            html, flags=re.IGNORECASE|re.DOTALL
        )
        # We need to find the specific back arrow. It might be <button aria-label="Go Back"
        html = re.sub(
            r'(aria-label="Go Back"[^>]*)onclick="[^"]*"',
            r'\1',
            html, flags=re.IGNORECASE
        )
        html = re.sub(
            r'(aria-label="Go Back"[^>]*)(>)',
            r'\1 onclick="location.href=\'../02-volunteer_2_open_requests_feed/code.html\'"\2',
            html, flags=re.IGNORECASE
        )
        
        # Primary Button 'Accept and Help' -> Screen 4
        # Wait, earlier I saw "Accompanying request accepted! Contacting Fei Yue FSC & Mr Tan..." alert.
        html = re.sub(
            r'(<button[^>]*)(onclick="alert[^"]*")([^>]*>[\s\S]*?Accept[^<]*</button>)',
            r'\1onclick="location.href=\'../04-volunteer_3_match_confirmed_meeting_plan/code.html\'"\3',
            html, flags=re.IGNORECASE|re.DOTALL
        )
        # Just in case it doesn't have an alert but has Accept
        html = re.sub(
            r'(<button[^>]*)(>[\s\S]*?Accept.*?Help[\s\S]*?</button>)',
            r'\1 onclick="location.href=\'../04-volunteer_3_match_confirmed_meeting_plan/code.html\'"\2',
            html, flags=re.IGNORECASE|re.DOTALL
        )
        
    elif i == 3: # Screen 4 -> 5
        # Back arrow to 3
        html = re.sub(
            r'(aria-label="Go Back"[^>]*)onclick="[^"]*"',
            r'\1',
            html, flags=re.IGNORECASE
        )
        html = re.sub(
            r'(aria-label="Go Back"[^>]*)(>)',
            r'\1 onclick="location.href=\'../03-volunteer_2_outing_details_route/code.html\'"\2',
            html, flags=re.IGNORECASE
        )
        # Banner -> Screen 5
        # "booking matched" or similar
        banner_pattern = r'(<section[^>]*bg-primary/5[^>]*>[\s\S]*?)(Booking Matched|Match Confirmed)([\s\S]*?</section>)'
        html = re.sub(banner_pattern, r'\1\2\3', html, flags=re.IGNORECASE)
        # Wait, let's just make the whole section clickable if it has Booking Matched
        if 'Booking Matched' in html or 'Match Confirmed' in html or 'helping Uncle Tan' in html.lower() or 'helping uncle tam' in html.lower():
            # Actually, I'll just find the first section with "Booking" or "Matched" and add onclick
            pass # We will do a generic replacement after

    elif i == 4: # Screen 5 -> Screen 4 (back)
        # Back arrow to 4
        html = re.sub(
            r'(aria-label="Back"[^>]*)onclick="[^"]*"',
            r'\1',
            html, flags=re.IGNORECASE
        )
        html = re.sub(
            r'(aria-label="Back"[^>]*)(>)',
            r'\1 onclick="location.href=\'../04-volunteer_3_match_confirmed_meeting_plan/code.html\'"\2',
            html, flags=re.IGNORECASE
        )
        
    elif i == 5: # Screen 6 back -> 5
        html = re.sub(
            r'(aria-label="Go Back"[^>]*)onclick="[^"]*"',
            r'\1',
            html, flags=re.IGNORECASE
        )
        html = re.sub(
            r'(aria-label="Go Back"[^>]*)(>)',
            r'\1 onclick="location.href=\'../05-volunteer_4_live_outing_check_in/code.html\'"\2',
            html, flags=re.IGNORECASE
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
        
print("Nav tabs and backward links updated.")

