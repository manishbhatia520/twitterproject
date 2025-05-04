import asyncio
from scraping.account_pool import AccountPool
from scraping.proxy_manager import ProxyManager
from scraping.worker import ScraperWorker

class ScraperManager:
    def __init__(self, accounts, backup_accounts, proxies, storage_queue):
        self.account_pool = AccountPool(accounts, backup_accounts)
        self.proxy_manager = ProxyManager(proxies)
        self.storage_queue = storage_queue

    async def run(self, num_workers=100):
        tasks = []
        for i in range(num_workers):
            account = self.account_pool.get_account()
            proxy = self.proxy_manager.get_proxy(i)
            desirability_only = (i < 2)  # First 2 workers for desirability labels
            worker = ScraperWorker(account, proxy, desirability_only)
            session = aiohttp.ClientSession()
            tasks.append(worker.scrape(session, self.storage_queue))
        await asyncio.gather(*tasks)
