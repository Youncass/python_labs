from models import BankAccount


def accounts_by_type(accounts: list, account_type: str):
    for acc in accounts:
        if acc.account_type.lower() == account_type.lower():
            yield acc


def positive_balance_accounts(accounts: list):
    for acc in accounts:
        if acc.balance > 0:
            yield acc


def accounts_above_threshold(accounts: list, threshold: float):
    for acc in accounts:
        if acc.balance > threshold:
            yield acc


class AccountIterator:
    def __init__(self, accounts: list, account_type: str = None):
        self._accounts = accounts
        self._account_type = account_type
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> BankAccount:
        while self._index < len(self._accounts):
            account = self._accounts[self._index]
            self._index += 1
            if self._account_type is None or account.account_type.lower() == self._account_type.lower():
                return account
        raise StopIteration
