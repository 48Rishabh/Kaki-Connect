import re

discovery_path = "/Users/Rishabh/Documents/Antigravity/Senior Date/02-discovery/discovery.html"
buddies_path = "/Users/Rishabh/Documents/Antigravity/Senior Date/03-buddies/01-call kaki/code.html"

with open(discovery_path, "r") as f:
    discovery_html = f.read()

# Make card clickable
card_pattern = r'(<article class="[^"]*tactile-hi[^"]*?)(>)'
discovery_html = re.sub(card_pattern, r'\1 cursor-pointer" onclick="location.href=\'../03-buddies/01-call kaki/code.html\'"\2', discovery_html, count=1)
# Add onclick to the inner button just in case
discovery_html = discovery_html.replace('<span>Video Call Uncle Raymond</span>', '<span onclick="location.href=\'../03-buddies/01-call kaki/code.html\'; event.stopPropagation();">Video Call Uncle Raymond</span>')

# Define the standard nav for discovery (Activities is active)
discovery_nav = """<nav aria-label="Main Navigation" class="fixed bottom-0 left-0 w-full z-50 flex justify-around items-center bg-surface-container-lowest border-t border-outline-variant/30 shadow-lg max-w-md mx-auto right-0">
    <div class="w-full flex justify-around items-center py-2 px-3">
      <a href="../02-discovery/discovery.html" class="flex flex-col items-center justify-center bg-primary text-on-primary rounded-full px-3 py-1 min-h-[52px]"><span class="material-symbols-outlined text-[24px]" style="font-variation-settings:'FILL' 1;">event</span><span class="text-label-sm font-semibold mt-0.5">Activity</span></a>
      <a href="../03-buddies/01-call kaki/code.html" class="flex flex-col items-center justify-center text-on-surface-variant px-3 py-1 min-h-[52px] rounded-xl hover:bg-surface-container active:scale-95"><span class="material-symbols-outlined text-[24px]">diversity_1</span><span class="text-label-sm font-semibold mt-0.5">Buddies</span></a>
      <a href="#" class="flex flex-col items-center justify-center text-on-surface-variant px-3 py-1 min-h-[52px] rounded-xl hover:bg-surface-container active:scale-95"><span class="material-symbols-outlined text-[24px]">health_and_safety</span><span class="text-label-sm font-semibold mt-0.5">Care Hub</span></a>
      <a href="#" class="flex flex-col items-center justify-center text-on-surface-variant px-3 py-1 min-h-[52px] rounded-xl hover:bg-surface-container active:scale-95"><span class="material-symbols-outlined text-[24px]">person</span><span class="text-label-sm font-semibold mt-0.5">Profile</span></a>
    </div>
  </nav>"""

# Find all <nav ...>...</nav> in discovery and replace them if they are bottom navs
nav_pattern = r'<nav[^>]*bottom-0[^>]*>.*?</nav>'
discovery_html = re.sub(nav_pattern, discovery_nav, discovery_html, flags=re.DOTALL)

with open(discovery_path, "w") as f:
    f.write(discovery_html)

# Now update buddies_path
with open(buddies_path, "r") as f:
    buddies_html = f.read()

buddies_nav = """<nav aria-label="Main Navigation" class="fixed bottom-0 left-0 w-full z-50 flex justify-around items-center bg-surface-container-lowest border-t border-outline-variant/30 shadow-lg max-w-md mx-auto right-0">
    <div class="w-full flex justify-around items-center py-2 px-3">
      <a href="../../02-discovery/discovery.html" class="flex flex-col items-center justify-center text-on-surface-variant px-3 py-1 min-h-[52px] rounded-xl hover:bg-surface-container active:scale-95"><span class="material-symbols-outlined text-[24px]">event</span><span class="text-label-sm font-semibold mt-0.5">Activity</span></a>
      <a href="../../03-buddies/01-call kaki/code.html" class="flex flex-col items-center justify-center bg-primary text-on-primary rounded-full px-3 py-1 min-h-[52px]"><span class="material-symbols-outlined text-[24px]" style="font-variation-settings:'FILL' 1;">diversity_1</span><span class="text-label-sm font-semibold mt-0.5">Buddies</span></a>
      <a href="#" class="flex flex-col items-center justify-center text-on-surface-variant px-3 py-1 min-h-[52px] rounded-xl hover:bg-surface-container active:scale-95"><span class="material-symbols-outlined text-[24px]">health_and_safety</span><span class="text-label-sm font-semibold mt-0.5">Care Hub</span></a>
      <a href="#" class="flex flex-col items-center justify-center text-on-surface-variant px-3 py-1 min-h-[52px] rounded-xl hover:bg-surface-container active:scale-95"><span class="material-symbols-outlined text-[24px]">person</span><span class="text-label-sm font-semibold mt-0.5">Profile</span></a>
    </div>
  </nav>"""

buddies_html = re.sub(nav_pattern, buddies_nav, buddies_html, flags=re.DOTALL)

with open(buddies_path, "w") as f:
    f.write(buddies_html)

print("Nav bars updated")
