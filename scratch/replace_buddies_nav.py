import re
import glob

# The buddies nav we just used
buddies_nav = """<nav aria-label="Main Navigation" class="fixed bottom-0 left-0 w-full z-50 flex justify-around items-center bg-surface-container-lowest border-t border-outline-variant/30 shadow-lg max-w-md mx-auto right-0">
    <div class="w-full flex justify-around items-center py-2 px-3">
      <a href="../../02-discovery/discovery.html" class="flex flex-col items-center justify-center text-on-surface-variant px-3 py-1 min-h-[52px] rounded-xl hover:bg-surface-container active:scale-95"><span class="material-symbols-outlined text-[24px]">event</span><span class="text-label-sm font-semibold mt-0.5">Activity</span></a>
      <a href="../../03-buddies/01-call kaki/code.html" class="flex flex-col items-center justify-center bg-primary text-on-primary rounded-full px-3 py-1 min-h-[52px]"><span class="material-symbols-outlined text-[24px]" style="font-variation-settings:'FILL' 1;">diversity_1</span><span class="text-label-sm font-semibold mt-0.5">Buddies</span></a>
      <a href="#" class="flex flex-col items-center justify-center text-on-surface-variant px-3 py-1 min-h-[52px] rounded-xl hover:bg-surface-container active:scale-95"><span class="material-symbols-outlined text-[24px]">health_and_safety</span><span class="text-label-sm font-semibold mt-0.5">Care Hub</span></a>
      <a href="#" class="flex flex-col items-center justify-center text-on-surface-variant px-3 py-1 min-h-[52px] rounded-xl hover:bg-surface-container active:scale-95"><span class="material-symbols-outlined text-[24px]">person</span><span class="text-label-sm font-semibold mt-0.5">Profile</span></a>
    </div>
  </nav>"""

nav_pattern = r'<nav[^>]*bottom-0[^>]*>.*?</nav>'

# Get all code.html in 03-buddies
files = glob.glob("/Users/Rishabh/Documents/Antigravity/Senior Date/03-buddies/**/code.html", recursive=True)
for fpath in files:
    with open(fpath, "r") as f:
        html = f.read()
    
    html = re.sub(nav_pattern, buddies_nav, html, flags=re.DOTALL)
    with open(fpath, "w") as f:
        f.write(html)
    print(f"Updated nav in {fpath}")

