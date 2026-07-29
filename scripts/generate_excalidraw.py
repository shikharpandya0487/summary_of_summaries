import json, uuid

def uid():
    return str(uuid.uuid4())

FONT_N = 2
FONT_B = 3

E = []

def TXT(x, y, label, sz=11, color="#1e1e1e", bold=False, w=600, align="left"):
    E.append({
        "id": uid(), "type": "text", "x": x, "y": y,
        "width": w, "height": sz * 1.4, "angle": 0,
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 0, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [], "roundness": None,
        "boundElements": [], "updated": 1, "link": None, "locked": False,
        "text": label, "fontSize": sz,
        "fontFamily": FONT_B if bold else FONT_N,
        "textAlign": align, "verticalAlign": "top",
        "containerId": None, "originalText": label,
        "autoResize": True, "lineHeight": 1.25
    })

def RECT(x, y, w, h, fill="#fff", stroke="#1e1e1e", sw=1.5, r=None):
    E.append({
        "id": uid(), "type": "rectangle", "x": x, "y": y,
        "width": w, "height": h, "angle": 0,
        "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [], "roundness": r if r else {"type": 3},
        "boundElements": [], "updated": 1, "link": None, "locked": False
    })

def ARW(x1, y1, x2, y2, color="#868e96", sw=1.5):
    E.append({
        "id": uid(), "type": "arrow", "x": x1, "y": y1,
        "width": abs(x2 - x1), "height": abs(y2 - y1), "angle": 0,
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [], "roundness": {"type": 2},
        "boundElements": [], "updated": 1, "link": None, "locked": False,
        "points": [[0, 0], [x2 - x1, y2 - y1]],
        "lastCommittedPoint": None, "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow"
    })

def LINE(x, y, w, h, color="#868e96", sw=1):
    E.append({
        "id": uid(), "type": "line", "x": x, "y": y,
        "width": w, "height": h, "angle": 0,
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": 0, "opacity": 60, "groupIds": [], "roundness": None,
        "boundElements": [], "updated": 1, "link": None, "locked": False,
        "points": [[0, 0], [w, h]], "lastCommittedPoint": None,
        "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": None
    })

# Colors
BL = "#4263EB"; PU = "#7048E8"; GR = "#0CA678"
OR = "#F59F00"; RE = "#E03131"; GY = "#868e96"; DK = "#1e1e1e"
WH = "#ffffff"; LT = "#f8f9fa"
B1 = "#EDF2FF"; B2 = "#F3F0FF"; B3 = "#E6FCF5"
B4 = "#FFF9DB"; B5 = "#FFE8E8"; YL = "#FEF3C7"

MX = 50
CW = 1400

sec_y = -20
def section(title, brief, color):
    global sec_y
    sec_y = max((e["y"] + (e.get("height") or 0) for e in E), default=sec_y+30)
    sec_y += 50
    TXT(MX, sec_y, title, 20, color, True, CW)
    TXT(MX, sec_y + 26, brief, 11, GY, False, CW)
    LINE(MX, sec_y + 42, CW, 0, color, 2)
    sec_y += 54
    return sec_y

# ── HEADER ──
RECT(MX-10, 10, CW+20, 90, LT, "#e0e0e0", 1, {"type": 2})
TXT(MX+10, 18, "INSIGHTHUB  —  PRODUCT DESIGN WHITEBOARD", 22, DK, True, CW, "center")
TXT(MX+10, 48, "Anonymous-first UX design. Inspired by roadmap.sh and ILovePdf — deliver value without a login wall.", 11, GY, False, CW, "center")
TXT(MX+10, 70, "Badges:  ", 9, DK, True)
RECT(120, 68, 14, 10, B3, GR, 1.5, {"type":4}); TXT(139, 68, "Core (No Login)", 8, GR, True)
RECT(280, 68, 14, 10, YL, OR, 1.5, {"type":4}); TXT(299, 68, "Nice-to-Have (No Login)", 8, OR, True)
RECT(480, 68, 14, 10, B5, RE, 1.5, {"type":4}); TXT(499, 68, "Nice-to-Have (Requires Auth)", 8, RE, True)

# ────────────────────────────────────────────────
# 1. ANONYMOUS USER JOURNEY
# ────────────────────────────────────────────────
ujy = section("ANONYMOUS USER JOURNEY", "What a visitor experiences without ever signing up", BL)

steps = [
    ("1. ARRIVE", "Land on feed page.\nNo signup wall.\nContent loads instantly.", BL, B1),
    ("2. BROWSE", "Scroll infinite feed.\nFilter by source.\nSearch by keyword.", BL, B1),
    ("3. READ", "Click any finding.\nTL;DR, takeaways,\njargon glossary.", BL, B1),
    ("4. BOOKMARK", "Save with one click.\nStored in localStorage.\nNo account needed.", BL, B1),
    ("5. RETURN", "Come back any time.\nFeed auto-refreshes.\nBookmarks still there.", BL, B1),
]
for i, (title, desc, color, bg) in enumerate(steps):
    dx = MX + i * 235
    RECT(dx, ujy, 225, 105, bg, color, 2)
    RECT(dx, ujy, 225, 28, color, color, 0)
    TXT(dx+8, ujy+5, title, 12, WH, True, 210, "center")
    TXT(dx+12, ujy+38, desc, 9, DK, False, 200)
    RECT(dx+8, ujy+87, 50, 14, GR, GR, 0, {"type": 4})
    TXT(dx+11, ujy+88, "no login", 7, WH, True, 45, "center")
    if i < len(steps) - 1:
        ARW(dx+225, ujy+52, dx+235, ujy+52, BL, 1.5)

# ────────────────────────────────────────────────
# 2. FEED WIREFRAME
# ────────────────────────────────────────────────
fwy = section("FEED & DETAIL WIREFRAMES", "Core UI: what an anonymous visitor sees", BL)

# Feed card
RECT(MX, fwy, 550, 140, WH, DK, 1.5)
RECT(MX, fwy, 550, 4, BL, BL, 0)
TXT(MX+15, fwy+14, "BREAKTHROUGH  |  Anthropic  |  5 min read  |  Score: 92", 10, BL, True)
LINE(MX, fwy+32, 550, 0, "#e0e0e0", 0.5)
TXT(MX+15, fwy+42, "Claude 4 achieves 97.3% on MATH benchmark, surpassing GPT-5 by 2.1 points.", 12, DK, False, 520)
RECT(MX+15, fwy+75, 80, 20, B3, GR, 0, {"type": 2})
TXT(MX+18, fwy+77, "no login", 7, GR, True, 74, "center")
TXT(MX+110, fwy+78, "[Expand]  [Save]  [Share]", 10, GY, False)
LINE(MX, fwy+100, 550, 0, "#e0e0e0", 0.5)
TXT(MX+15, fwy+108, "Key Takeaways  ·  Full Summary  ·  Why This Matters  ·  Jargon Glossary", 9, GY, False)

# Arrow
ARW(MX+560, fwy+70, MX+590, fwy+70, GY, 1.5)

# Detail card
RECT(MX+600, fwy, 550, 140, WH, DK, 1.5)
RECT(MX+600, fwy, 550, 4, BL, BL, 0)
TXT(MX+615, fwy+14, "KEY TAKEAWAYS", 12, DK, True)
LINE(MX+600, fwy+32, 550, 0, "#e0e0e0", 0.5)
TXT(MX+615, fwy+44, "·  97.3% accuracy on MATH (+2.1 vs GPT-5)", 10, DK, False)
TXT(MX+615, fwy+64, "·  4x faster inference than Claude 3", 10, DK, False)
TXT(MX+615, fwy+84, "·  New sparse attention reduces KV cache by 60%", 10, DK, False)
TXT(MX+615, fwy+114, "[Read Full Summary]  [Read Original]", 10, BL, False)

# Second feed card below
fw2 = fwy + 160
RECT(MX, fw2, 550, 110, WH, DK, 1.5)
RECT(MX, fw2, 550, 4, PU, PU, 0)
TXT(MX+15, fw2+14, "ARCHITECTURE  |  ByteByteGo  |  8 min read  |  Score: 78", 10, PU, True)
LINE(MX, fw2+32, 550, 0, "#e0e0e0", 0.5)
TXT(MX+15, fw2+42, "Why Uber moved from microservices to well-defined monoliths for core ride-matching.", 11, DK, False, 520)
RECT(MX+15, fw2+72, 80, 20, B3, GR, 0, {"type": 2})
TXT(MX+18, fw2+74, "no login", 7, GR, True, 74, "center")
TXT(MX+110, fw2+75, "[Expand]  [Save]", 10, GY, False)

# Bookmarks tab
bky = fw2 + 130
TXT(MX, bky, "BOOKMARKS TAB  (localStorage, no login)", 14, OR, True, 450)
bky += 28
RECT(MX, bky, 550, 80, WH, OR, 1.5)
TXT(MX+15, bky+8, "[Feed]  [Bookmarks ★]  —  Your Saved Items (3)", 11, DK, False)
LINE(MX, bky+30, 550, 0, "#e0e0e0", 0.5)
TXT(MX+15, bky+42, "ByteByteGo — Why Uber Moved from Microservices...  [Unsave]", 10, DK, False)
TXT(MX+15, bky+62, "Anthropic — Claude 4 MATH Benchmark  [Unsave]", 10, DK, False)

# ────────────────────────────────────────────────
# 3. FEATURE MAP  (Core vs Nice-to-Have)
# ────────────────────────────────────────────────
fmy = section("FEATURE MAP", "Features split by auth requirement. Core features work instantly.", OR)

# Core features (anonymous)
RECT(MX, fmy, 375, 240, B3, GR, 2)
TXT(MX+15, fmy+12, "CORE  (No Login Required)", 14, GR, True, 345)
LINE(MX+10, fmy+35, 355, 0, GR, 0.5)
core_items = [
    "Infinite-scroll feed of findings",
    "TL;DR + key takeaways + full summary",
    "Filter by source blog",
    "Bookmark (localStorage persistence)",
    "Full-text keyword search",
    "Auto-refresh banner (every 5 min)",
    "Responsive mobile + desktop",
    "Jargon glossary on detail view",
]
for i, item in enumerate(core_items):
    RECT(MX+12, fmy+44+i*23, 22, 16, B3, GR, 0, {"type": 4})
    TXT(MX+40, fmy+44+i*23, item, 9, DK, False)

# Nice-to-have (anonymous, no auth)
RECT(MX+400, fmy, 375, 240, YL, OR, 2)
TXT(MX+415, fmy+12, "NICE-TO-HAVE (No Login)", 14, OR, True, 345)
LINE(MX+410, fmy+35, 355, 0, OR, 0.5)
nice_items = [
    "Auto-categorisation (breakthrough etc.)",
    "Upvote findings (localStorage tracking)",
    "Breakthroughs spotlight section",
    "Dark mode toggle (localStorage)",
    "Most-upvoted sort option",
    "Shareable permalinks (URL-based)",
]
for i, item in enumerate(nice_items):
    RECT(MX+412, fmy+44+i*23, 22, 16, YL, OR, 0, {"type": 4})
    TXT(MX+440, fmy+44+i*23, item, 9, DK, False)

# Post-MVP (requires auth)
RECT(MX+800, fmy, 375, 240, B5, RE, 2)
TXT(MX+815, fmy+12, "POST-MVP (Requires Auth)", 14, RE, True, 345)
LINE(MX+810, fmy+35, 355, 0, RE, 0.5)
post_items = [
    "Synced bookmarks across devices",
    "Personalised feed (For You tab)",
    "Follow sources / topics",
    "Daily email digest",
    "Slack / Discord integration",
    "Watchlist alerts",
]
for i, item in enumerate(post_items):
    RECT(MX+812, fmy+44+i*23, 22, 16, B5, RE, 0, {"type": 4})
    TXT(MX+840, fmy+44+i*23, item, 9, DK, False)

# ────────────────────────────────────────────────
# 4. SCORING & CURATION
# ────────────────────────────────────────────────
scy = section("SCORING & CURATION", "Fully automated — personalisation happens anonymously via heuristic rules", PU)

# Formula
RECT(MX, scy, 1170, 42, B2, PU, 2)
TXT(MX+15, scy+12, "FinalScore = (Recency × 0.25) + (SourceAuthority × 0.20) + (ContentQuality × 0.25) + (CommunitySignal × 0.20) + (UserFeedback × 0.10)", 11, DK, True, 1140)

scy += 55
# Factor table
factors = [
    ("RECENCY", "25%", "Exponential decay, 48h half-life", B1, BL),
    ("SOURCE AUTHORITY", "20%", "Tier 1: Anthropic/Meta/ByteByteGo, Tier 2: IBM/Oracle", B2, PU),
    ("CONTENT QUALITY", "25%", "Length × tech density × code blocks × narrative structure", B3, GR),
    ("COMMUNITY SIGNAL", "20%", "Upvotes, saves, dwell time across all anonymous visitors", B4, OR),
    ("USER FEEDBACK", "10%", "Votes, show-more/less clicks (localStorage), anonymous", B5, RE),
]
for i, (name, wt, desc, bg, color) in enumerate(factors):
    yy = scy + i * 28
    RECT(MX, yy, 180, 25, bg, color, 1.5, {"type": 2})
    TXT(MX+8, yy+4, name, 8, color, True)
    RECT(MX+190, yy, 55, 25, WH, GY, 1, {"type": 2})
    TXT(MX+196, yy+4, wt, 8, DK, True)
    RECT(MX+255, yy, 670, 25, WH, GY, 1, {"type": 2})
    TXT(MX+262, yy+4, desc, 8, DK, False)

scy2 = scy + len(factors)*28 + 15
TXT(MX, scy2, "RULES:", 11, PU, True)
for i, rule in enumerate([
    "score >= 60  (mandatory minimum)",
    "source_authority >= Tier 3",
    "+15 breakthrough / +10 debugging-war-story / +10 contains code",
    "-5 marketing content / -5 length < 300 words",
]):
    TXT(MX+20, scy2+i*22, ">  " + rule, 9, DK, False)

# ────────────────────────────────────────────────
# 5. AUTO-CLASSIFICATION TAXONOMY
# ────────────────────────────────────────────────
cty = section("AUTO-CLASSIFICATION TAXONOMY", "Heuristic-based, no ML, works for all anonymous visitors equally", PU)

cats = [
    ("BREAKTHROUGH", "New model release\nSOTA result\nMajor perf improvement", B1, BL),
    ("DEBUGGING", "Root cause analysis\nProduction incident\nPostmortem", B5, RE),
    ("ARCHITECTURE", "System design\nTradeoff analysis\nMigration story", B4, OR),
    ("TUTORIAL", "Step-by-step guide\nHow-to\nCode walkthrough", B3, GR),
    ("RELEASE NOTES", "Version changelog\nDeprecation notice\nFeature announcement", B2, PU),
]
for i, (title, desc, bg, color) in enumerate(cats):
    dx = MX + i * 235
    RECT(dx, cty, 225, 80, bg, color, 2)
    RECT(dx, cty, 225, 5, color, color, 0)
    TXT(dx+10, cty+12, title, 12, color, True, 205, "center")
    TXT(dx+10, cty+35, desc, 8, DK, False, 205, "center")

# ────────────────────────────────────────────────
# 6. NICE-TO-HAVE PREVIEW  (Post-MVP, needs auth)
# ────────────────────────────────────────────────
nfy = section("NICE-TO-HAVE PREVIEW  —  Post-MVP (Requires Auth)", "These features depend on user accounts. Not included in anonymous-first MVP.", RE)

# Digest Settings
RECT(MX, nfy, 360, 175, B5, RE, 2)
TXT(MX+12, nfy+10, "DIGEST SETTINGS", 12, RE, True)
LINE(MX, nfy+30, 360, 0, "#e0e0e0", 0.5)
digest_items = [
    "Frequency: [Daily]  Time: [08:00]",
    "Categories: Breakthrough, Arch, Tutorial",
    "Min Score: [60]  Max Items: [10]",
    "Delivery: Email, Slack, Discord",
]
for i, s in enumerate(digest_items):
    TXT(MX+12, nfy+40+i*28, s, 9, DK, False)
TXT(MX+12, nfy+152, "(requires user account)", 8, RE, False)

# Watchlist Preview
RECT(MX+390, nfy, 360, 175, B5, RE, 2)
TXT(MX+402, nfy+10, "WATCHLISTS & ALERTS", 12, RE, True)
LINE(MX+390, nfy+30, 360, 0, "#e0e0e0", 0.5)
watch_items = [
    "Follow sources / topics / keywords",
    "Notify: In-App, Email, Slack",
    "Min score threshold per watchlist",
    "Real-time matching engine",
]
for i, s in enumerate(watch_items):
    TXT(MX+402, nfy+40+i*28, s, 9, DK, False)
TXT(MX+402, nfy+152, "(requires user account)", 8, RE, False)

# Personalisation Preview
RECT(MX+780, nfy, 390, 175, B5, RE, 2)
TXT(MX+792, nfy+10, "PERSONALISED FEED", 12, RE, True)
LINE(MX+780, nfy+30, 390, 0, "#e0e0e0", 0.5)
pers_items = [
    "Onboarding: select topics of interest",
    "Implicit signal tracking (dwell, scroll)",
    "Feed re-ranked by personal affinity",
    "For You tab vs General tab",
]
for i, s in enumerate(pers_items):
    TXT(MX+792, nfy+40+i*28, s, 9, DK, False)
TXT(MX+792, nfy+152, "(requires user account)", 8, RE, False)

# ────────────────────────────────────────────────
# 7. SCOPE SUMMARY
# ────────────────────────────────────────────────
spy = section("SCOPE SUMMARY", "What is built in the MVP vs later phases", BL)

col_w = 420
col_gap = 30

# MVP scope
RECT(MX, spy, col_w, 210, B3, GR, 2)
TXT(MX+15, spy+10, "MVP (No Login — Core)", 14, GR, True, col_w-30)
LINE(MX+10, spy+32, col_w-20, 0, GR, 0.5)
mvp = ["RSS polling from 3-5 engineering blogs", "Text extraction + auto-summarisation", "Feed view (date-sorted, paginated)", "Detail view (TL;DR + takeaways + gloss)", "Filter by source", "Bookmark (localStorage)", "Keyword search", "Auto-refresh banner", "Responsive design"]
for i, item in enumerate(mvp):
    TXT(MX+20, spy+40+i*19, "·  " + item, 9, DK, False)

# Nice-to-have
x2 = MX + col_w + col_gap
RECT(x2, spy, col_w, 210, YL, OR, 2)
TXT(x2+15, spy+10, "NICE-TO-HAVE (No Login)", 14, OR, True, col_w-30)
LINE(x2+10, spy+32, col_w-20, 0, OR, 0.5)
nth = ["Auto-categorisation (heuristic)", "Upvote + most-upvoted sort", "Breakthroughs spotlight section", "Dark mode", "Shareable permalinks"]
for i, item in enumerate(nth):
    TXT(x2+20, spy+40+i*19, "·  " + item, 9, DK, False)

# Post-MVP
x3 = x2 + col_w + col_gap
RECT(x3, spy, col_w, 210, B5, RE, 2)
TXT(x3+15, spy+10, "POST-MVP (Requires Auth)", 14, RE, True, col_w-30)
LINE(x3+10, spy+32, col_w-20, 0, RE, 0.5)
pmvp = ["User accounts (email/OAuth)", "Synced bookmarks across devices", "Personalised feed (For You tab)", "Email digest subscription", "Slack / Discord webhooks", "Watchlist alerts"]
for i, item in enumerate(pmvp):
    TXT(x3+20, spy+40+i*19, "·  " + item, 9, DK, False)

# ────────────────────────────────────────────────
# COLOR KEY
# ────────────────────────────────────────────────
cky = max((e["y"] + (e.get("height") or 0) for e in E), default=0) + 40
RECT(MX-10, cky, CW+20, 40, LT, "#e0e0e0", 1, {"type": 2})
TXT(MX+15, cky+10, "COLOR KEY:", 10, DK, True)
legend = [(GR, "Core (No Login)"), (OR, "Nice-to-Have (No Login)"), (RE, "Requires Auth"), (BL, "Primary UI"), (PU, "Secondary"), (GY, "Neutral")]
lx = 150
for c, lbl in legend:
    RECT(lx, cky+11, 16, 14, WH, c, 1.5, {"type": 4})
    TXT(lx+22, cky+12, lbl, 8, c, True)
    lx += 160

# ── SAVE ──
doc = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": E,
    "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
    "files": {}
}

with open("insighthub-design.excalidraw", "w", encoding="utf-8") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

types = {}
fonts = {}
for e in E:
    t = e["type"]
    types[t] = types.get(t, 0) + 1
    if t == "text":
        f2 = e.get("fontFamily", 0)
        fonts[f2] = fonts.get(f2, 0) + 1

maxw = max(e["x"] + (e.get("width") or 0) for e in E)
maxh = max(e["y"] + (e.get("height") or 0) for e in E)
print(f"insighthub-design.excalidraw  |  {len(E)} elements")
print(f"Types: {types}  |  Font: Normal={fonts.get(2,0)} Bold={fonts.get(3,0)}")
print(f"Canvas: {maxw:.0f}w x {maxh:.0f}h")
