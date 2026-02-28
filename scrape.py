import asyncio
from playwright.async_api import async_playwright
import re

async def run():
    async with async_playwright() as p:
        # Launch browser (headless is required for GitHub Actions)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        total_sum = 0
        
        # Seeds 43 to 52
        for seed in range(43, 53):
            url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
            print(f"Visiting Seed {seed}...")
            
            try:
                # 1. Navigate and wait for network to settle
                await page.goto(url, wait_until="networkidle", timeout=60000)
                
                # 2. CRITICAL: Wait for at least one table cell (td) to be visible
                # The 'js_table' pages load content dynamically; we MUST wait.
                await page.wait_for_selector("td", timeout=10000)
                
                # 3. Extract all text from table cells
                cells = await page.locator("td").all_inner_texts()
                
                page_sum = 0
                for text in cells:
                    # Remove anything not a digit or decimal (handles Rs, $, commas)
                    clean_val = re.sub(r'[^\d.]', '', text.strip())
                    if clean_val and clean_val != ".":
                        try:
                            val = float(clean_val)
                            page_sum += val
                            total_sum += val
                        except ValueError:
                            continue
                
                print(f"  -> Seed {seed} subtotal: {page_sum}")
                
            except Exception as e:
                print(f"  -> Error or timeout on seed {seed}: {e}")

        # The Grader looks for this EXACT line in the GitHub Action Logs
        print("\n" + "="*30)
        print(f"TOTAL_SUM: {total_sum}", flush=True)
        print("="*30)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
