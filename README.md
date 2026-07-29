# InsightHub

**Curated engineering intelligence — read ten posts in five minutes.**

InsightHub ingests articles from top engineering blogs (ByteByteGo, Anthropic, Meta Engineering, and more), extracts the key findings, and presents them as a clean, browsable feed of concise summaries. No login required — the full core experience works instantly for anonymous visitors.

> Built for busy developers who want to stay on top of the best engineering content without spending hours browsing blogs, newsletters, and social media.

---

## Features

### Core — No Login Required

| Feature | Description |
|---|---|
| **Feed** | Latest findings sorted by date with infinite scroll (20 items/page) |
| **Detail View** | Full summary, key takeaways, and a link to the original article |
| **Filter by Source** | Checkbox filters for each active blog, shareable via URL |
| **Bookmarks** | Save items to read later — persisted in localStorage across sessions |
| **Search** | Real-time keyword search across titles, summaries, and source names |
| **Auto-Refresh** | Background polling every 5 minutes with a "New items available" banner |

### Nice-to-Have (Still Anonymous)

- **Auto-categorisation** — items tagged as breakthrough, debugging, architecture, etc.
- **Upvoting** — vote on findings; sort by "Most Upvoted"
- **Breakthroughs Spotlight** — curated section for major announcements
- **Dark mode** — theme toggle stored in localStorage

### Post-MVP (Requires Auth)

- Daily email digest
- User accounts with cross-device sync
- Personalised "For You" feed
- Follow sources and topics
- Slack / Discord integrations

---

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌────────────────┐
│   RSS Feeds     │────▶│   Poller Service │────▶│  SQLite DB     │
│ (ByteByteGo,    │     │  (cron, 15 min)  │     │  (Sources +    │
│  Anthropic,     │     │                  │     │   Findings)    │
│  Meta Eng, ...) │     └───────┬──────────┘     └───────┬────────┘
└─────────────────┘             │                        │
                                ▼                        ▼
                        ┌──────────────────┐     ┌────────────────┐
                        │  Summariser      │     │  Web App       │
                        │  (extracts key   │     │  (Feed +       │
                        │   takeaways)     │     │   Detail)      │
                        └──────────────────┘     └────────────────┘
```

### Tech Stack (MVP)

| Layer | Technology |
|---|---|
| **Frontend** | Responsive web — works on mobile & desktop |
| **Backend** | Lightweight server with RSS polling & summarisation |
| **Database** | SQLite — sources + findings |
| **Persistence** | localStorage for bookmarks & preferences |

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/shikharpandya0487/summary_of_summaries.git
cd insighthub

# Install dependencies
# TODO: add install command

# Run the app
# TODO: add run command
```

---

## Data Model

### Finding

| Field | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `title` | string | Article title |
| `source_name` | string | Blog name (e.g. "ByteByteGo") |
| `source_url` | string | Original article URL (unique) |
| `published_at` | datetime | Article publication date |
| `fetched_at` | datetime | When we polled the RSS feed |
| `summary_tldr` | text | 1-2 sentence summary |
| `summary_full` | text | 3-5 paragraph summary |
| `key_takeaways` | text[] | Array of bullet points |
| `category` | string | breakthrough, debugging, architecture, tutorial, release-notes, general |
| `upvotes` | integer | Default 0 |

### Source

| Field | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `name` | string | Display name (unique) |
| `rss_url` | string | RSS feed URL |
| `website_url` | string | Blog homepage |
| `is_active` | boolean | Currently polled? |
| `last_fetched_at` | datetime | Last successful poll |

---

## Roadmap

- [x] Product definition & design
- [ ] MVP: RSS polling + summarisation + feed + detail view
- [ ] MVP: Filter, search, bookmarks
- [ ] MVP: Auto-refresh, responsive design
- [ ] Post-MVP: Dark mode, upvoting, categorisation
- [ ] Post-MVP: Auth, email digests, personalised feeds

---

## License

MIT
