# Лабораторная 3 | Вариант 16 | Электронная библиотека

from abc import ABC, abstractmethod

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


class Document(ABC):
    def __init__(self, doc_id: int, title: str, author: str, year: int):
        self._id = doc_id
        self._title = title
        self._author = author
        self._year = year

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("! Название не может быть пустым")
        self._title = value

    @property
    def author(self) -> str:
        return self._author

    @property
    def year(self) -> int:
        return self._year

    @abstractmethod
    def get_info(self) -> str:
        pass

    @abstractmethod
    def get_volume(self) -> int:
        pass


class TextDocument(Document):
    def __init__(self, doc_id: int, title: str, author: str, year: int, pages: int):
        super().__init__(doc_id, title, author, year)
        self._pages = pages

    @property
    def pages(self) -> int:
        return self._pages

    @pages.setter
    def pages(self, value: int):
        if value <= 0:
            raise ValueError("! Количество страниц должно быть > 0")
        self._pages = value

    def get_info(self) -> str:
        base_info = f"[{self._id}] {self._title} ({self._author}, {self._year})"
        return f"{base_info} [Текст, {self._pages} стр.]"

    def get_volume(self) -> int:
        return self._pages


class Presentation(Document):
    def __init__(self, doc_id: int, title: str, author: str, year: int, slides: int):
        super().__init__(doc_id, title, author, year)
        self._slides = slides

    @property
    def slides(self) -> int:
        return self._slides

    @slides.setter
    def slides(self, value: int):
        if value <= 0:
            raise ValueError("! Количество слайдов должно быть > 0")
        self._slides = value

    def get_info(self) -> str:
        base_info = f"[{self._id}] {self._title} ({self._author}, {self._year})"
        return f"{base_info} [Презентация, {self._slides} слайдов]"

    def get_volume(self) -> int:
        return self._slides


class DocumentRepository:
    def __init__(self):
        self._documents: list[Document] = []

    def add_document(self, doc: Document):
        self._documents.append(doc)

    def remove_document(self, doc_id: int) -> bool:
        for i in range(len(self._documents)):
            if self._documents[i].id == doc_id:
                del self._documents[i]
                return True
        return False

    def find_by_title(self, title: str) -> list[Document]:
        return [doc for doc in self._documents if title.lower() in doc.title.lower()]

    def get_all_info(self):
        if not self._documents:
            print("! Репозиторий пуст.")
            return
        for doc in self._documents:
            print(doc.get_info())

    def get_total_volume(self) -> int:
        return sum(doc.get_volume() for doc in self._documents)


def add_document(repo: DocumentRepository):
    print("Какой документ добавить?")
    print("1. Текстовый документ")
    print("2. Презентация")
    type_choice = input_int("Тип", lambda x: 1 <= x <= 2)

    doc_id = input_int("ID", lambda x: x > 0)
    title = input("Название: ").strip()
    author = input("Автор: ").strip()
    year = input_int("Год", lambda x: 1000 < x < 2100)

    if type_choice == 1:
        pages = input_int("Количество страниц", lambda x: x > 0)
        doc = TextDocument(doc_id, title, author, year, pages)
    else:
        slides = input_int("Количество слайдов", lambda x: x > 0)
        doc = Presentation(doc_id, title, author, year, slides)

    repo.add_document(doc)
    print("Документ добавлен.")


def main():
    repo = DocumentRepository()

    repo.add_document(TextDocument(1, "Война и мир", "Л. Толстой", 1869, 1300))
    repo.add_document(TextDocument(2, "Преступление и наказание", "Ф. Достоевский", 1866, 671))
    repo.add_document(Presentation(3, "Введение в Python", "И. Иванов", 2024, 45))
    repo.add_document(TextDocument(4, "Повелитель тайн", "Е Юань", 2018, 1340))

    while True:
        print("1. Показать все документы")
        print("2. Добавить документ")
        print("3. Удалить документ")
        print("4. Поиск по названию")
        print("5. Показать общий объем")
        print("0. Выход")

        choice = input_int("Выберите действие", lambda x: 0 <= x <= 5)

        if choice == 1:
            repo.get_all_info()
        elif choice == 2:
            add_document(repo)
        elif choice == 3:
            doc_id = input_int("Введите ID для удаления", lambda x: x > 0)
            if repo.remove_document(doc_id):
                print("Документ удален.")
            else:
                print("! Документ с таким ID не найден.")
        elif choice == 4:
            query = input("Введите название: ").strip()
            results = repo.find_by_title(query)
            if results:
                for doc in results:
                    print(doc.get_info())
            else:
                print("! Ничего не найдено.")
        elif choice == 5:
            total = repo.get_total_volume()
            print(f"Общий объем: {total} единиц")
        elif choice == 0:
            print("Выход из программы.")
            break

        input("\nНажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    main()
