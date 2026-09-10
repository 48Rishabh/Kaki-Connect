import os

BASE = "/Users/Rishabh/Documents/Antigravity/Senior Date/04-volunteer"

# Screen 1 -> 2
path1 = os.path.join(BASE, "01-volunteer_1_welcome_overview", "code.html")
with open(path1, "r") as f: h1 = f.read()
h1 = h1.replace('<span>View Open Requests (4 Nearby)</span>', '<span onclick="location.href=\'../02-volunteer_2_open_requests_feed/code.html\'; event.stopPropagation();" class="cursor-pointer">View Open Requests (4 Nearby)</span>')
# actually better to just add onclick to the button
h1 = h1.replace('<button class="w-full bg-primary hover:bg-primary-container text-on-primary py-3.5 px-6 rounded-full font-headline-sm text-headline-sm font-semibold flex items-center justify-center gap-2 shadow-md hover:shadow-lg tactile-press transition-all duration-200">',
'<button onclick="location.href=\'../02-volunteer_2_open_requests_feed/code.html\'" class="w-full bg-primary hover:bg-primary-container text-on-primary py-3.5 px-6 rounded-full font-headline-sm text-headline-sm font-semibold flex items-center justify-center gap-2 shadow-md hover:shadow-lg tactile-press transition-all duration-200">')
with open(path1, "w") as f: f.write(h1)

# Screen 4 -> 5
path4 = os.path.join(BASE, "04-volunteer_3_match_confirmed_meeting_plan", "code.html")
with open(path4, "r") as f: h4 = f.read()
h4 = h4.replace('<button class="w-full h-12 rounded-full bg-primary hover:bg-primary-container text-on-primary font-label-md text-label-md font-semibold shadow-sm flex items-center justify-center gap-2 tactile-press transition-all">',
'<button onclick="location.href=\'../05-volunteer_4_live_outing_check_in/code.html\'" class="w-full h-12 rounded-full bg-primary hover:bg-primary-container text-on-primary font-label-md text-label-md font-semibold shadow-sm flex items-center justify-center gap-2 tactile-press transition-all">')
with open(path4, "w") as f: f.write(h4)

# Screen 5 -> 6
path5 = os.path.join(BASE, "05-volunteer_4_live_outing_check_in", "code.html")
with open(path5, "r") as f: h5 = f.read()
h5 = h5.replace('<button class="w-full py-3.5 px-spacing-md bg-primary hover:bg-primary-container text-on-primary rounded-full font-headline-sm text-headline-sm font-bold shadow-md active:scale-95 transition-all flex items-center justify-center gap-2 group" type="button">',
'<button onclick="location.href=\'../06-volunteer_5_safety_guidelines_protocols/code.html\'" class="w-full py-3.5 px-spacing-md bg-primary hover:bg-primary-container text-on-primary rounded-full font-headline-sm text-headline-sm font-bold shadow-md active:scale-95 transition-all flex items-center justify-center gap-2 group" type="button">')
with open(path5, "w") as f: f.write(h5)

print("Buttons patched")

