import asyncio
import random
import aiohttp

class ScraperWorker:
    def __init__(self, account, proxy, desirability_only=False):
        self.account = account
        self.proxy = proxy
        self.desirability_only = desirability_only
        self.fingerprint_uses = 0
        self.max_fingerprint_uses = random.randint(5, 10)

    async def scrape(self, session, storage_queue):
        while True:
            try:
                if self.fingerprint_uses >= self.max_fingerprint_uses:
                    self.fingerprint_uses = 0
                    self.max_fingerprint_uses = random.randint(5, 10)
                    # Rotate fingerprint (implement as needed)
                headers = {
                    "Authorization": f"Bearer {self.account['auth_token']}",
                    "Cookie": self.account['cookies'],
                    "User-Agent": self.account['user_agent'],
                }
                query = "e"
                url = f"https://twitter.com/i/api/2/search/adaptive.json?q={query}"
                async with session.get(url, headers=headers, proxy=f"http://{self.proxy}", timeout=30) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        # Optionally filter for desirability labels
                        if self.desirability_only:
                            # Only keep tweets with dynamic desirability labels
                            data = [d for d in data if self.is_desirable(d)]
                        storage_queue.append(data)
                        self.fingerprint_uses += 1
                    elif resp.status in (401, 403):
                        raise Exception("Account banned or unauthorized")
                    elif resp.status == 429:
                        await asyncio.sleep(random.randint(60, 120))
                await asyncio.sleep(random.uniform(15, 25))
            except Exception as e:
                print(f"Error for account {self.account['username']}: {e}")
                break

    def is_desirable(self, data):
        # Implement your desirability label check
        return True
