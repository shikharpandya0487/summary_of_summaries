# InsightHub — Product Definition

> **1.5-day build for 2 developers. MVP: RSS-only ingestion, localStorage persistence, heuristic categorisation. Anon-first — no login required, inspired by roadmap.sh and ILovePdf.**

---

## 1. Vision

InsightHub is a web app for busy developers who want to stay on top of the best engineering content without spending hours browsing blogs, newsletters, and social media. It ingests articles from top engineering blogs (ByteByteGo, Anthropic, Meta Engineering, and more), automatically extracts the key findings, and presents them as a clean, browsable feed of concise summaries — so a developer can get the signal from ten posts in five minutes. **No login required** — like [roadmap.sh](https://roadmap.sh) or [ILovePdf](https://www.ilovepdf.com/), the core experience is fully available to anonymous visitors the instant they land. *This is a success if a user can open the app during a coffee break and walk away knowing the three most important things that happened in the engineering world that day.*

---

## 2. Users

**Priya — Senior Backend Engineer**
- 8 years experience, works at a mid-size SaaS company.
- Follows 15+ engineering blogs and 4 newsletters but is overwhelmed by the volume.
- Wants a daily snapshot of genuinely interesting findings without the noise.
- Moderately tech savvy — comfortable with web apps, expects clean UI.

**Marcus — Junior Full-Stack Developer**
- 1.5 years in the industry, still building his mental model of "what matters."
- Subscribes to ByteByteGo and a few YouTube channels but often misses big announcements.
- Wants summaries that explain jargon and connect dots for him.
- Prefers browsing over searching — exploratory feed works best.

**Tanvi — Engineering Manager**
- Manages a team of 6, has very limited time for individual learning.
- Needs to know about major tooling changes, deprecations, and breakthroughs that affect her team's stack.
- Wants to share relevant findings with her team easily.
- Will use the app 2-3 times a week for 5-10 minutes.

---

## 3. User Stories

### Core (No Login Required — MVP)

*Inspired by roadmap.sh and ILovePdf: the full core experience works instantly for anonymous visitors.*

**1. As a visitor, I want to see a feed of the latest findings from engineering blogs, so that I can quickly browse what's new.**
> **Done when:**
> - Feed page loads with items sorted by publication date (newest first)
> - Each item shows: title, source blog name, publication date, and a 1-2 sentence summary
> - Feed paginates or infinite-scrolls (20 items per page)
> - At least 3 source blogs are being polled (e.g. ByteByteGo, Anthropic, Meta Engineering)

**2. As a visitor, I want to click a finding to see the full summary and details, so that I can understand it deeply.**
> **Done when:**
> - Detail page shows title, source, date, full summary (3-5 paragraphs), and a list of key takeaways
> - A "Read Original" link opens the source article in a new tab
> - The page is responsive (works on mobile browser)

**3. As a visitor, I want to filter the feed by source blog, so that I can focus on content from specific authors.**
> **Done when:**
> - Filter bar with checkboxes for each active source blog
> - Selecting a source filters the feed to only show items from that source
> - "Show All" option to reset filters
> - Filter state is reflected in the URL (shareable filtered view)

**4. As a visitor, I want the feed to auto-refresh so that I see newly published findings without reloading manually.**
> **Done when:**
> - A "New items available" banner appears when new content is fetched
> - Clicking the banner or a refresh button loads new items
> - Feed polls for updates every 5 minutes via background fetch

**5. As a visitor, I want to bookmark findings so that I can save interesting ones to read later.**
> **Done when:**
> - Each feed item has a bookmark icon
> - Clicking toggles bookmark state (visual feedback: filled/outline icon)
> - Bookmarks persist across page reloads (stored in localStorage — no account needed)
> - A "Bookmarks" tab shows all saved items

**6. As a visitor, I want to search findings by keyword, so that I can find content about specific topics.**
> **Done when:**
> - Search bar at the top of the feed
> - Searches across title, summary, and source name
> - Results update as the user types (debounced)
> - Empty state message when no results match

### Nice-to-Have (Still Anonymous — No Login)

**7. As a visitor, I want findings auto-categorised (e.g. breakthrough, debugging, architecture), so that I can filter by category.**
> **Done when:**
> - Each item shows a category badge (e.g. 🔥 Breakthrough, 🐛 Debugging, 🏗️ Architecture)
> - Feed can be filtered by category
> - Categories are assigned by keyword-based heuristics

**8. As a visitor, I want to upvote findings so that the community can surface the best content.**
> **Done when:**
> - Upvote button on each item and detail page
> - Vote count displayed next to the button
> - Users can upvote only once per item (localStorage tracking)
> - Feed can be sorted by "Most Upvoted"

**9. As a visitor, I want to see a "Breakthroughs" spotlight section so that I don't miss major announcements.**
> **Done when:**
> - A curated section on the homepage showing items tagged as "breakthrough"
> - Shows top 3 breakthrough items from the last 7 days
> - Badge or visual distinction from regular feed items

**10. As a visitor, I want dark mode so that late-night browsing is easier on my eyes.**
> **Done when:**
> - Toggle in the header switches between light and dark themes
> - Preference stored in localStorage
> - All components respect the theme

### Nice-to-Have (Requires Authentication — Post-MVP)

**11. As a returning user, I want to subscribe to a daily email digest so that I get the top findings delivered to my inbox.**
> **Done when:**
> - Email subscription form (email + frequency preference)
> - Daily cron job sends top 5 items from the last 24 hours
> - Unsubscribe link in email
> - Basic email template with title, summary, and links

**12. As a user, I want my bookmarks and preferences to sync across devices, so that I can pick up where I left off.**
> **Done when:**
> - User account with email/password or OAuth
> - Bookmarks stored server-side
> - Preferences (filters, dark mode) sync to account
> - Log in on any device → same experience

**13. As a user, I want to follow specific sources and topics so that my feed reflects my interests.**
> **Done when:**
> - Follow/unfollow sources and categories
> - Feed re-ranked based on followed interests
> - "For You" tab shows personalised content

---

## 4. Scope

### Core (No Login Required — MVP)
- RSS feed polling from 3-5 engineering blogs
- Text extraction and auto-summarisation of articles
- Feed view sorted by date with pagination
- Detail view with full summary, takeaways, and original link
- Filter by source
- Bookmark items (localStorage — no account needed)
- Keyword search
- Responsive design (mobile + desktop)
- Background auto-refresh with notification banner

### Nice-to-Have (Still Anonymous)
- Auto-categorisation (breakthrough / debugging / architecture)
- Upvoting with most-upvoted sort
- Spotlight: "Breakthroughs of the Week" section
- Dark mode
- Shareable finding permalinks

### Nice-to-Have (Requires Auth — Post-MVP)
- Daily email digest
- User accounts with cross-device sync
- Personalised feed ("For You" tab)
- Follow sources and topics
- Third-party integrations (Slack, Discord, email digests)

### Non-Goals
- User accounts / authentication is not needed for the MVP — the app is fully functional for anonymous visitors (like roadmap.sh or ILovePdf)
- Personalised feeds (no user profiles or recommendations in MVP)
- YouTube or newsletter ingestion (RSS blogs only)
- Community comments or discussion
- Mobile app (responsive web only)
- Real-time push notifications

---

## 5. Key Screens / Mockups

```
┌─────────────────────────────────────────────────────────────┐
│                         HOME / FEED                           │
│                                                              │
│  [InsightHub]                                    [🔍 Search] │
│  ─────────────────────────────────────────────────────────── │
│  🔄 New findings available — Click to refresh               │
│  ─────────────────────────────────────────────────────────── │
│                                                              │
│  Filters: [☑ All] [☑ ByteByteGo] [☑ Anthropic] [☑ Meta]    │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 🏗️ ByteByteGo · 2h ago · 5 min read                      │ │
│  │ Why Uber Moved from Microservices to Monoliths            │ │
│  │ Uber's core ride-matching logic now runs as a well-       │ │
│  │ defined monolith, cutting latency by 30%...               │ │
│  │ [Read More]  [🔖 Bookmark]                                │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 🔥 Anthropic · 5h ago · 3 min read                       │ │
│  │ Claude 4 Achieves 97.3% on MATH Benchmark                 │ │
│  │ Claude 4 surpasses GPT-5 by 2.1 points with a novel       │ │
│  │ sparse attention mechanism...                             │ │
│  │ [Read More]  [🔖 Bookmark]                                │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  User Flow: Feed → Click "Read More" → Detail Page           │
│             Feed → Click 🔖 → Bookmarks tab                  │
│             Feed → Type in search bar → Filtered results     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                       DETAIL PAGE                            │
│                                                              │
│  [← Back to Feed]                                            │
│                                                              │
│  🔥 BREAKTHROUGH                                             │
│                                                              │
│  Claude 4 Achieves 97.3% on MATH Benchmark                   │
│                                                              │
│  Anthropic · July 28, 2026 · 3 min read  [🔖 Bookmark]      │
│  ─────────────────────────────────────────────────────────── │
│                                                              │
│  Key Takeaways                                               │
│  • 97.3% accuracy on MATH (↑2.1 vs GPT-5)                   │
│  • 4x faster inference than Claude 3                         │
│  • New sparse attention architecture                         │
│                                                              │
│  Full Summary                                                │
│  Anthropic has released Claude 4, achieving a new state-     │
│  of-the-art on the MATH benchmark...                         │
│  [2 more paragraphs]                                         │
│                                                              │
│  📎 [Read Original Article →]                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                       BOOKMARKS TAB                          │
│                                                              │
│  [Feed]  [Bookmarks ★]                                       │
│                                                              │
│  Your Saved Items (3)                                        │
│  ─────────────────────────────────────────────────────────── │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 🏗️ ByteByteGo — Why Uber Moved from Microservices...  │ │
│  │ Saved July 28, 2026  [🔖 Unsave]                        │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 🔥 Anthropic — Claude 4 MATH Benchmark                   │ │
│  │ Saved July 28, 2026  [🔖 Unsave]                        │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Scoring & Curation

### Scoring Formula

```
FinalScore = (Recency x 0.25) + (SourceAuthority x 0.20) +
             (ContentQuality x 0.25) + (CommunitySignal x 0.20) +
             (UserFeedback x 0.10)
```

### Scoring Factors

| Factor | Weight | Components |
|--------|--------|------------|
| Recency | 25% | Exponential decay, 48h half-life |
| Source Authority | 20% | Tier 1: Anthropic/Meta/ByteByteGo, Tier 2: IBM/Oracle |
| Content Quality | 25% | Length x tech density x code blocks x narrative structure |
| Community Signal | 20% | Upvotes, saves, dwell time across anonymous visitors |
| User Feedback | 10% | Votes, show-more/less clicks (localStorage), anonymous |

### Acceptance Rules

- **score >= 60** — mandatory minimum for feed inclusion
- **source_authority >= Tier 3**
- Bonus: +15 breakthrough, +10 debugging-war-story, +10 contains code
- Penalty: -5 marketing content, -5 length < 300 words
- **score > 80** → eligible for Spotlight section

### Auto-Classification Taxonomy

| Category | Detection |
|----------|-----------|
| Breakthrough | New model release, SOTA result, major perf improvement |
| Debugging | Root cause analysis, production incident, postmortem |
| Architecture | System design, tradeoff analysis, migration story |
| Tutorial | Step-by-step guide, how-to, code walkthrough |
| Release Notes | Version changelog, deprecation notice, feature announcement |

---

## 7. Tech Stack (MVP)

| Layer | Technology |
|-------|-----------|
| Backend | Python (FastAPI) or Node (Express) — lightweight server with RSS polling and LLM integration |
| Frontend | React / Vue / Svelte SPA — feed UI, detail view, filter, search, bookmarks |
| Database | SQLite — findings + sources tables with FTS5 for full-text search |
| LLM | OpenAI API / Anthropic API / Ollama — summarisation (TL;DR, takeaways, full) |
| Cache | Redis (optional MVP) — feed cache, dedup tracking |
| Persistence | localStorage — bookmarks, preferences, upvotes (no account needed) |

---

## 8. Implementation Plan (1.5 Days)

### Day 1 — Backend & Ingestion
- RSS poller + parser for 3-5 engineering blogs
- SQLite schema (sources, findings tables)
- HTML-to-text extraction
- LLM summarisation (TL;DR + takeaways)
- Scoring + quality gate (score >= 60)
- REST API endpoints (GET /feed, GET /findings/:id)

### Day 2 — Frontend & Polish
- Feed view (sorted by date, 20 items, infinite scroll)
- Detail view (summary, takeaways, original link)
- Filter by source (URL state)
- Bookmark toggle (localStorage)
- Search (debounced, across titles)
- Auto-refresh banner (polls every 5min)
- Responsive CSS (mobile + desktop)

### Stretch (if time permits)
- Dark mode toggle
- Upvote + most-upvoted sort

---

## 9. Data & Rules

### Core Entity: Finding

| Field | Type | Notes |
|---|---|---|
| `id` | auto-increment integer | Primary key |
| `title` | string (required) | From article title |
| `source_name` | string (required) | Blog name, e.g. "Anthropic" |
| `source_url` | string (required, unique) | Original article URL |
| `published_at` | datetime (required) | Article publication date |
| `fetched_at` | datetime | When we polled the RSS feed |
| `summary_tldr` | text (required) | 1-2 sentence summary |
| `summary_full` | text (required) | 3-5 paragraph summary |
| `key_takeaways` | text[] | Array of bullet points |
| `category` | string | One of: breakthrough, debugging, architecture, tutorial, release-notes, general |
| `upvotes` | integer | Default 0 |

### Entity: Source

| Field | Type | Notes |
|---|---|---|
| `id` | auto-increment integer | Primary key |
| `name` | string (required, unique) | Display name |
| `rss_url` | string (required) | RSS feed URL |
| `website_url` | string | Blog homepage |
| `is_active` | boolean | Whether we currently poll this source |
| `last_fetched_at` | datetime | Last successful poll |

### Rules

- **A finding's source_url must be unique** — if the same article is published by the same source, we update rather than duplicate.
- **Summaries are generated on first fetch** — when a new article is polled, it is queued for summarisation before appearing in the feed.
- **Bookmarks are stored in localStorage** — no user accounts in MVP, so bookmarks are per-browser. Clearing browser data loses them.
- **Upvote limit is per-browser** — tracked in localStorage by finding ID. One vote per finding per browser.
- **Auto-categorisation is heuristic-based** — keyword matching on title and full text. Not ML. Categories are stored but can be overridden manually.
- **Feed shows items from the last 30 days** — older items are searchable but not in the default feed.
- **RSS polling runs every 15 minutes** — lightweight cron checks all active sources for new items.
- **Rate limiting** — respect `robots.txt` and minimum 10-second delay between requests to the same domain.

---

*Auth, email digests, and personalisation come post-MVP. The core app is fully functional for anonymous visitors — like roadmap.sh or ILovePdf: deliver value the instant someone lands on the page.*
