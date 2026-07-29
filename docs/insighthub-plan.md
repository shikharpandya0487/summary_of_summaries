# InsightHub — Developer Tool for Technical Knowledge Discovery

## Product Overview

A **web-based developer tool** that ingests technical content from engineering blogs, newsletters, research papers, and YouTube, then distills it into beginner-friendly summaries of the most insightful findings — breakthroughs, debugging war stories, architecture decisions, and more. **No login required** — the full core experience is available to every visitor instantly, inspired by roadmap.sh and ILovePdf.

```
┌──────────────────────────────────────────────────────────────────┐
│                        INSIGHTHUB SYSTEM                          │
│                                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐        │
│  │  INGESTION   │───▶│   SCORING    │───▶│ SUMMARIZATION│        │
│  │   PIPELINE   │    │    ENGINE    │    │    LAYER     │        │
│  └──────────────┘    └──────────────┘    └──────────────┘        │
│         │                  │                      │               │
│         ▼                  ▼                      ▼               │
│  ┌──────────────────────────────────────────────────────┐        │
│  │                 STORAGE & INDEXING                     │        │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐    │        │
│  │  │ Relational│  │  Vector  │  │   Cache / Queue  │    │        │
│  │  │    DB    │  │   Store  │  │                  │    │        │
│  │  └──────────┘  └──────────┘  └──────────────────┘    │        │
│  └──────────────────────────────────────────────────────┘        │
│         │                                                         │
│         ▼                                                         │
│  ┌────────────────────────────────────────────────────────┐      │
│  │                   WEB APPLICATION                       │      │
│  │  ┌──────────┐ ┌──────────┐ ┌────────┐ ┌──────────┐    │      │
│  │  │  Feed    │ │ Topics   │ │ Digest │ │ Spotlight│    │      │
│  │  │  View    │ │ View     │ │ Engine │ │ Sections │    │      │
│  │  └──────────┘ └──────────┘ └────────┘ └──────────┘    │      │
│  │  ┌──────────┐ ┌──────────┐ ┌────────────────────┐    │      │
│  │  │ Search   │ │ Watchlist│ │ Personalization    │    │      │
│  │  │ Discovery│ │ Alerts   │ │ Engine             │    │      │
│  │  └──────────┘ └──────────┘ └────────────────────┘    │      │
│  └────────────────────────────────────────────────────────┘      │
│         │                                                         │
│         ▼                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐        │
│  │  Email       │    │  Slack /     │    │  Webhook /   │        │
│  │  Digests     │    │  Discord     │    │  API         │        │
│  └──────────────┘    └──────────────┘    └──────────────┘        │
└──────────────────────────────────────────────────────────────────┘
```

---

## 1. Goals & Scope

### Problem Statement
Developers spend hours daily filtering noise — newsletters, blogs, tweets, papers — to find the few genuinely insightful pieces. Existing aggregators lack **developer-specific curation**, **beginner-friendly summarization**, and **scoring based on engineering relevance**.

### Core Goals
- Surface **high-signal technical findings** from curated sources
- Generate **attractive, beginner-friendly summaries** with progressive disclosure
- Prioritize **latest content** while respecting authority and community feedback
- Auto-detect and spotlight **breakthroughs** and **debugging war stories**

### Target Audience
- Software engineers (junior to senior) who want to stay informed efficiently
- Engineering managers tracking industry trends
- Teams wanting shared technical awareness

### Success Metrics
| Metric | Target |
|---|---|---|
| Weekly active visitors | > 1,000 (prototype phase) |
| Avg. session duration | > 8 min |
| Items bookmarked per visitor/week | > 5 |
| Digest open rate | > 45% |
| Visitor retention (D7) | > 40% |

### Design Philosophy
Inspired by **roadmap.sh** and **ILovePdf** — both provide full core value without asking users to create an account. InsightHub follows the same principle:
- **Anonymous-first**: every core feature works on page load — feed, search, filters, bookmarks (localStorage)
- **Login is never a wall**: authentication exists only for cross-device sync and personalised delivery (email digests, follow topics)
- **Zero friction**: the first interaction is "see content", not "sign up"

---

## 2. Data Ingestion Pipeline

### Sources

| Source Type | Examples | Ingestion Method | Refresh Cadence |
|---|---|---|---|
| Engineering Blogs | ByteByteGo, IBM, Anthropic, OpenAI, Oracle, Meta Engineering, Netflix TechBlog, Uber Engineering, Google AI Blog | RSS/Atom feeds + web scraping fallback | Every 1h |
| Research Papers | arXiv, OpenReview, specific lab pages | RSS + paper metadata APIs | Every 6h |
| Newsletters | TLDR, The Algorithm, ByteByteGo newsletter, weekly ML newsletters | Email parsing API + web scraping archives | Daily |
| YouTube | Tech talks, conference recordings, engineering deep dives | YouTube Data API (transcripts + metadata) | Every 6h |
| Web Search | Google/Bing news search for targeted topics | Search APIs | On-demand |
| Community Submissions | User-submitted URLs via browser extension | Public submission endpoint | Real-time |

### Ingestion Architecture

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  RSS Poller │  │ Web Scraper │  │ YouTube API │  │ Email       │
│  (every 1h) │  │ (on-demand) │  │  (every 6h) │  │  Parser     │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │                │
       └────────────────┼────────────────┼────────────────┘
                        │                │
                        ▼                ▼
              ┌──────────────────────────────┐
              │      Deduplication Hash       │
              │  (URL + title + content hash) │
              └──────────────┬───────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │   Freshness Score Filter      │
              │   Discard if: stale, seen,    │
              │   below min quality threshold │
              └──────────────┬───────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │   Raw Content Store           │
              │   (S3 / GCS / local FS)      │
              └──────────────┬───────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │ Queue for Processing          │
              │ (RabbitMQ / Redis / SQS)      │
              └──────────────────────────────┘
```

### Time Window Strategy

| Granularity | Scope | Retention | Feed Presence |
|---|---|---|---|
| Hot (daily) | Last 24h | Indexed in hot cache | Priority |
| Fresh (weekly) | Last 7 days | Full search + feed | Default view |
| Recent (monthly) | Last 30 days | Searchable, lower feed weight | Via filters |
| Archive | 30+ days | Searchable only | Not in feed |
| Evergreen Classics | All time, high-signal | Separate "Classics" section | Dedicated tab |

### Deduplication
- **Exact**: URL + content hash match
- **Near**: Cosine similarity on title + lead paragraph (>0.95) = likely duplicate
- **Cross-source**: same story covered by multiple sources — merge signals, pick best source as canonical
- **Historical check**: query embedding store for similar content before inserting

### Source Health Monitoring
- Track fetch success rate per source
- Detect structural changes (HTML layout breaks)
- Automatic pause for sources with >20% failure rate over 24h
- Admin dashboard for source health overview

---

## 3. Curation & Scoring Engine

### Scoring Formula

```
FinalScore = (Recency × 0.25) + (SourceAuthority × 0.20) +
             (ContentQuality × 0.25) + (CommunitySignal × 0.20) +
             (UserFeedback × 0.10)
```

### Scoring Factors

| Factor | Weight | Components | Data Source |
|---|---|---|---|
| **Recency** | 25% | Exponential decay over configurable half-life (default 48h) | Ingestion timestamp |
| **Source Authority** | 20% | Tiered: Tier1 (Anthropic, OpenAI, Meta, ByteByteGo), Tier2 (IBM, Oracle, Netflix), Tier3 (notable individuals, community blogs) | Manual + algorithmic (domain authority score) |
| **Content Quality** | 25% | Length × density of technical terms × presence of code/architecture diagrams × narrative structure | ML classifier trained on historical data |
| **Community Signal** | 20% | Upvotes, saves, shares, comments, dwell time across all users | Platform analytics |
| **User Feedback** | 10% | Newsletter embedded engagement (upvotes, replies), explicit ratings, "show more like this" signals | External + internal |

### Auto-Classification Taxonomy

```
┌──────────────────────────────────────────────────────────────────┐
│                      AUTO-CLASSIFICATION                          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  BREAKTHROUGH │  │  DEBUGGING   │  │  ARCHITECTURE│           │
│  │              │  │  WAR STORY   │  │  DECISION    │           │
│  │  New model   │  │  Root cause  │  │  System      │           │
│  │  release     │  │  analysis    │  │  design      │           │
│  │  SOTA result │  │  Production  │  │  Tradeoff    │           │
│  │  Major perf  │  │  incident    │  │  analysis    │           │
│  │  improvement │  │  postmortem  │  │              │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   TUTORIAL   │  │  PAPER       │  │  RELEASE     │           │
│  │              │  │  SUMMARY     │  │  NOTES       │           │
│  │  Step-by-step│  │  Research    │  │  Version     │           │
│  │  guide       │  │  findings    │  │  changelog   │           │
│  │  How-to      │  │  ArXiv deep  │  │  Deprecations│           │
│  │              │  │  dive        │  │              │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                                                   │
│  Detection: keyword frequency × structural heuristics × LLM      │
│  verification                                                    │
└──────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria Rule System

Composable rules that define what qualifies as "insightful":

```
Rules:
  - score >= 60  (mandatory minimum)
  - source_authority >= Tier 3
  - content_length >= 500 words OR is paper-summary
  - user_feedback.positive_ratio >= 0.6 (if available)

Bonus boosts:
  +15 if category = breakthrough
  +10 if category = debugging-war-story
  +10 if contains code blocks or architecture diagrams
   -5 if primarily marketing/press release
   -5 if length < 300 words (shallow content)
```

### User Feedback Integration
- **External signals**: parse newsletter embedded upvote counts, reply threads for sentiment
- **Internal signals**: upvote/downvote per item, "show more like this", dwell time
- **Reputation system**: frequent high-quality contributors get weighting boost
- **Temporal feedback decay**: older feedback signals weighted less than recent

---

## 4. Summarization Layer

### Architecture

```
┌──────────────────────────────────────────────────────────┐
│                 SUMMARIZATION PIPELINE                     │
│                                                           │
│  Raw Content ──▶ Text Extraction ──▶ Chunking             │
│                     (HTML→text,        (overlapping        │
│                      transcript,        windows of         │
│                      PDF parsing)       ~2000 tokens)      │
│                                          │                 │
│                                          ▼                 │
│  ┌──────────────────────────────────────────────────┐     │
│  │        LLM SUMMARIZATION (4 layers)               │     │
│  │                                                   │     │
│  │  Layer 1: TL;DR (1 sentence)                     │     │
│  │  Layer 2: Key Takeaways (3-5 bullet points)      │     │
│  │  Layer 3: Full Summary (2-3 paragraphs)          │     │
│  │  Layer 4: "Why This Matters" context note        │     │
│  └──────────────────────────────────────────────────┘     │
│                          │                                 │
│                          ▼                                 │
│  ┌──────────────────────────────────────────────────┐     │
│  │        POST-PROCESSING                            │     │
│  │  - Jargon detection + glossary generation         │     │
│  │  - Category verification                         │     │
│  │  - Score consistency check                        │     │
│  │  - Source attribution injection                   │     │
│  └──────────────────────────────────────────────────┘     │
│                          │                                 │
│                          ▼                                 │
│                  Store + Index                              │
└──────────────────────────────────────────────────────────┘
```

### Progressive Disclosure Card

```
┌─────────────────────────────────────────────────────────────────┐
│  Card View (Feed)                                               │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🔥 BREAKTHROUGH  ·  Anthropic  ·  5 min read  ·  ⭐92  │   │
│  │                                                         │   │
│  │ Claude 4 achieves 97.3% on MATH benchmark,              │   │
│  │ surpassing GPT-5 by 2.1 points.                         │   │
│  │                                                         │   │
│  │ [▶ Expand]  [🔖 Save]  [👍 23]  [🔗 Share]  [ℹ ...]   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ── Click "Expand" ──▶                                         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Key Takeaways                                            │   │
│  │ • 97.3% accuracy on MATH (↑2.1 vs GPT-5)                │   │
│  │ • 4x faster inference than Claude 3                      │   │
│  │ • New sparse attention architecture                      │   │
│  │                                                          │   │
│  │ [▶ Read Full Summary]  [▶ Read Original]                 │   │
│  │                                                          │   │
│  │ Jargon: 🤔 What's "sparse attention"?                    │   │
│  │ ┌──────────────────────────────────────────────────┐     │   │
│  │ │ Sparse attention is a technique where the model   │     │   │
│  │ │ only looks at relevant parts of the input instead │     │   │
│  │ │ of everything, making it faster and more memory-  │     │   │
│  │ │ efficient.                                        │     │   │
│  │ └──────────────────────────────────────────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ── Click "Read Full Summary" ──▶ Navigate to detail page      │
└─────────────────────────────────────────────────────────────────┘
```

### Jargon Auto-Glossary Pipeline

1. Build domain term corpus from all ingested content using TF-IDF
2. Cross-reference against general English frequency lists
3. Terms with high tech-corpus frequency × low general frequency → flag as jargon
4. LLM generates one-sentence plain-English explanation per term
5. Store in glossary cache keyed by term + context
6. On render, scan summary text for glossary terms and inject tooltip markup

### Cost Optimization

| Strategy | Detail |
|---|---|
| Batch summarization | LLM processes multiple items in single call during low-traffic hours |
| Cache reuse | Same source content → reuse previous summary if content delta < 10% |
| Model tiering | TL;DR uses cheaper/faster model (e.g., GPT-4o-mini), full summary uses premium model |
| Fallback chain | If LLM unavailable → extractive summarization via TextRank |

---

## 5. Web UX & Developer Workflows

### 5.1 Core Feed

```
┌─────────────────────────────────────────────────────────────────┐
│  [InsightHub]  Feed  Topics  Digest  Spotlight  Search  [👤]    │
├─────────────────────────────────────────────────────────────────┤
│  ▼ Filters                                                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Sources: ☑All  ☑Anthropic  ☑Meta  ☑ByteByteGo  ☑Oracle    │ │
│  │ Categories: ☑Breakthrough  ☑Debugging  ☑Architecture       │ │
│  │ Date: [Last 7 days ▼]  Score: [50+]  Difficulty: [Any ▼]   │ │
│  │ [Apply]  [Reset]  [Save as View...]                         │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  Sort: 🔥 Trending  ·  Latest  ·  Top Rated  ·  [Custom...]     │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ 🔥 BREAKTHROUGH · Anthropic · 5 min · ⭐92         [👍23]  │ │
│  │ Claude 4 achieves 97.3% on MATH benchmark, surpassing      │ │
│  │ GPT-5 by 2.1 points.                                       │ │
│  │ [▶ Expand]  [🔖]  [🔗]  [➕ More like this]               │ │
│  └─────────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ 🐛 DEBUGGING · Meta Engineering · 12 min · ⭐87   [👍15]   │ │
│  │ How a single null pointer caused 15% latency spike across  │ │
│  │ Meta's CDN edge nodes.                                     │ │
│  │ [▶ Expand]  [🔖]  [🔗]  [➕ More like this]               │ │
│  └─────────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ 🏗️ ARCHITECTURE · ByteByteGo · 8 min · ⭐78     [👍11]     │ │
│  │ Why Uber moved from microservices to well-defined           │ │
│  │ monoliths for core ride-matching logic.                     │ │
│  │ [▶ Expand]  [🔖]  [🔗]  [➕ More like this]               │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  [Load more...]                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Topics View

```
┌─────────────────────────────────────────────────────────────────┐
│  Topics                                                          │
│                                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ 🚀       │ │ 🐛       │ │ 🏗️       │ │ 📝       │           │
│  │ Break-   │ │ Debugging│ │ Archi-   │ │ Tutorial │           │
│  │ through  │ │ War Story│ │ tecture  │ │          │           │
│  │ 47 items │ │ 32 items │ │ 28 items │ │ 19 items │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ 📄       │ │ 📦       │ │ 💭       │ │ ⭐       │           │
│  │ Paper    │ │ Release  │ │ Opinion  │ │ All-Time │           │
│  │ Summary  │ │ Notes    │ │          │ │ Best     │           │
│  │ 15 items │ │ 22 items │ │ 11 items │ │ 99 items │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│                                                                  │
│  ── Selected: Breakthrough ──▶                                 │
│                                                                  │
│  🔥 Breakthroughs — This Week                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Anthropic · Claude 4 MATH 97.3% · ⭐92      [👍23]     │    │
│  │ [▶ Expand]  [🔖]                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ OpenAI · GPT-5 vision latency cut 40% · ⭐88 [👍18]    │    │
│  │ [▶ Expand]  [🔖]                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Related: #llm  #inference  #benchmark                          │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 Digest Engine

```
┌─────────────────────────────────────────────────────────────────┐
│  Digest Settings                                                 │
│                                                                  │
│  Frequency: [Daily ▼]  Day: [Any day ▼]  Time: [08:00 ▼]       │
│                                                                  │
│  Categories: ☑ Breakthrough  ☑ Debugging  ☑ Architecture       │
│              ☑ Paper Summary  ☐ Tutorial  ☐ Release Notes      │
│                                                                  │
│  Min Score: [60]  Max Items: [10]                                │
│                                                                  │
│  Sources: ☑ All  |  Exclude: [__________________]               │
│                                                                  │
│  Delivery: ☑ In-App  ☑ Email  ☐ Slack  ☐ Discord              │
│                                                                  │
│  [Save Settings]  [Preview Digest]                               │
│                                                                  │
│  ── Digest Preview (Tue, Jul 28, 2026) ──                      │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 🔥 BREAKTHROUGH — Claude 4 MATH 97.3%                   │    │
│  │ ⭐92 · Anthropic · 5 min read                           │    │
│  │ Claude 4 achieves 97.3% on MATH benchmark...            │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 🐛 DEBUGGING — Meta CDN null pointer incident           │    │
│  │ ⭐87 · Meta Engineering · 12 min read                   │    │
│  │ How a single null pointer caused 15% latency spike...   │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 🏗️ ARCHITECTURE — Uber monolith revival                │    │
│  │ ⭐78 · ByteByteGo · 8 min read                          │    │
│  │ Why Uber moved from microservices to...                 │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 5.4 Spotlight Sections

| Spotlight | Criteria | Refresh | Placement |
|---|---|---|---|
| **Breakthroughs of the Week** | Top 3-5 items, category=breakthrough, score > 80 | Weekly, Monday | Homepage hero section |
| **Debugging War Stories** | Category=debugging-war-story, score > 70 | Weekly, Thursday | Sidebar + dedicated tab |
| **Hidden Gems** | Score > 70 but saves < 10 (under-engaged) | Daily | Bottom of feed, "Did you miss?" |
| **Trending Now** | Highest velocity (saves/hour over 24h) | Every 4h | Top of feed + banner |
| **Classic Must-Reads** | All-time high score, curated manually | Monthly refresh | "Library" tab |

### 5.5 Watchlists & Alerts

```
┌─────────────────────────────────────────────────────────────────┐
│  Watchlists & Alerts                                             │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ My Watchlists                                            │    │
│  │                                                          │    │
│  │  📡 Anthropic — 3 new items since last visit       [🔔] │    │
│  │  📡 ML Infrastructure — 1 new item                 [🔔] │    │
│  │  📡 SRE Incident Reports — 2 new items             [🔔] │    │
│  │                                                          │    │
│  │  [+ Create Watchlist]                                     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ── Create Watchlist ──▶                                       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Name: [ML Infrastructure                         ]      │    │
│  │                                                          │    │
│  │ Sources: ☑All  ☑Anthropic  ☑OpenAI  ☐Meta               │    │
│  │                                                          │    │
│  │ Topics: ☑Breakthrough  ☑Architecture  ☐Tutorial         │    │
│  │                                                          │    │
│  │ Keywords: [inference, training, GPU, distributed]        │    │
│  │                                                          │    │
│  │ Min Score: [70]                                          │    │
│  │                                                          │    │
│  │ Notify via: ☑In-App  ☑Email  ☐Slack  ☐Webhook          │    │
│  │                                                          │    │
│  │ [Save Watchlist]                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 5.6 Search & Discovery

```
┌─────────────────────────────────────────────────────────────────┐
│  Search                                                          │
│                                                                  │
│  [┌─────────────────────────────────────────────────────────┐]  │
│  [│ sparse attention architecture inference speed    ⌕      │]  │
│  [└─────────────────────────────────────────────────────────┘]  │
│                                                                  │
│  [Semantic Search ▼]  [Last 30 days ▼]  [All Sources ▼]        │
│                                                                  │
│  Results (12)                                                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 🔥 Claude 4 Sparse Attention — Anthropic                │    │
│  │ ⭐92 · 5 min · Jul 26, 2026                             │    │
│  │ Claude 4 introduces a novel sparse attention mechanism  │    │
│  │ that reduces KV cache size by 60% while maintaining...  │    │
│  │ [▶ Expand]  [🔖]                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 🏗️ Efficient Transformer Architectures — ByteByteGo    │    │
│  │ ⭐85 · 8 min · Jul 20, 2026                             │    │
│  │ A visual deep dive into sparse, linear, and flash       │    │
│  │ attention mechanisms...                                 │    │
│  │ [▶ Expand]  [🔖]                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Search syntax:                                                  │
│  source:anthropic category:breakthrough score:>80 since:2026-06  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.7 Detail Page

```
┌─────────────────────────────────────────────────────────────────┐
│  [Back to Feed]  [InsightHub]  Feed  Topics  Digest  [👤]       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🔥 BREAKTHROUGH                                                │
│                                                                  │
│  Claude 4 achieves 97.3% on MATH benchmark, surpassing          │
│  GPT-5 by 2.1 points                                            │
│                                                                  │
│  Anthropic · Jul 26, 2026 · 5 min read · ⭐92                   │
│                                                                  │
│  [👍 23]  [🔖 Save]  [🔗 Share]  [📋 Copy Link]               │
│                                                                  │
│  ──────────────────────────────────────────────────────────     │
│                                                                  │
│  📋 Key Takeaways                                               │
│  • 97.3% accuracy on MATH (↑2.1 vs GPT-5)                      │
│  • 4x faster inference than Claude 3                            │
│  • New sparse attention architecture reduces KV cache 60%       │
│                                                                  │
│  📄 Full Summary                                                 │
│  Anthropic has released Claude 4, achieving a state-of-the-art  │
│  97.3% accuracy on the MATH benchmark... [2 more paragraphs]     │
│                                                                  │
│  💡 Why This Matters                                             │
│  This is the first time a model has crossed the 97% threshold   │
│  on MATH, signaling that LLM reasoning capabilities are         │
│  approaching expert-level mathematical proficiency.             │
│                                                                  │
│  🤔 Jargon                                                      │
│  • sparse attention — technique where model focuses only on     │
│    relevant input parts, reducing computation                   │
│  • KV cache — key-value cache that stores attention            │
│    computations for faster inference                            │
│                                                                  │
│  🔗 Original Source                                             │
│  [Read Full Blog Post →]  anthropic.com/blog/claude-4           │
│                                                                  │
│  ──────────────────────────────────────────────────────────     │
│                                                                  │
│  📎 Related Findings                                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 🏗️ Efficient Transformer Architectures — ByteByteGo    │    │
│  │ A visual deep dive into modern attention mechanisms...   │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 📝 Fine-tuning Claude 4 for Code Generation — Tutorial   │    │
│  │ Step-by-step guide to adapt Claude 4 for your codebase   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  💬 Community Notes (2)                                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ @mikewu — "Note: MATH benchmark results have high       │    │
│  │ variance (±1.5%). Take exact numbers with a grain of    │    │
│  │ salt." [👍5]                                            │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 5.8 Personalization Engine

```
┌─────────────────────────────────────────────────────────────────┐
│  Personalization Flow                                           │
│                                                                  │
│  ┌──────────┐    ┌──────────────┐    ┌────────────────────┐    │
│  │ Onboarding│───▶│  Implicit    │───▶│  Explicit           │    │
│  │ Survey    │    │  Signals     │    │  Feedback           │    │
│  └──────────┘    └──────────────┘    └────────────────────┘    │
│       │                │                      │                 │
│       ▼                ▼                      ▼                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  User Profile                                            │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │   │
│  │  │ Topic Weight  │  │ Source       │  │ Difficulty   │  │   │
│  │  │ Vector        │  │ Affinity     │  │ Preference   │  │   │
│  │  │ [LLM: 0.8]   │  │ [Anth: 0.9]  │  │ [Intermed]   │  │   │
│  │  │ [Infra: 0.3] │  │ [Meta: 0.6]  │  │              │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Feed Re-ranking                                       │   │
│  │  Base score × personalization boost per item           │   │
│  │  Personalization = cosine_sim(item_tags, user_vector)  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Implicit Signals Collected:                                    │
│  ┌──────────────┬──────────────────────┬──────────────────┐     │
│  │ Signal        │ Measurement          │ Decay             │    │
│  ├──────────────┼──────────────────────┼──────────────────┤    │
│  │ Dwell time    │ > 30s = positive     │ 7-day half-life  │    │
│  │ Scroll depth  │ > 80% = positive     │ 7-day half-life  │    │
│  │ Expand rate   │ Expanded = positive  │ 14-day half-life │    │
│  │ Bookmark      │ Strong positive      │ No decay         │    │
│  │ Hide          │ Strong negative      │ 30-day half-life │    │
│  └──────────────┴──────────────────────┴──────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Collaboration & Social Features

### Collections
- Create named collections (e.g., "System Design Interview Prep", "LLM Papers Q3 2026")
- Add items with optional personal notes
- Public / private / team-only visibility
- Collaborative collections with shared editing

### Social Actions
| Action | Visibility | Notification |
|---|---|---|
| Upvote | Public | N/A |
| Save to collection | Public/Private | N/A |
| Share | External link | N/A |
| Comment on item | Public (on detail page) | To author |
| Follow user | Private | When they save new item |
| React (🔥 😄 🤯 💡) | Public | N/A |

### Activity Feed
- "People you follow saved: ..."
- "Trending in your network"
- Weekly leaderboard: most saves by users in your team

---

## 7. Tech Stack & Operations

### Suggested Stack

| Layer | Technology | Rationale |
|---|---|---|
| **Frontend** | Next.js (React + SSR) + Tailwind CSS | SEO-friendly, good DX, fast iteration |
| **Backend API** | FastAPI (Python) or Go | FastAPI for ML integration ease; Go for performance |
| **Database** | PostgreSQL + PgVector | Relational data + semantic search in one DB |
| **Cache** | Redis | Feed cache, session store, rate limiting |
| **Queue** | Celery + Redis / Bull + Redis | Background scraping and summarization jobs |
| **Object Storage** | S3 / GCS / MinIO | Raw content, images, exports |
| **LLM** | OpenAI / Anthropic API + open-source fallback (Llama, Mistral) | Summarization, classification, glossary generation |
| **Search** | PostgreSQL FTS + PgVector hybrid | Combined keyword + semantic search |
| **Monitoring** | Sentry + Grafana + Prometheus | Error tracking, metrics, dashboards |
| **CI/CD** | GitHub Actions | Build, test, deploy pipeline |

### Infrastructure Diagram

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Browser │    │  CDN     │    │  LB      │    │  API     │
│  (React) │───▶│ (Vercel) │───▶│  (NGINX) │───▶│  Servers │
└──────────┘    └──────────┘    └──────────┘    └────┬─────┘
                                                      │
                                                      ▼
                                            ┌──────────────────┐
                                            │  Application     │
                                            │  Logic Layer     │
                                            │  (FastAPI/Go)    │
                                            └──┬────┬────┬────┘
                                               │    │    │
                          ┌────────────────────┘    │    └────────────┐
                          ▼                         ▼                 ▼
                   ┌────────────┐          ┌────────────┐    ┌──────────────┐
                   │ PostgreSQL │          │   Redis    │    │  Queue       │
                   │ + PgVector │          │   Cache    │    │ (Celery/Bull)│
                   └────────────┘          └────────────┘    └──────┬───────┘
                                                                     │
                          ┌──────────────────────────────────────────┘
                          ▼
                   ┌──────────────┐
                   │  Workers     │
                   │  Scraping    │
                   │  Summarizing │
                   │  Classifying │
                   └──────┬───────┘
                          │
                          ▼
                   ┌──────────────┐
                   │  LLM APIs    │
                   │  + Object    │
                   │  Storage     │
                   └──────────────┘
```

### Scaling Considerations

| Bottleneck | Mitigation | At What Scale |
|---|---|---|
| Scraping throughput | Distributed scrapers, rotating proxies, cache-aware polling | > 500 sources |
| LLM API costs | Caching, batch processing, model tiering, open-source fallback | > 10k items/day |
| Feed personalization | Pre-computed user vectors, materialized feed view, CDN edge caching | > 10k users |
| Search latency | PgVector index tuning, read replicas, query result caching | > 100k items |
| Email digests | Template pre-rendering, batch send via SES/SendGrid | > 10k digests/day |

### Rate Limiting & Legal
- Respect `robots.txt` and `Crawl-Delay` directives
- Cache-friendly polling intervals per source
- Rate limit per source domain (max 1 req/10s)
- Source attribution: always link to original, show excerpt not full content
- Fair use: summaries are transformative, limited excerpts only
- DMCA takedown mechanism for content removal requests

---

## 8. Phased Delivery Plan

### Phase 1 — MVP (Weeks 1-4)

| Week | Focus | Deliverables |
|---|---|---|
| 1 | Scraping & Ingestion | RSS scraper for top 10 sources, raw content storage, dedup pipeline |
| 2 | LLM Summarization | 4-layer summarization pipeline, basic categorization, glossary generation |
| 3 | Web App — Core Feed | Auth, feed view with cards, expand/collapse, save/bookmark, basic search |
| 4 | Digest & Polish | Daily digest engine, email delivery, filter sidebar, polish feed UX |

**Phase 1 Outcome**: User can browse feed of top findings from 10 sources, read progressive summaries, save items, and receive daily email digest.

### Phase 2 — Curation & Personalization (Weeks 5-8)

| Week | Focus | Deliverables |
|---|---|---|
| 5 | Scoring Engine | Full formula integration, recency decay, source tiers, signal collection |
| 6 | Personalization | Onboarding survey, implicit signal tracking, feed re-ranking, preference reset |
| 7 | Spotlight Sections | Breakthroughs of Week, Debugging War Stories, Trending Now, Hidden Gems |
| 8 | Watchlists & Alerts | Watchlist CRUD, notification settings, Slack/Discord webhook, in-app notification center |

**Phase 2 Outcome**: Personalized feed with scored items, curated spotlights, and configurable alerts.

### Phase 3 — Community & Scale (Weeks 9-12)

| Week | Focus | Deliverables |
|---|---|---|
| 9 | Collections & Social | Public profiles, collections, collaborative lists, comments, reactions |
| 10 | Search v2 | Semantic search (PgVector), search syntax, saved searches |
| 11 | Source Expansion | Web scraper for 20+ additional sources, YouTube API integration, newsletter email parser |
| 12 | Performance & Infrastructure | Load testing, caching optimization, monitoring setup, admin dashboard |

**Phase 3 Outcome**: Community features, full semantic search, 30+ sources ingested, production-ready infrastructure.

---

## 9. Open Questions for Design Discussion

| Area | Question |
|---|---|
| **Scoring** | Should user feedback from newsletters be weighted equally to in-platform feedback? |
| **LLM** | Do we risk homogenizing summaries across sources? How to preserve source voice? |
| **Personalization** | Opt-in vs. default-on personalization? How to avoid filter bubbles? |
| **Monetization** | Freemium vs. subscription vs. free? What goes behind the paywall? |
| **Moderation** | Automated vs. manual moderation for community notes? |
| **Legal** | Are we comfortable with web scraping as primary ingestion method, or should we pursue partnerships? |
| **Mobile** | Mobile web vs. native app for Phase 4? |
| **Languages** | English-only MVP or multilingual support later? |

---

## Appendix: ASCII System Diagrams

### Data Flow Diagram

```
User Actions
     │
     ▼
┌────────────────────────────────────────────────────────────┐
│                    WEB APPLICATION                           │
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌────────┐  ┌──────────────┐  │
│  │ Browse  │  │ Search  │  │ Digest │  │ Configure    │  │
│  │ Feed    │  │         │  │ Subscribe│  │ Watchlists  │  │
│  └────┬────┘  └────┬────┘  └───┬────┘  └──────┬───────┘  │
│       │            │           │              │           │
│       ▼            ▼           ▼              ▼           │
│  ┌────────────────────────────────────────────────────┐   │
│  │              API Layer (FastAPI / Go)               │   │
│  └────┬───────────────┬────────────────┬──────────────┘   │
│       │               │                │                  │
└───────┼───────────────┼────────────────┼──────────────────┘
        │               │                │
        ▼               ▼                ▼
   ┌──────────┐   ┌──────────┐   ┌──────────────┐
   │ PostgreSQL│   │  Redis   │   │  Background  │
   │+PgVector │   │  Cache   │   │  Queue       │
   └──────────┘   └──────────┘   └──────┬───────┘
                                        │
                                        ▼
                              ┌────────────────────┐
                              │  Worker Processes    │
                              │                      │
                              │  ┌────────────────┐  │
                              │  │ Scraper Worker │  │
                              │  └───────┬────────┘  │
                              │          │            │
                              │  ┌───────▼────────┐  │
                              │  │ Classifier      │  │
                              │  │ Worker          │  │
                              │  └───────┬────────┘  │
                              │          │            │
                              │  ┌───────▼────────┐  │
                              │  │ Summarizer      │  │
                              │  │ Worker          │  │
                              │  └───────┬────────┘  │
                              │          │            │
                              │  ┌───────▼────────┐  │
                              │  │ Scorer Worker  │  │
                              │  └────────────────┘  │
                              └────────────────────┘
                                        │
                                        ▼
                              ┌────────────────────┐
                              │  External APIs      │
                              │  - LLM Providers    │
                              │  - YouTube Data     │
                              │  - RSS Feeds        │
                              │  - Web Scrape       │
                              └────────────────────┘
```

### Feed Rendering Flow

```
Page Load
    │
    ▼
┌─────────────────────────────┐
│ Fetch User Profile          │
│ (topic vector, preferences) │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Query Items (SQL + PgVector)│
│ WHERE score >= threshold    │
│ AND date >= user timeframe  │
│ ORDER BY personalized_score │
│ LIMIT 20                    │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Cache Check (Redis)         │
│ If cached result exists:    │
│   return cached cards       │
│ Else:                       │
│   fetch from DB             │
│   render cards              │
│   cache for 5 minutes       │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Hydrate Cards               │
│ - Attach TL;DR              │
│ - Inject jargon tooltips    │
│ - Check bookmark status     │
│ - Attach reaction counts    │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Render Feed (React/Next.js) │
│ - Responsive grid           │
│ - Infinite scroll trigger   │
└─────────────────────────────┘
```

### Digest Generation Flow

```
Scheduler (Cron: Daily 07:00)
    │
    ▼
┌─────────────────────────────────────┐
│ Fetch all users with digest enabled │
└──────────────┬──────────────────────┘
               │
               ▼ (batch)
┌─────────────────────────────────────┐
│ For each user:                      │
│   ┌─────────────────────────────┐   │
│   │ Apply user preferences:     │   │
│   │ - chosen categories         │   │
│   │ - min score threshold       │   │
│   │ - excluded sources          │   │
│   │ - max items count           │   │
│   └──────────┬──────────────────┘   │
│              ▼                       │
│   ┌─────────────────────────────┐   │
│   │ Query items from last 24h   │   │
│   │ Score >= user threshold     │   │
│   │ Limit N items               │   │
│   └──────────┬──────────────────┘   │
│              ▼                       │
│   ┌─────────────────────────────┐   │
│   │ Render digest template      │   │
│   │ (HTML or Markdown)          │   │
│   └──────────┬──────────────────┘   │
│              │                       │
└──────────────┼───────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Batch send via email provider       │
│ (SES / SendGrid / Resend)           │
│ + Store digest in-app archive       │
└─────────────────────────────────────┘
```

### Categorization Pipeline

```
Raw Content
    │
    ▼
┌─────────────────────────────────────┐
│ Feature Extraction                  │
│ - Word count                        │
│ - Code block detection              │
│ - Diagram/image detection           │
│ - Keyword frequency analysis        │
│ - Narrative structure score         │
│ - Readability index (Flesch)        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Rule-Based Classification           │
│                                     │
│ IF contains "breakthrough" /        │
│    "state-of-the-art" / "first"     │
│    + high technical density         │
│    → breakthrough (confidence: 0.7) │
│                                     │
│ IF contains "incident" /            │
│    "postmortem" / "root cause" /    │
│    "mitigation" + narrative style   │
│    → debugging-war-story (0.8)      │
│                                     │
│ IF contains architecture diagrams   │
│    + system design language         │
│    → architecture (0.75)            │
│                                     │
│ IF step-by-step + code examples     │
│    → tutorial (0.8)                 │
│                                     │
│ Default → uncategorized             │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ LLM Verification                    │
│ "Given this content and initial     │
│  classification, do you agree?      │
│  Respond with: confirm / override   │
│  + confidence score"                │
│                                     │
│ If LLM confidence < 0.5 →           │
│   move to manual review queue       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Store final category + confidence   │
│ Index in database                   │
└─────────────────────────────────────┘
```

---

*This document represents the complete product plan for InsightHub. Use it as the basis for design discussions, sprint planning, and technical specification.*
