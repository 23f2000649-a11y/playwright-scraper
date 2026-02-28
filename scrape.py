import asyncio
from playwright.async_api import async_playwright
import re

async def run():
    async with async_playwright() as p:
        # Launch headless browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        total_sum = 0
        
        # Iterating through seeds 43 to 52
        for seed in range(43, 53):
            url = f"https://21f1003821.pythonanywhere.com/playwright/seed/{seed}"
            print(f"Opening: {url}")
            
            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Extract all text from table data (td) tags
                cells = await page.locator("td").all_inner_texts()
                
                for text in cells:
                    # Remove anything that isn't a digit or a decimal point
                    clean_val = re.sub(r'[^\d.]', '', text.strip())
                    if clean_val:
                        try:
                            total_sum += float(clean_val)
                        except ValueError:
                            continue
            except Exception as e:
                print(f"Error on {seed}: {e}")

        print("\n" + "="*20)
        print(f"FINAL_TOTAL_SUM: {total_sum}")
        print("="*20)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
