import asyncio
import json
import struct
from pathlib import Path

from playwright.async_api import async_playwright


LAYOUT_CHECK = """() => {
    const failures = [];
    const stories = [...document.querySelectorAll('.story')];
    const columns = [...document.querySelectorAll('.column')];
    const footer = document.querySelector('footer');
    const masthead = document.querySelector('h1');
    const expectedFooter = '40 stories. One day. 25 November 2026.';
    const expectedDate = 'WEDNESDAY 25 NOVEMBER 2026';
    if (stories.length !== 40) failures.push(`Expected 40 stories; got ${stories.length}`);
    if (columns.length !== 4 || columns.some(c => c.querySelectorAll('.story').length !== 10))
        failures.push('Expected four columns of ten stories');
    if (footer?.textContent.trim() !== expectedFooter) failures.push('Footer differs');
    if (masthead?.getAttribute('aria-label') !== expectedDate) failures.push('Masthead differs');
    if (document.querySelectorAll('script, link, img, iframe, video, audio, object').length)
        failures.push('Page must use inline CSS with no scripts or external assets');
    if ([...document.styleSheets].some(s => s.href)) failures.push('External stylesheet');
    if (document.documentElement.scrollWidth !== 1024 || document.documentElement.scrollHeight !== 1024)
        failures.push('Document overflows its 1024×1024 viewport');

    const tolerance = 0.75;
    const within = (a, b) => a.left >= b.left - tolerance && a.top >= b.top - tolerance
        && a.right <= b.right + tolerance && a.bottom <= b.bottom + tolerance;
    const viewport = { left: 0, top: 0, right: 1024, bottom: 1024 };
    const walker = document.createTreeWalker(document.querySelector('main'), NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
        if (!node.textContent.trim()) continue;
        const range = document.createRange();
        range.selectNodeContents(node);
        const bounds = range.getBoundingClientRect();
        const parent = node.parentElement;
        if (!within(bounds, viewport) || !within(bounds, parent.getBoundingClientRect()))
            failures.push(`Text exceeds its box: ${node.textContent.trim()}`);
        const card = parent.closest('.story');
        if (card && !within(bounds, card.getBoundingClientRect()))
            failures.push(`Text exceeds its story card: ${node.textContent.trim()}`);
    }

    const allTimes = [];
    stories.forEach((story, i) => {
        const number = story.querySelector('.number')?.textContent;
        const time = story.querySelector('time');
        if (number !== String(i + 1).padStart(2, '0')) failures.push(`Number mismatch at story ${i + 1}`);
        if (!time || !/^\\d{2}:\\d{2}Z$/.test(time.textContent)
            || time.dateTime !== `2026-11-25T${time.textContent.slice(0, 5)}:00Z`)
            failures.push(`Invalid UTC timestamp at story ${i + 1}`);
        else allTimes.push(time.dateTime);
        for (const selector of ['.source', '.topic', 'h3', 'p']) {
            const element = story.querySelector(selector);
            if (!element?.textContent.trim()) failures.push(`Missing ${selector} at story ${i + 1}`);
        }
        for (const selector of ['h3', 'p']) {
            const range = document.createRange();
            range.selectNodeContents(story.querySelector(selector));
            if (range.getClientRects().length !== 1) failures.push(`Wrapped ${selector} at story ${i + 1}`);
        }
        const metadata = [...story.querySelector('.meta').children];
        metadata.slice(1).forEach((element, j) => {
            if (metadata[j].getBoundingClientRect().right > element.getBoundingClientRect().left + tolerance)
                failures.push(`Overlapping metadata at story ${i + 1}`);
        });
    });
    if (allTimes.join() !== [...allTimes].sort().join()) failures.push('Stories are not in UTC order');
    const summaryRange = document.createRange();
    summaryRange.selectNodeContents(document.querySelector('.summary p'));
    if (summaryRange.getClientRects().length !== 1) failures.push('Day summary is not one line');
    const themes = ['WAR', 'UKRAINE', 'IRAN', 'MARKETS', 'EU', 'ASIA', 'AFRICA', 'SCIENCE', 'AMERICAS'];
    const tags = [...document.querySelectorAll('.topic')].map(t => t.textContent);
    for (const theme of themes) if (!tags.some(t => t.split(' / ').includes(theme))) failures.push(`Missing theme: ${theme}`);
    const headlineSize = parseFloat(getComputedStyle(document.querySelector('.calendar')).fontSize);
    const otherSizes = [...document.querySelectorAll('main *:not(h1):not(h1 *)')]
        .map(e => parseFloat(getComputedStyle(e).fontSize));
    if (headlineSize < 80 || otherSizes.some(s => s >= headlineSize)) failures.push('Date is not the largest type');
    return {
        failures,
        viewport: [innerWidth, innerHeight],
        columns: columns.map(c => c.getBoundingClientRect().width),
        stories: stories.length,
        footer: footer?.textContent,
        mastheadFontPx: headlineSize,
        externalRequests: performance.getEntriesByType('resource').map(r => r.name),
    };
}"""


async def main():
    root = Path(__file__).resolve().parent
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox"])
        try:
            page = await browser.new_page(viewport={"width": 1024, "height": 1024}, device_scale_factor=1)
            await page.goto((root / "news.html").as_uri(), wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            result = await page.evaluate(LAYOUT_CHECK)
            if result["externalRequests"]:
                result["failures"].append("Page loaded additional resources")
            if result["failures"]:
                raise RuntimeError(json.dumps(result, indent=2, ensure_ascii=False))
            png = await page.screenshot(path=str(root / "entry.png"), full_page=False, animations="disabled")
            dimensions = struct.unpack(">II", png[16:24])
            if dimensions != (1024, 1024):
                raise RuntimeError(f"Unexpected PNG dimensions: {dimensions}")
            result["pngPixels"] = list(dimensions)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        finally:
            await browser.close()


asyncio.run(main())
