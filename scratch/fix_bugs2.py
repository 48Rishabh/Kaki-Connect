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

for folder in SCREENS:
    path = os.path.join(BASE, folder, "code.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Make sure fixed/sticky headers and navs align to 420px exact.
    # We can just add CSS rules targeting <header> and <nav> specifically for these screens.
    css_addition = """
    header, nav {
      max-width: 420px !important;
      margin-left: auto !important;
      margin-right: auto !important;
      left: 0 !important;
      right: 0 !important;
    }
  """
    if 'header, nav {' not in html:
        html = html.replace('</style>', css_addition + '</style>')

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
print("Headers and navs constrained.")
