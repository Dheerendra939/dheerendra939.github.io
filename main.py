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

        # Open local index.html
        file_path = "file://" + os.path.abspath("index.html")
        print(f"📄 Opening: {file_path}")
        await page.goto(file_path)

        # Wait for JavaScript in index.html to finish (adjust timeout if needed)
        await page.wait_for_timeout(5000)

        # Extract all anchor tag hrefs
        links = await page.eval_on_selector_all("a", "els => els.map(a => a.href)")
        print(f"🔗 Found {len(links)} external links.")

        for i, link in enumerate(links, start=1):
            print(f"\n🌐 Visiting link {i}/{len(links)}: {link}")
            try:
                await page.goto(link, timeout=20000)
                content = await page.content()

                # Save HTML content
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
