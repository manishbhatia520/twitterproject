import asyncio
from scraping.manager import ScraperManager

# Load accounts, backup_accounts, proxies from your config or file
accounts = [...]  # List of dicts with auth_token, cookies, user_agent, username
backup_accounts = [...]  # List of backup accounts
proxies = [...]  # List of proxy strings
storage_queue = []

async def main():
    manager = ScraperManager(accounts, backup_accounts, proxies, storage_queue)
    # Repeat 5 times for 500 accounts (100 in parallel)
    for _ in range(5):
        await manager.run(num_workers=100)
        # Wait for Twitter API ratelimit reset (15 min)
        await asyncio.sleep(15 * 60)

if __name__ == "__main__":
    asyncio.run(main())
