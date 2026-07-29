# InsightHub — Pitch Script (3-4 min)

---

## Speaker 1 — The Problem & Vision (1.5-2 min)

Hi, we're building **InsightHub**.

**The problem:** Every day, engineers like us scroll through 15+ engineering blogs, newsletters, and social media — ByteByteGo, Meta Engineering, Anthropic, you name it. There's incredible content in there, but finding it means spending hours filtering noise. Most of us just give up and stick to whatever Twitter shows us.

**What if you could open a page during your coffee break and walk away knowing the three most important things that happened in engineering that day?** No signup, no noise, no scrolling through 50 tabs.

That's InsightHub.

It ingests articles from top engineering blogs, automatically distills them into **TL;DRs, key takeaways, and full summaries**, then presents them as a clean, browsable feed. Think of it as a personal research assistant for engineering content — but it works instantly for anyone who lands on the page.

**Our design north star is roadmap.sh and ILovePdf.** Both deliver full value without ever asking for an account. You land, you get value, you leave. That's it.

We're scoping this as a **1.5-day build for two developers**. MVP is RSS-only from 3-5 sources, with localStorage for bookmarks. No auth, no cloud bill — just a lightweight web app that does one thing well: **help engineers stay informed in 5 minutes**.

Over to my co-speaker for the architecture and plan.

---

## Speaker 2 — The Architecture & Plan (1.5-2 min)

Here's how it works in three steps.

**Step one — Ingestion:** A cron job polls RSS feeds every 15 minutes. New articles get parsed, deduplicated by URL and content hash, and queued for processing.

**Step two — Processing:** An LLM generates a one-sentence TL;DR, 3-5 key takeaways, and a full summary. A scoring engine ranks each finding by recency, source authority, and content quality. Items below a score of 60 get discarded — only high-signal content reaches the feed.

**Step three — Delivery:** A REST API serves the feed to a responsive web app. Users get infinite-scroll browsing, filter by source, keyword search, and bookmarking — all without an account because bookmarks live in localStorage.

**The tech stack is intentionally boring and fast:** SQLite for the database, a lightweight Python or Node backend, and vanilla-ish frontend with responsive CSS. No Kubernetes, no microservices, no auth system. Just enough to ship.

**Day one** is backend: RSS poller, summarisation pipeline, scoring, and API.

**Day two** is frontend: feed view, detail view, filters, search, bookmarks, and auto-refresh.

**Stretch goals** if time permits: dark mode and upvoting.

We're not building the next social network. We're building a utility — like a calculator for engineering news. Land, scan, leave. That's the whole thing.

Happy to take questions.

---

## Features Reference

### Core (No Login — MVP)

| Tag | Feature | Use |
|-----|---------|-----|
| Browse | Infinite-scroll feed | Latest findings sorted by date |
| Read | Full summary page | TL;DR, takeaways, glossary, original link |
| Filter | Filter by source | Check/uncheck blogs, state in URL |
| Refresh | Auto-refresh poll | Banner when new content available |
| Bookmark | Save for later | Persisted in localStorage, no account needed |
| Search | Keyword search | Full-text across titles, summaries, sources |

### Nice-to-Have (Still Anonymous)

| Tag | Feature | Use |
|-----|---------|-----|
| Categorise | Auto-tag findings | Heuristic: breakthrough, debugging, architecture, etc. |
| Upvote | Community voting | Vote on findings, sort by most-upvoted |
| Spotlight | Breakthroughs hero | Top-scoring items on homepage |
| Darkmode | Theme toggle | localStorage preference, all components themed |

### Post-MVP (Requires Auth)

| Tag | Feature | Use |
|-----|---------|-----|
| Digest | Email summary | Top findings delivered to inbox daily/weekly |
| Sync | Cross-device sync | Bookmarks and preferences across devices |
| Follow | Follow sources | Personalised feed based on followed interests |
