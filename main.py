import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    url = "https://dheerendra939.github.io"
    print(f"🚀 Launching Chromium in headless mode...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print(f"🌐 Opening: {url}")
        await page.goto(url, wait_until="networkidle")

        # Wait up to 30s for dynamic content
        await page.wait_for_timeout(30000)

        # Function to extract link candidates from a frame
        async def extract_clickables(frame):
            selectors = [
                "a[href]",                    # normal links
                "button",                     # buttons
                "[onclick]",                  # any element with onclick handler
                "[data-link]",                 # custom data-link
                "div[role='button']"           # div acting as a button
            ]
            selector_union = ", ".join(selectors)
            elements = await frame.query_selector_all(selector_union)
            clickables = []
            for el in elements:
                try:
                    href = await el.get_attribute("href")
                    onclick = await el.get_attribute("onclick")
                    data_link = await el.get_attribute("data-link")
                    text = (await el.inner_text())[:50]
                    link = href or data_link or onclick or text
                    clickables.append((el, link))
                except:
                    pass
            return clickables

        # Collect from main page and all iframes
        all_frames = [page] + page.frames
        all_clickables = []

        for frame in all_frames:
            print(f"\n🔍 Checking frame: {frame.url}")
            clickables = await extract_clickables(frame)
            print(f"   Found {len(clickables)} clickable elements.")
            all_clickables.extend(clickables)

        if not all_clickables:
            print("⚠️ No clickable elements found on the page.")
        else:
            print(f"\n🔗 Total clickable elements found: {len(all_clickables)}")

            # Click each clickable safely
            os.makedirs("clicked_pages", exist_ok=True)
            for i, (element, desc) in enumerate(all_clickables, start=1):
                try:
                    print(f"🖱️ [{i}/{len(all_clickables)}] Clicking: {desc}")
                    await element.click(timeout=5000)
                    await page.wait_for_timeout(2000)  # wait for any redirects or popups
                    path = f"clicked_pages/page_{i}.html"
                    content = await page.content()
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"✅ Saved {path}")
                except Exception as e:
                    print(f"❌ Skipped {desc} due to: {e}")

        await browser.close()
        print("\n🏁 Done! All clickable elements were tested and saved.")

if __name__ == "__main__":
    asyncio.run(main())
