import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    output_dir = "scraped_pages"
    os.makedirs(output_dir, exist_ok=True)

    target_url = "https://dheerendra939.github.io"

    print(f"🚀 Launching Chromium in headless mode...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Log browser console messages (to debug JS loading)
        page.on("console", lambda msg: print("🖥️", msg.text))

        print(f"🌐 Opening: {target_url}")
        await page.goto(target_url, wait_until="networkidle")

        # Wait for some time to allow delayed JS (10–20 seconds)
        await page.wait_for_timeout(15000)

        # Wait for <a> links to appear
        try:
            await page.wait_for_selector("a[href]", timeout=20000)
        except:
            print("⚠️ No links found after waiting.")

        # Collect links (including dynamically loaded ones)
        all_links = await page.eval_on_selector_all("a", "els => els.map(a => a.href)")
        unique_links = list(set(all_links))

        print(f"🔗 Found {len(unique_links)} links:")
        for link in unique_links:
            print("  →", link)

        # Visit each link and save HTML
        for i, link in enumerate(unique_links, start=1):
            print(f"\n🕸️ Visiting {link}")
            try:
                await page.goto(link, wait_until="networkidle", timeout=30000)
                content = await page.content()
                filename = os.path.join(output_dir, f"page_{i}.html")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Saved HTML → {filename}")
            except Exception as e:
                print(f"❌ Failed to visit {link}: {e}")

        await browser.close()
        print("\n🏁 Done! All links visited and saved to 'scraped_pages'.")

if __name__ == "__main__":
    asyncio.run(main())
