import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


async def main():
    root = Path(__file__).resolve().parent
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox"])
        page = await browser.new_page(viewport={"width": 1024, "height": 1024}, device_scale_factor=1)
        await page.goto((root / "news.html").as_uri())
        await page.screenshot(path=str(root / "entry.png"))
        await browser.close()


asyncio.run(main())
