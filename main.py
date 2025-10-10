import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    url = "https://dheerendra939.github.io"
    output_dir = "clicked_pages"
    os.makedirs(output_dir, exist_ok=True)

    print("🚀 Launching Chromium in headless mode...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Log browser console messages (optional, helps debugging)
        page.on("console", lambda msg: print("🖥️", msg.text))

        print(f"🌐 Opening: {url}")
        await page.goto(url, wait_until="networkidle")

        # Wait for the ad script / dynamic content to load
        await page.wait_for_timeout(15000)  # 15 seconds (adjust if needed)

        # Wait until at least one clickable element appears
        try:
            await page.wait_for_selector(
                "a[href], button, [onclick], [data-link], div[role='button']", 
                timeout=20000
            )
        except:
            print("⚠️ No clickable elements appeared after waiting.")

        # Function to extract clickable elements
        async def extract_clickables(frame):
            selectors = [
                "a[href]",
                "button",
                "[onclick]",
                "[data-link]",
                "div[role='button']"
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
                    desc = href or data_link or onclick or text
                    clickables.append((el, desc))
                except:
                    pass
            return clickables

        # Collect clickables from main page and all frames
        all_frames = [page] + page.frames
        all_clickables = []

        for frame in all_frames:
            clickables = await extract_clickables(frame)
            all_clickables.extend(clickables)

        print(f"🔗 Total clickable elements found: {len(all_clickables)}")

        # Click each element and save resulting page
        for i, (element, desc) in enumerate(all_clickables, start=1):
            try:
                print(f"🖱️ [{i}/{len(all_clickables)}] Clicking: {desc}")
                await element.click(timeout=5000)
                await page.wait_for_timeout(2000)  # wait for any changes
                html_content = await page.content()
                file_path = os.path.join(output_dir, f"page_{i}.html")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"✅ Saved {file_path}")
            except Exception as e:
                print(f"❌ Skipped {desc} due to error: {e}")

        await browser.close()
        print("\n🏁 Done! All dynamic elements clicked and pages saved.")

if __name__ == "__main__":
    asyncio.run(main())
