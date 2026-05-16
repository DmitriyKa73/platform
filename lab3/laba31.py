"""Дневник заметок — создание, просмотр и поиск заметок с сохранением в JSON."""

import json
from datetime import datetime
from pathlib import Path

NOTES_FILE = Path(__file__).resolve().parent / "notes.json"
DATE_FORMAT = "%d.%m.%Y"
DATETIME_FORMAT = "%d.%m.%Y %H:%M"
SEPARATOR = "─" * 50


def load_notes() -> list[dict]:
    """Загрузить заметки из JSON-файла."""
    if not NOTES_FILE.exists():
        return []
    with NOTES_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_notes(notes: list[dict]) -> None:
    """Сохранить заметки в JSON-файл."""
    with NOTES_FILE.open("w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def create_note() -> None:
    """Создать новую заметку с автоматической датой и временем."""
    title = input("Введите заголовок заметки: ").strip()
    if not title:
        print("Заголовок не может быть пустым.")
        return

    print("Введите текст заметки (пустая строка — завершить ввод):")
    lines: list[str] = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    text = "\n".join(lines)

    now = datetime.now()
    note = {
        "title": title,
        "text": text,
        "datetime": now.strftime(DATETIME_FORMAT),
        "date": now.strftime(DATE_FORMAT),
    }

    notes = load_notes()
    notes.append(note)
    save_notes(notes)
    print(f"\nЗаметка сохранена ({note['datetime']}).")


def format_note(note: dict, index: int | None = None) -> str:
    """Форматировать одну заметку для вывода."""
    prefix = f"#{index} " if index is not None else ""
    lines = [
        f"{prefix}{SEPARATOR}",
        f"  Заголовок: {note['title']}",
        f"  Дата:      {note['datetime']}",
        f"  Текст:",
    ]
    for line in note.get("text", "").split("\n"):
        lines.append(f"    {line}" if line else "    (пусто)")
    lines.append(SEPARATOR)
    return "\n".join(lines)


def show_all_notes() -> None:
    """Показать все заметки."""
    notes = load_notes()
    count = len(notes)

    if count == 0:
        print("\nЗаметок пока нет.")
        return

    print(f"\n{'=' * 50}")
    print(f"  ВСЕ ЗАМЕТКИ (всего: {count})")
    print(f"{'=' * 50}\n")

    for i, note in enumerate(notes, start=1):
        print(format_note(note, index=i))
        print()


def find_by_date() -> None:
    """Найти заметки по дате (ДД.ММ.ГГГГ)."""
    date_str = input("Введите дату (ДД.ММ.ГГГГ): ").strip()
    try:
        datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        print("Неверный формат даты. Используйте ДД.ММ.ГГГГ, например: 16.05.2026")
        return

    notes = load_notes()
    found = [n for n in notes if n.get("date") == date_str or n.get("datetime", "").startswith(date_str)]

    if not found:
        print(f"\nЗаметок за {date_str} не найдено.")
        return

    print(f"\n{'=' * 50}")
    print(f"  ЗАМЕТКИ ЗА {date_str} (найдено: {len(found)})")
    print(f"{'=' * 50}\n")

    for i, note in enumerate(found, start=1):
        print(format_note(note, index=i))
        print()


def print_menu() -> None:
    print("\n" + "=" * 50)
    print("  ДНЕВНИК ЗАМЕТОК")
    print("=" * 50)
    print("  1 – Создать новую заметку")
    print("  2 – Показать все заметки")
    print("  3 – Найти заметку по дате")
    print("  4 – Выход")
    print("=" * 50)


def main() -> None:
    """Главный цикл программы."""
    while True:
        print_menu()
        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            create_note()
        elif choice == "2":
            show_all_notes()
        elif choice == "3":
            find_by_date()
        elif choice == "4":
            print("\nДо свидания!")
            break
        else:
            print("Неверный выбор. Введите число от 1 до 4.")


if __name__ == "__main__":
    main()
