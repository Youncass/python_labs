def filter_objects(objects: list, predicate) -> list:
    return list(filter(predicate, objects))


def transform_objects(objects: list, operation) -> list:
    return list(map(operation, objects))


def sort_objects(objects: list, key_function, reverse: bool = False) -> list:
    return sorted(objects, key=key_function, reverse=reverse)


def create_balance_checker(min_balance: float):
    def checker(account) -> bool:
        return account.balance >= min_balance
    return checker


def get_positive_balance_accounts(accounts: list) -> list:
    return filter_objects(accounts, lambda acc: acc.balance > 0)


def get_balances(accounts: list) -> list:
    return transform_objects(accounts, lambda acc: acc.balance)


def sort_by_balance(accounts: list, reverse: bool = True) -> list:
    return sort_objects(accounts, key_function=lambda acc: acc.balance, reverse=reverse)


def has_negative_balance(accounts: list) -> bool:
    return any(acc.balance < 0 for acc in accounts)


def all_have_positive_balance(accounts: list) -> bool:
    return all(acc.balance > 0 for acc in accounts)


def total_balance(accounts: list) -> float:
    return sum(acc.balance for acc in accounts)


def accounts_as_dict(accounts: list) -> dict:
    return {acc.number: acc.balance for acc in accounts}


def unique_owners(accounts: list) -> set:
    return {acc.owner for acc in accounts}


def get_owners_list(accounts: list) -> list:
    return transform_objects(accounts, lambda acc: acc.owner)
