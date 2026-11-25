# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/aijaz52/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/aijaz52/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

![canvas: 1024 × 1024](badges/canvas.svg) ![stories: 40 · UTC](badges/stories.svg) ![assets: self-contained](badges/assets.svg)

Forty reports from the supplied Wednesday 25 November 2026 brief in one 1024×1024 news front page: a dominant date masthead, a one-line day summary, and four columns of numbered reports with UTC times, source tags, theme tags, headlines, and details. The editorial sequence follows the supplied brief; the first card identifies Putin's 24 November remarks as a carry-over into this edition.

[`news.html`](news.html) is self-contained, with inline CSS and no external assets. Its 1,000px content area holds four 241px columns and three 12px gutters, inside 12px page margins. The fixed grid places the theme strip immediately after the summary and fits the masthead, all 40 reports, and the footer into 1,024px of height.

`main.ts` copies the rendered [`entry.png`](entry.png) byte-identically to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).

## Run it

Rendering requires Python, Playwright, and its Chromium browser (`python3 -m pip install playwright` and `python3 -m playwright install chromium`). Node.js 22.18 or later runs the entry point directly.

```sh
python3 render.py && MAKEFUN_OUTPUT_DIR=out node main.ts
```

The renderer uses a 1024×1024 viewport and a device scale factor of 1. Before capturing the image, it checks all 40 numbered cards, UTC timestamps, one-line headlines and details, the exact footer, all nine theme tags, text boundaries, metadata overlap, and the absence of external asset requests. It fails rather than saving an image with clipping or overflow. The page uses system fonts; the checked-in image was rendered with DejaVu Sans and DejaVu Sans Mono.

---

<sub>Entered on [make.fun](https://make.fun/?ref=bsdfw3nf&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
