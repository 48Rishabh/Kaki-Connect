#!/usr/bin/env python3
"""
Fix the broken phone-frame CSS injection:
1. Remove the previous `body > div:first-of-type` rule that was too broad
2. Replace with a `.kaki-phone-frame` class-based approach
3. Add that class to the correct outer wrapper div on each screen
4. Bulletproof the progress bars against height inheritance from any parent
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

# The correct phone-frame CSS using a named class + progress bar overrides
FRAME_STYLE = """<style id="kaki-phone-frame">
  /* ── Desktop backdrop ───────────────────────────────────── */
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

  /* ── Phone frame: applied via class on the outer wrapper ── */
  .kaki-phone-frame {
    width: 100% !important;
    max-width: 420px !important;
    min-height: 100vh !important;
    margin: 0 auto !important;
    position: relative !important;
    box-shadow: 0 0 40px rgba(0,0,0,0.12) !important;
    box-sizing: border-box !important;
  }

  /* ── Progress bar: always exactly 6px, never expands ────── */
  .kaki-progress-track {
    width: 100% !important;
    height: 6px !important;
    min-height: 0 !important;
    max-height: 6px !important;
    background-color: #E2E8F0 !important;
    border-radius: 9999px !important;
    overflow: hidden !important;
    flex: none !important;
    flex-shrink: 0 !important;
  }
  .kaki-progress-fill {
    height: 100% !important;
    min-height: 0 !important;
    max-height: 6px !important;
    border-radius: 9999px !important;
    background-color: #2f5d97 !important;
    display: block !important;
    flex: none !important;
  }
</style>"""

def patch_file(idx, folder, fname):
    path = os.path.join(BASE, folder, fname)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    original = html

    # ── Step 1: Remove the old broken frame style block entirely ──────────
    html = re.sub(
        r'<style id="kaki-phone-frame">.*?</style>\n?',
        '',
        html,
        flags=re.DOTALL
    )

    # ── Step 2: Inject the correct frame style before </head> ─────────────
    html = html.replace("</head>", FRAME_STYLE + "\n</head>", 1)

    # ── Step 3: Add .kaki-progress-track and .kaki-progress-fill classes ──
    # Pattern: <div class="w-full bg-slate-200/80 h-1.5 overflow-hidden">
    #            <div class="bg-primary h-full rounded-full" style="width: X%;">
    html = re.sub(
        r'(<div class=")(w-full bg-slate-200/80 h-1\.5 overflow-hidden)(")',
        r'\1\2 kaki-progress-track\3',
        html
    )
    html = re.sub(
        r'(<div class=")(bg-primary h-full rounded-full)(" style="width:)',
        r'\1\2 kaki-progress-fill\3',
        html
    )
    # Also catch style with space before colon: style="width: X%;"
    html = re.sub(
        r'(<div class=")(bg-primary h-full rounded-full)(" style="width: )',
        r'\1\2 kaki-progress-fill\3',
        html
    )

    # ── Step 4: Add .kaki-phone-frame to the correct outer wrapper ─────────
    # Strategy: find the outermost wrapping div that is a direct child of body.
    # Different screens have different body structures:
    #   Screens with outer div wrapper: add class to that div
    #   Screens without outer div wrapper (body → header directly): wrap in a div

    # For screens that already have an outer wrapper div, add the class to it.
    # Detect pattern: body immediately followed (possibly via comment/whitespace) by a <div class="...">
    #
    # Screens 03, 06, 08, 09, 11: body > div (outer wrapper) → add class
    # Screens 02, 05, 07: body > header → we need to wrap entire body content
    # Screen 04: body > main → add class to main instead
    # Screen 01: body > header → wrap
    # Screen 10: body > header → wrap

    body_first_tag = re.search(r'<body[^>]*>\s*(?:<!--[^>]*-->\s*)*<([a-z]+)', html)
    first_tag = body_first_tag.group(1) if body_first_tag else ''

    if first_tag == 'div':
        # Add kaki-phone-frame to the first div after body (outermost wrapper)
        html = re.sub(
            r'(<body[^>]*>\s*(?:<!--[^-]*(?:--(?!>)[^-]*)*-->\s*)*<div\b)([^>]*>)',
            lambda m: m.group(1) + add_class(m.group(2), 'kaki-phone-frame'),
            html,
            count=1
        )
    elif first_tag == 'main':
        # Screen 04: add class to the <main> wrapper
        html = re.sub(
            r'(<body[^>]*>\s*(?:<!--[^-]*(?:--(?!>)[^-]*)*-->\s*)*<main\b)([^>]*>)',
            lambda m: m.group(1) + add_class(m.group(2), 'kaki-phone-frame'),
            html,
            count=1
        )
    else:
        # Screens where body directly contains header/header etc. — wrap all body children
        # Insert wrapper div after <body...> and close before </body>
        # Only if not already wrapped
        if 'kaki-phone-frame' not in html:
            html = re.sub(
                r'(<body[^>]*>)',
                r'\1\n<div class="kaki-phone-frame">',
                html,
                count=1
            )
            html = html.replace('</body>', '</div>\n</body>', 1)

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Patched: {folder}/{fname}")
    else:
        print(f"⚠️  No change: {folder}/{fname}")

def add_class(attr_str, new_class):
    """Add a CSS class to an existing class="..." attribute string, or create one."""
    if 'class="' in attr_str:
        return attr_str.replace('class="', f'class="{new_class} ', 1)
    elif "class='" in attr_str:
        return attr_str.replace("class='", f"class='{new_class} ", 1)
    else:
        return f' class="{new_class}"' + attr_str

if __name__ == "__main__":
    for i, (folder, fname) in enumerate(SCREENS):
        patch_file(i, folder, fname)
    print("\nDone!")
