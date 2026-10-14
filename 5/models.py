class BankAccount:
    def __init__(self, number: str, owner: str, balance: float, account_type: str):
        self._number = number
        self._owner = owner
        self._balance = balance
        self._account_type = account_type

    @property
    def number(self) -> str:
        return self._number

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float):
        self._balance = value

    @property
    def account_type(self) -> str:
        return self._account_type

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("! Сумма пополнения должна быть > 0")
        self._balance += amount

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("! Сумма списания должна быть > 0")
        if amount > self._balance:
            raise ValueError("! Недостаточно средств")
        self._balance -= amount

    def get_info(self) -> str:
        return (f"[{self._number}] {self._owner} | "
                f"тип: {self._account_type} | "
                f"баланс: {self._balance:.2f} руб.")

    def __repr__(self) -> str:
        return self.get_info()


class DebitAccount(BankAccount):
    def __init__(self, number: str, owner: str, balance: float, cashback: float = 0.0):
        super().__init__(number, owner, balance, "Дебетовый")
        self._cashback = cashback

    @property
    def cashback(self) -> float:
        return self._cashback

    def get_info(self) -> str:
        base = super().get_info()
        return f"{base} | кэшбэк: {self._cashback}%"

    def calculate_cashback(self, spent: float) -> float:
        return spent * self._cashback / 100


class SavingsAccount(BankAccount):
    def __init__(self, number: str, owner: str, balance: float, interest_rate: float = 0.0):
        super().__init__(number, owner, balance, "Сберегательный")
        self._interest_rate = interest_rate

    @property
    def interest_rate(self) -> float:
        return self._interest_rate

    def get_info(self) -> str:
        base = super().get_info()
        return f"{base} | ставка: {self._interest_rate}%"

    def calculate_interest(self, months: int = 12) -> float:
        return self._balance * self._interest_rate / 100 * months / 12
