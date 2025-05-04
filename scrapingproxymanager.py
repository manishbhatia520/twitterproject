import random

class ProxyManager:
    def __init__(self, proxies):
        self.proxies = proxies

    def get_proxy(self, account_idx):
        # 10:1 ratio
        proxy_idx = account_idx // 10
        return self.proxies[proxy_idx % len(self.proxies)]
