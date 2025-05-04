import random
import threading

class AccountPool:
    def __init__(self, accounts, backup_accounts):
        self.lock = threading.Lock()
        self.accounts = accounts[:]  # Active accounts
        self.backup_accounts = backup_accounts[:]  # Backup pool
        self.banned_accounts = set()

    def get_account(self):
        with self.lock:
            available = [a for a in self.accounts if a['username'] not in self.banned_accounts]
            if not available:
                raise Exception("No active accounts available!")
            return random.choice(available)

    def ban_account(self, username):
        with self.lock:
            self.banned_accounts.add(username)
            # Replace with backup if available
            if self.backup_accounts:
                replacement = self.backup_accounts.pop(0)
                self.accounts = [replacement if a['username'] == username else a for a in self.accounts]
