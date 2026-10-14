# Лабораторная 1 | Вариант 10 | Доходы предприятия

def input_monthly_income(month: int) -> float:
    while True:
        try:
            income = float(input(f"Введите доход за месяц {month}: "))
            if income < 0:
                print("! Ошибка: доход не может быть отрицательным")
                continue
        except ValueError:
            print("! Ошибка: необходимо ввести число")
            continue
        return income

def calculate_income_above_average(incomes: list[float], average: float) -> int:
    count = 0
    for income in incomes:
        if income > average:
            count += 1
    return count

def main():
    incomes = []
    for i in range(12):
        incomes.append(input_monthly_income(i + 1))

    total_income = sum(incomes)
    average_income = total_income / 12
    max_income = max(incomes)
    min_income = min(incomes)
    months_above_avg = calculate_income_above_average(incomes, average_income)

    print(f"Годовой доход: {total_income:.2f}")
    print(f"Среднемесячный доход: {average_income:.2f}")
    print(f"Наиболее прибыльный месяц: {max_income:.2f}")
    print(f"Наименее прибыльный месяц: {min_income:.2f}")
    print(f"Количество месяцев с доходом выше среднего: {months_above_avg}")

if __name__ == "__main__":
    main()
