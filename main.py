import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    output_dir = "scraped_pages"
    os.makedirs(output_dir, exist_ok=True)

    print("🚀 Launching Chromium in headless mode...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Open local index.html and wait for JS to load fully
        file_path = "file://" + os.path.abspath("index.html")
        print(f"📄 Opening: {file_path}")
        await page.goto(file_path, wait_until="networkidle")

        # Wait until links appear
        try:
            await page.wait_for_selector("a[href]", timeout=20000)
        except:
            print("⚠️ No links appeared within 20 seconds.")

        # Collect links from all frames
        all_links = set()
        for frame in page.frames:
            links = await frame.eval_on_selector_all("a", "els => els.map(a => a.href)")
            all_links.update(links)

        print(f"🔗 Found {len(all_links)} external links: {list(all_links)}")

        for i, link in enumerate(all_links, start=1):
            print(f"\n🌐 Visiting link {i}/{len(all_links)}: {link}")
            try:
                await page.goto(link, timeout=20000)
                content = await page.content()
                filename = os.path.join(output_dir, f"page_{i}.html")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Saved {link} → {filename}")
            except Exception as e:
                print(f"❌ Error visiting {link}: {e}")

        await browser.close()
        print("\n🏁 Done! All pages visited and saved.")

if __name__ == "__main__":
    asyncio.run(main())
