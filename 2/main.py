# Лабораторная 2 | Вариант 13 | Музыкальные композиции

def input_int(message, predicate):
    while True:
        try:
            r = int(input(message + ": "))
        except ValueError:
            print("! Введите целое число")
            continue
        if not predicate(r):
            print("! Неправильное число")
            continue
        return r


def durations_analysis(playlist):
    if not playlist:
        print("! Плейлист пуст. Нечего анализировать.")
        return

    durations = [song['duration'] for song in playlist]
    print(f"Самая длинная композиция: {max(durations)} секунд")
    print(f"Самая короткая композиция: {min(durations)} секунд")
    print(f"Средняя продолжительность: {sum(durations) / len(durations):.2f} секунд")
    print("\nКомпозиции по убыванию длительности:")
    for song in sorted(playlist, key=lambda x: -x['duration']):
        print(f"  {song['name']}: {song['duration']} секунд")


def add_song(playlist):
    name = input("Введите имя композиции: ")
    author = input("Введите исполнителя композиции: ")
    genre = input("Введите жанр композиции: ")
    duration = input_int("Введите длительность композиции (в секундах, > 0)", lambda x: x > 0)

    playlist.append({
        "name": name,
        "author": author,
        "genre": genre,
        "duration": duration,
    })
    print(f'Композиция "{name}" добавлена.')


def remove_song(playlist):
    name = input("Введите имя композиции для удаления: ")
    sentinel = object()
    song = next(filter(lambda x: name in x["name"], playlist), sentinel)

    if song is not sentinel:
        playlist.remove(song)
        print(f'Композиция "{song['name']}" удалена')
    else:
        print("! Композиция не найдена")


def main():
    playlist = [
        {"name": "Between Two Worlds", "author": "Mili", "genre": "soundtrack", "duration": 4*60 + 57},
        {"name": "Unanswered", "author": "Suicide Silence", "genre": "deathcore", "duration": 2*60 + 16},
        {"name": "Nocturne No. 20", "author": "Chopin", "genre": "classics", "duration": 4*60 + 31},
        {"name": "Moonlight Sonata (1st Movement)", "author": "Beethoven", "genre": "classics", "duration": 7*60 + 25},
        {"name": "Hero", "author": "Mili", "genre": "soundtrack", "duration": 3*60 + 35},
    ]

    while True:
        print("1. Все композиции")
        print("2. Поиск композиций исполнителя")
        print("3. Фильтрация по жанру")
        print("4. Анализ продолжительностей")
        print("5. Список уникальных исполнителей")
        print("6. Добавить композицию")
        print("7. Удалить композицию")
        print("0. Выйти")

        p = input_int("Введите опцию", lambda p: 0 <= p <= 7)

        if p == 1:
            for song in playlist:
                print(f"  {song['name']} — {song['author']} ({song['genre']}, {song['duration']} сек.)")
        elif p == 2:
            author = input("Введите исполнителя: ")
            found = False
            for song in filter(lambda x: author.lower() in x['author'].lower(), playlist):
                print(f"  {song['name']} — {song['author']}")
                found = True
            if not found:
                print("! Композиции этого исполнителя не найдены.")
        elif p == 3:
            genre = input("Введите жанр: ")
            found = False
            for song in filter(lambda x: genre.lower() in x['genre'].lower(), playlist):
                print(f"  {song['name']} — {song['genre']}")
                found = True
            if not found:
                print("! Композиции этого жанра не найдены.")
        elif p == 4:
            durations_analysis(playlist)
        elif p == 5:
            authors = sorted(set(map(lambda x: x['author'], playlist)))
            for author in authors:
                print(f"  {author}")
        elif p == 6:
            add_song(playlist)
        elif p == 7:
            remove_song(playlist)
        elif p == 0:
            print("Выход из программы.")
            break

        input("\nНажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    main()
