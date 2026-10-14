# Лабораторная 5 | Вариант 7 | Банковские счета

from models import *
from operations import *
from generators import *


def input_int(message: str, predicate=lambda x: True) -> int:
    while True:
        try:
            value = int(input(message + ": "))
        except ValueError:
            print("! Введите целое число")
            continue
        if not predicate(value):
            print("! Неверное значение")
            continue
        return value


def input_float(message: str, predicate=lambda x: True) -> float:
    while True:
        try:
            value = float(input(message + ": "))
        except ValueError:
            print("! Введите число")
            continue
        if not predicate(value):
            print("! Неверное значение")
            continue
        return value


def show_accounts(accounts: list[BankAccount]):
    if not accounts:
        print("! Нет счетов для отображения.")
        return
    for acc in accounts:
        print(acc.get_info())


def create_sample_accounts() -> list[BankAccount]:
    return [
        DebitAccount("DE001", "Иванов И.И.", 15000.0, cashback=1.5),
        SavingsAccount("SA001", "Петров П.П.", 250000.0, interest_rate=8.0),
        DebitAccount("DE002", "Сидоров С.С.", -500.0, cashback=1.0),  # Отрицательный счёт
        SavingsAccount("SA002", "Кузнецова А.А.", 50000.0, interest_rate=7.5),
        DebitAccount("DE003", "Иванов И.И.", 3000.0, cashback=2.0),
        SavingsAccount("SA003", "Смирнов В.В.", 1000000.0, interest_rate=6.0),
    ]


def main():
    accounts = create_sample_accounts()

    while True:
        print("1. Показать все счета")
        print("2. Фильтр: положительный баланс (filter)")
        print("3. Получить балансы (map)")
        print("4. Сортировка по балансу (sorted)")
        print("5. Общий баланс")
        print("6. Проверка: есть ли отрицательные счета? (any)")
        print("7. Проверка: все ли счета положительные? (all)")
        print("8. Уникальные владельцы (set comprehension)")
        print("9. Словарь {номер: баланс} (dict comprehension)")
        print("10. Генератор: счета по типу")
        print("11. Генератор: счета выше порога")
        print("12. Собственный итератор: только дебетовые")
        print("13. Функция, возвращающая функцию (баланс >= порога)")
        print("0. Выход")

        choice = input_int("Выберите действие", lambda x: 0 <= x <= 13)

        try:
            match choice:
                case 1:
                    show_accounts(accounts)

                case 2:
                    positive = get_positive_balance_accounts(accounts)
                    print(f"\nСчета с положительным балансом ({len(positive)}):")
                    show_accounts(positive)

                case 3:
                    balances = get_balances(accounts)
                    print(f"\nБалансы (map): {balances}")

                case 4:
                    reverse = input("По убыванию? (y/n): ").strip().lower() == "y"
                    sorted_accs = sort_by_balance(accounts, reverse=reverse)
                    print("\nСортировка по балансу:")
                    show_accounts(sorted_accs)

                case 5:
                    total = total_balance(accounts)
                    print(f"\nОбщий баланс: {total:.2f} руб.")

                case 6:
                    if has_negative_balance(accounts):
                        print("\nДа, есть счета с отрицательным балансом.")
                    else:
                        print("\nНет, все счета с положительным балансом.")

                case 7:
                    if all_have_positive_balance(accounts):
                        print("\nВсе счета имеют положительный баланс.")
                    else:
                        print("\nНе все счета положительные.")

                case 8:
                    owners = unique_owners(accounts)
                    print(f"\nУникальные владельцы (set): {owners}")

                case 9:
                    mapping = accounts_as_dict(accounts)
                    print("\nСловарь {номер: баланс}:")
                    for k, v in mapping.items():
                        print(f"  {k}: {v:.2f} руб.")

                case 10:
                    acc_type = input("Тип (Дебетовый/Сберегательный): ").strip()
                    print(f"\nСчета типа '{acc_type}':")
                    for acc in accounts_by_type(accounts, acc_type):
                        print(acc.get_info())

                case 11:
                    threshold = input_float("Порог баланса", lambda x: x >= 0)
                    print(f"\nСчета с балансом > {threshold}:")
                    for acc in accounts_above_threshold(accounts, threshold):
                        print(acc.get_info())

                case 12:
                    print("\nСобственный итератор (только Дебетовые):")
                    iterator = AccountIterator(accounts, "Дебетовый")
                    for acc in iterator:
                        print(acc.get_info())

                case 13:
                    min_bal = input_float("Минимальный баланс", lambda x: x >= 0)
                    checker = create_balance_checker(min_bal)
                    filtered = filter_objects(accounts, checker)
                    print(f"\nСчета с балансом >= {min_bal}:")
                    show_accounts(filtered)

                case 0:
                    print("Выход.")
                    break

        except ValueError as e:
            print(f"! Ошибка: {e}")

        input("\nНажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    main()
