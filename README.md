# InsightHub

**Curated engineering intelligence — read ten posts in five minutes.**

1.5-day build for 2 developers. Anonymous-first — no login required.

> Built for busy developers who want to stay on top of the best engineering content without spending hours browsing blogs, newsletters, and social media.

---

## Repository Structure

```
├── README.md
├── docs/
│   ├── insighthub-product-definition.md   — Full product spec, scoring, tech stack, plan
│   ├── insighthub-plan.md                 — Detailed system design & UX flows
│   ├── TODO-tech.md                       — Build checklist (1.5 days)
│   └── pitch-script.md                    — 3-4 minute pitch (2 speakers)
├── diagrams/
│   ├── insighthub-design.excalidraw       — Product design whiteboard
│   ├── insighthub-hld.excalidraw          — High-level design diagram
│   ├── insighthub-tech-hld.excalidraw     — Technical HLD + architecture
│   └── final-hld.excalidraw              — Final HLD export
└── scripts/
    ├── generate_excalidraw.py             — Generates insighthub-design.excalidraw
    └── generate_hld.py                    — Generates insighthub-hld.excalidraw
```

Open `.excalidraw` files at [excalidraw.com](https://excalidraw.com).

---

## Quick Start

```bash
# Regenerate diagrams after editing generators
cd scripts
python generate_hld.py
python generate_excalidraw.py
```

---

## License

MIT
