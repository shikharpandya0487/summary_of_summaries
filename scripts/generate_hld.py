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

def DIAM(x, y, w, h, fill="#fff", stroke="#1e1e1e", sw=1.5):
    E.append({
        "id": uid(), "type": "diamond", "x": x, "y": y,
        "width": w, "height": h, "angle": 0,
        "strokeColor": stroke, "backgroundColor": fill,
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [], "roundness": {"type": 3},
        "boundElements": [], "updated": 1, "link": None, "locked": False
    })

def ARW(x1, y1, x2, y2, color="#868e96", sw=1.5, end="arrow"):
    E.append({
        "id": uid(), "type": "arrow", "x": x1, "y": y1,
        "width": abs(x2 - x1), "height": abs(y2 - y1),
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": sw, "strokeStyle": "solid",
        "roughness": 0, "opacity": 100, "groupIds": [], "roundness": {"type": 2},
        "boundElements": [], "updated": 1, "link": None, "locked": False,
        "points": [[0, 0], [x2 - x1, y2 - y1]],
        "lastCommittedPoint": None, "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": end
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
WH = "#ffffff"; LT = "#f8f9fa"; YL = "#FEF3C7"
B1 = "#EDF2FF"; B2 = "#F3F0FF"; B3 = "#E6FCF5"
B4 = "#FFF9DB"; B5 = "#FFE8E8"; B6 = "#FEF9E7"

MX = 50
CW = 1350

sec_y = -20
def section(title, brief, color):
    global sec_y
    sec_y = max((e["y"] + (e.get("height") or 0) for e in E), default=sec_y+30)
    sec_y += 55  # generous vertical gap
    TXT(MX, sec_y, title, 18, color, True, CW)
    TXT(MX, sec_y + 24, brief, 11, GY, False, CW)
    LINE(MX, sec_y + 40, CW, 0, color, 2)
    sec_y += 52
    return sec_y

# ── HEADER ──
RECT(MX-10, 10, CW+20, 95, LT, "#e0e0e0", 1, {"type": 2})
TXT(MX+10, 18, "INSIGHTHUB  —  HIGH-LEVEL DESIGN", 20, DK, True, CW, "center")
TXT(MX+10, 46, "Anonymous-first, like roadmap.sh and ILovePdf: every core feature works without login.", 11, GY, False, CW, "center")
TXT(MX+10, 70, "NODES:  ", 9, DK, True)
lx = 130
for lbl, c in [("Source",BL),("Process",GR),("Storage",PU),("Decision",OR),("Core (No Login)", GR), ("Nice-to-Have (Auth)", OR)]:
    bg = B1 if lbl=="Source" else B3 if lbl=="Process" else B2 if lbl=="Storage" else B4 if lbl=="Decision" else B3 if "Core" in lbl else YL
    RECT(lx, 68, 14, 10, bg, c, 1.5, {"type":4})
    TXT(lx+18, 68, lbl, 8, c, True)
    lx += 125

# ────────────────────────────────────────────────
# 1. SYSTEM CONTEXT
# ────────────────────────────────────────────────
sy = section("SYSTEM CONTEXT", "How InsightHub fits into the developer ecosystem — everyone is anonymous", BL)

cx = MX + 380
RECT(cx-140, sy, 280, 58, BL, WH, 3)
TXT(cx-110, sy+10, "INSIGHTHUB", 18, WH, True, 220, "center")
TXT(cx-130, sy+34, "Summarise · Curate · Deliver    |    No Login Required", 9, "#c0d0ff", False, 260, "center")

# Left sources
for i, (a, b) in enumerate([("ENGINEERING BLOGS", "ByteByteGo, Netflix, Meta"), ("NEWSLETTERS", "Substack, Dev emails"), ("YOUTUBE / VIDEO", "Tech talks, Conferences")]):
    y0 = sy + i * 50
    RECT(MX, y0, 180, 42, B1, BL, 1.5)
    TXT(MX+5, y0+4, a, 10, BL, True, 170, "center")
    TXT(MX+5, y0+20, b, 8, DK, False, 170, "center")
    ARW(MX+180, y0+21, cx-140, sy+29, BL, 1)

# Right outputs
for i, (a, b) in enumerate([("DEVELOPERS", "Sr/Jr Engineers, Managers"), ("SITE VISITORS", "Anyone — no signup needed"), ("INTEGRATIONS", "REST API, Webhooks (future)")]):
    y0 = sy + i * 50
    RECT(cx+140, y0, 180, 42, B2, PU, 1.5)
    TXT(cx+145, y0+4, a, 10, PU, True, 170, "center")
    TXT(cx+145, y0+20, b, 8, DK, False, 170, "center")
    ARW(cx+140, sy+29, cx+140, y0+21, PU, 1)

# ────────────────────────────────────────────────
# 2. CORE FUNCTIONALITY (NO LOGIN)
# ────────────────────────────────────────────────
fy = section("CORE FUNCTIONALITY  —  No Login Required", "These features work the instant a visitor lands on the page. (Like roadmap.sh / ILovePdf)", GR)

core = [
    ("FEED BROWSING", "Scroll infinite feed of\nlatest engineering findings.\nDate-sorted with pagination.", B3, GR),
    ("DETAIL VIEW", "Click any finding to read\nthe full summary, key\ntakeaways, and jargon gloss.", B3, GR),
    ("FILTER BY SOURCE", "Check/uncheck blogs to\nnarrow the feed. State is\nstored in the URL.", B3, GR),
    ("BOOKMARKS", "Save findings to read later.\nPersisted in localStorage.\nNo account needed.", B3, GR),
    ("SEARCH", "Full-text search across\ntitles, summaries, and\nsource names. Debounced.", B3, GR),
    ("AUTO-REFRESH", "Banner when new content\nis available. Background\npolls every 5 minutes.", B3, GR),
]

gw = 190  # card width
for i, (lbl, desc, bg, color) in enumerate(core):
    dx = MX + i * (gw + 10)
    RECT(dx, fy, gw, 150, WH, color, 2)
    RECT(dx, fy, gw, 6, color, color, 0)
    TXT(dx+8, fy+14, lbl, 12, color, True, gw-16, "center")
    TXT(dx+8, fy+38, desc, 9, DK, False, gw-16)
    LINE(dx+10, fy+135, gw-20, 0, color, 1)
    TXT(dx+8, fy+138, "core · no login", 7, color, True, gw-16, "center")

# Arrow implying flow between them stays implicit — these coexist

# ────────────────────────────────────────────────
# 3. DATA FLOW
# ────────────────────────────────────────────────
dfy = section("DATA FLOW", "How content moves through the system — fully automated, no user input needed", GR)

stages = [("POLL","RSS/API",B1,BL),("NORMALISE","Dedup/Parse",B3,GR),("CLASSIFY","Tag/Score",B4,OR),
          ("SUMMARISE","TL;DR",B3,GR),("STORE","DB/Index",B2,PU),("DELIVER","Feed",B2,PU),("USER","View",B5,RE)]
for i, (lbl, desc, bg, color) in enumerate(stages):
    dx = MX + i * 150
    RECT(dx, dfy, 140, 50, bg, color, 1.5)
    TXT(dx+5, dfy+4, lbl, 10, color, True, 130, "center")
    TXT(dx+5, dfy+22, desc, 8, DK, False, 130, "center")
    if i < len(stages) - 1:
        ARW(dx+140, dfy+25, dx+150, dfy+25, GR, 1)

# Quality gate below pipeline
dgx = MX + 3*150 + 15
DIAM(dgx, dfy+72, 120, 65, B4, RE, 1.5)
TXT(dgx+12, dfy+92, "QUALITY\nGATE", 9, RE, True, 95, "center")
ARW(dgx+60, dfy+50, dgx+60, dfy+72, RE, 1)

ARW(dgx+120, dfy+105, dgx+180, dfy+105, RE, 1)
RECT(dgx+185, dfy+95, 100, 22, B5, RE, 1, {"type": 2})
TXT(dgx+192, dfy+98, "DISCARDED", 8, RE, True, 85, "center")

ARW(dgx+60, dfy+137, dgx+60, dfy+175, GR, 1)
RECT(dgx-20, dfy+175, 160, 28, B3, GR, 1.5, {"type": 2})
TXT(dgx-10, dfy+180, "TO STORAGE & DELIVERY", 9, GR, True, 140, "center")

# ────────────────────────────────────────────────
# 4. USER JOURNEY  (Anonymous)
# ────────────────────────────────────────────────
ujy = section("USER JOURNEY  —  Anonymous Visitor", "End-to-end experience without ever creating an account", OR)

steps = [("1. ARRIVE","No signup wall.\nLand on feed.","Feed","Loads instantly."),
         ("2. BROWSE","Scroll through\nlatest findings.","Explore","Filter, search."),
         ("3. READ","Click any card.\nTL;DR + Key Takeaways +\nJargon glossary.","Engage","Bookmark (localStorage)."),
         ("4. RETURN","Come back later.\nFeed auto-refreshes.\nBookmarks still there.","Repeat","No login required.")]

for i, (title, desc, action, note) in enumerate(steps):
    dx = MX + i * 265
    RECT(dx, ujy, 250, 120, B4 if i%2==0 else B1, OR if i%2==0 else BL, 2)
    RECT(dx, ujy, 250, 32, OR if i%2==0 else BL, OR if i%2==0 else BL, 0)
    TXT(dx+8, ujy+6, title, 13, WH, True, 235, "center")
    TXT(dx+10, ujy+40, desc, 9, DK, False, 230)
    LINE(dx+10, ujy+95, 230, 0, GY, 0.5)
    TXT(dx+10, ujy+98, action + "  |  " + note, 8, GY, False, 230)
    if i < len(steps) - 1:
        ARW(dx+250, ujy+60, dx+265, ujy+60, OR, 1.5)

# ────────────────────────────────────────────────
# 5. SCORING DECISION TREE
# ────────────────────────────────────────────────
sty = section("SCORING & CURATION LOGIC", "Fully automatic — no user profile needed for curation", PU)

scx = MX + CW//2

RECT(scx-85, sty, 170, 30, B1, BL, 1.5)
TXT(scx-85, sty+6, "RAW FINDING ARRIVES", 10, BL, True, 170, "center")
ARW(scx, sty+30, scx, sty+52, GY, 1.2)

DIAM(scx-75, sty+52, 150, 60, B4, OR, 1.5)
TXT(scx-60, sty+72, "PASSES QUALITY\nGATE?", 9, OR, True, 120, "center")

ARW(scx-75, sty+82, scx-145, sty+115, RE, 1)
RECT(scx-225, sty+112, 130, 24, B5, RE, 1, {"type": 2})
TXT(scx-218, sty+115, "DISCARDED", 8, RE, True, 115, "center")

ARW(scx, sty+112, scx, sty+140, GR, 1.2)
RECT(scx-180, sty+140, 360, 30, B3, GR, 1.5)
TXT(scx-170, sty+146, "COMPUTE SCORE", 10, GR, True, 340, "center")
TXT(scx-180, sty+178, "Recency · Authority · Quality · Signal · Feedback", 8, DK, False, 360, "center")
ARW(scx, sty+192, scx, sty+210, GY, 1.2)

DIAM(scx-75, sty+210, 150, 60, B4, OR, 1.5)
TXT(scx-60, sty+230, "SCORE >= 60?", 9, OR, True, 120, "center")

ARW(scx-75, sty+240, scx-145, sty+273, RE, 1)
RECT(scx-225, sty+270, 130, 24, B5, RE, 1, {"type": 2})
TXT(scx-218, sty+273, "DISCARDED", 8, RE, True, 115, "center")

ARW(scx, sty+270, scx, sty+300, GR, 1.2)
RECT(scx-130, sty+300, 260, 30, B3, GR, 1.5)
TXT(scx-120, sty+306, "CLASSIFY: Breakthrough · Debugging · Arch · Tutorial", 9, GR, True, 240, "center")
ARW(scx, sty+330, scx, sty+355, GY, 1.2)

DIAM(scx-75, sty+355, 150, 60, B4, OR, 1.5)
TXT(scx-60, sty+375, "SPOTLIGHT\nELIGIBLE?", 9, OR, True, 120, "center")

ARW(scx-40, sty+415, scx-130, sty+450, GR, 1.5)
RECT(scx-230, sty+450, 175, 26, B3, GR, 1.5, {"type": 2})
TXT(scx-222, sty+454, "FEED + SPOTLIGHT", 9, GR, True, 160, "center")
TXT(scx-222, sty+433, "score > 80", 7, DK, False, 160, "center")

ARW(scx+40, sty+415, scx+130, sty+450, GY, 1.5)
RECT(scx+55, sty+450, 175, 26, WH, GY, 1.5, {"type": 2})
TXT(scx+63, sty+454, "FEED ONLY", 9, DK, True, 160, "center")
TXT(scx+63, sty+433, "score 60-80", 7, GY, False, 160, "center")

# ────────────────────────────────────────────────
# 6. NICE-TO-HAVE (Requires Auth)
# ────────────────────────────────────────────────
nhy = section("NICE-TO-HAVE  —  Requires Authentication (Post-MVP)", "Features that need user accounts. Not in scope for the anonymous-first MVP.", OR)

# Left column: what stays anonymous
RECT(MX, nhy, 520, 175, B3, GR, 2)
TXT(MX+15, nhy+10, "CORE (No Login — MVP)", 14, GR, True, 490)
TXT(MX+15, nhy+36, "✓  Feed browsing with infinite scroll", 10, DK, False, 490)
TXT(MX+15, nhy+56, "✓  Detail view with TL;DR + takeaways", 10, DK, False, 490)
TXT(MX+15, nhy+76, "✓  Filter by source", 10, DK, False, 490)
TXT(MX+15, nhy+96, "✓  Bookmark findings (localStorage)", 10, DK, False, 490)
TXT(MX+15, nhy+116, "✓  Full-text search", 10, DK, False, 490)
TXT(MX+15, nhy+136, "✓  Auto-refresh banner", 10, DK, False, 490)
TXT(MX+15, nhy+156, "✓  Responsive design (mobile + desktop)", 10, DK, False, 490)

# Right column: what needs auth
RECT(MX+550, nhy, 520, 175, B4, OR, 2)
TXT(MX+565, nhy+10, "NICE-TO-HAVE (Requires Auth)", 14, OR, True, 490)
TXT(MX+565, nhy+36, "○  Synced bookmarks across devices", 10, DK, False, 490)
TXT(MX+565, nhy+56, "○  Personalised feed (For You tab)", 10, DK, False, 490)
TXT(MX+565, nhy+76, "○  Follow sources / topics", 10, DK, False, 490)
TXT(MX+565, nhy+96, "○  Daily / weekly email digest", 10, DK, False, 490)
TXT(MX+565, nhy+116, "○  Slack / Discord webhook integration", 10, DK, False, 490)
TXT(MX+565, nhy+136, "○  Upvote tracking across visits", 10, DK, False, 490)
TXT(MX+565, nhy+156, "○  Watchlist alerts (new matching content)", 10, DK, False, 490)

# Divider line between columns
LINE(MX+520, nhy+10, 0, 155, "#e0e0e0", 1.5)

# ────────────────────────────────────────────────
# 7. EXTERNAL INTEGRATION MAP
# ────────────────────────────────────────────────
epy = section("EXTERNAL INTEGRATION MAP", "Sources — System — Outputs. The user never needs to authenticate.", BL)

# Col 1: Sources
TXT(MX+60, epy, "DATA SOURCES", 11, BL, True, 220, "center")
for i, s in enumerate(["RSS Feeds", "YouTube API", "Substack / Email", "Search APIs", "User Submit"]):
    RECT(MX+10, epy+22+i*34, 280, 28, B1, BL, 1, {"type": 2})
    TXT(MX+18, epy+26+i*34, s, 9, DK, False, 265)
    ARW(MX+290, epy+36+i*34, MX+325, epy+36+i*34, GY, 0.8)

# Col 2: InsightHub
x2 = MX + 380
RECT(x2, epy-5, 340, 165, B1, BL, 2)
TXT(x2+20, epy+8, "INSIGHTHUB", 16, BL, True, 300, "center")
TXT(x2+20, epy+32, "Ingestion · Processing · Curation · Delivery", 9, DK, False, 300, "center")
TXT(x2+20, epy+55, "Storage: PostgreSQL + PgVector", 9, DK, False, 300, "center")
TXT(x2+20, epy+78, "Search: ElasticSearch", 9, DK, False, 300, "center")
TXT(x2+20, epy+101, "Cache: Redis", 9, DK, False, 300, "center")
TXT(x2+20, epy+124, "API: REST Gateway (no auth required)", 9, DK, False, 300, "center")
LINE(x2+20, epy+147, 300, 0, "#c0d0ff", 1)
TXT(x2+20, epy+150, "anonymous access · no API keys", 8, GY, False, 300, "center")

# Col 3: Outputs
x3 = MX + 770
TXT(x3+60, epy, "OUTPUT CHANNELS", 11, PU, True, 220, "center")
for i, o in enumerate(["Web Feed UI", "Email Digest", "Slack Integration", "Discord Webhook", "REST API"]):
    RECT(x3+10, epy+22+i*34, 280, 28, B2, PU, 1, {"type": 2})
    TXT(x3+18, epy+26+i*34, o, 9, DK, False, 265)
    ARW(x2+340, epy+36+i*34, x3+10, epy+36+i*34, GY, 0.8)

# ── SAVE ──
doc = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": E,
    "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
    "files": {}
}

with open("insighthub-hld.excalidraw", "w", encoding="utf-8") as f:
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
print(f"insighthub-hld.excalidraw  |  {len(E)} elements")
print(f"Types: {types}  |  Font: Normal={fonts.get(2,0)} Bold={fonts.get(3,0)}")
print(f"Canvas: {maxw:.0f}w x {maxh:.0f}h")
