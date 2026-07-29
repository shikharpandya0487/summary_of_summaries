# InsightHub — Technical TODO

## Phase 1: Ingestion (Day 1)
- [ ] RSS feed polling (cron, 15min)
- [ ] Parse RSS/Atom → extract title, URL, date, content
- [ ] HTML-to-text extraction
- [ ] Dedup by URL + content hash
- [ ] Store findings in SQLite

## Phase 2: Summarisation (Day 1-2)
- [ ] LLM API integration for TL;DR (1 sentence)
- [ ] Key takeaways (3-5 bullets)
- [ ] Full summary (2-3 paragraphs)
- [ ] Jargon detection + auto-glossary

## Phase 3: Scoring & Curation (Day 2)
- [ ] Scoring formula (recency, authority, quality, signal)
- [ ] Quality gate: discard score < 60
- [ ] Auto-categorisation (keyword heuristics)
- [ ] Spotlight detection (score > 80)

## Phase 4: Web App (Day 2-3)
- [ ] Feed view with infinite scroll
- [ ] Detail view (TL;DR, takeaways, glossary)
- [ ] Filter by source (URL state)
- [ ] Search with debounce
- [ ] Bookmark toggle (localStorage)
- [ ] Auto-refresh banner (5min poll)
- [ ] Responsive layout

## Phase 5: Polish (Day 3)
- [ ] Dark mode
- [ ] Upvote + most-upvoted sort
- [ ] Breakthrough spotlight section
- [ ] Shareable permalinks
- [ ] Loading/error/empty states

## Phase 6: Post-MVP
- [ ] User accounts (email/OAuth)
- [ ] Synced bookmarks across devices
- [ ] Personalised feed (For You tab)
- [ ] Email digest (daily/weekly)
- [ ] Slack/Discord webhooks
- [ ] Watchlist alerts
