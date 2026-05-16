"""Журнал наблюдений — программа для ежедневных записей."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
JOURNAL_FILE = DATA_DIR / "journal.txt"

DATE_FORMAT = "%Y-%m-%d"
FIELD_SEPARATOR = " | "


@dataclass
class Entry:
    date: str
    rating: int
    text: str


def ensure_data_dir() -> None:
    """Создаёт папку data, если её ещё нет."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def read_date(prompt: str) -> str:
    """Запрашивает дату в формате ГГГГ-ММ-ДД с проверкой."""
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, DATE_FORMAT)
        except ValueError:
            print("Ошибка! Введите дату в формате ГГГГ-ММ-ДД (например: 2024-09-15).")
            continue
        return value


def read_rating(prompt: str) -> int:
    """Запрашивает оценку от 1 до 10."""
    while True:
        value = input(prompt).strip()
        try:
            rating = int(value)
        except ValueError:
            print("Ошибка! Введите целое число от 1 до 10.")
            continue
        if 1 <= rating <= 10:
            return rating
        print("Ошибка! Оценка должна быть в диапазоне от 1 до 10.")


def format_entry_line(entry: Entry) -> str:
    """Формирует строку записи для файла."""
    return f"{entry.date}{FIELD_SEPARATOR}{entry.rating}{FIELD_SEPARATOR}{entry.text}"


def parse_entry_line(line: str) -> Entry | None:
    """Разбирает строку файла в запись. Возвращает None при ошибке."""
    line = line.strip()
    if not line:
        return None
    parts = line.split(FIELD_SEPARATOR, maxsplit=2)
    if len(parts) != 3:
        return None
    date_str, rating_str, text = parts
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        rating = int(rating_str)
    except ValueError:
        return None
    if not 1 <= rating <= 10:
        return None
    return Entry(date=date_str, rating=rating, text=text)


def load_entries() -> list[Entry]:
    """Читает все записи из файла."""
    if not JOURNAL_FILE.exists():
        return []
    entries: list[Entry] = []
    with JOURNAL_FILE.open(encoding="utf-8") as file:
        for line in file:
            entry = parse_entry_line(line)
            if entry is not None:
                entries.append(entry)
    return entries


def save_entry(entry: Entry) -> None:
    """Добавляет запись в конец файла."""
    ensure_data_dir()
    with JOURNAL_FILE.open("a", encoding="utf-8") as file:
        file.write(format_entry_line(entry) + "\n")


def clear_journal() -> None:
    """Очищает журнал."""
    ensure_data_dir()
    JOURNAL_FILE.write_text("", encoding="utf-8")


def print_menu() -> None:
    """Выводит главное меню."""
    print("=" * 40)
    print("        ЖУРНАЛ НАБЛЮДЕНИЙ")
    print("=" * 40)
    print("Выберите действие:")
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Очистить журнал")
    print("4. Выход")


def add_entry() -> None:
    """Добавляет новую запись в журнал."""
    print("--- Добавление новой записи ---")
    date_str = read_date("Введите дату (ГГГГ-ММ-ДД): ")
    text = input("Введите текст наблюдения: ").strip()
    rating = read_rating("Введите оценку (1-10): ")
    save_entry(Entry(date=date_str, rating=rating, text=text))
    print("\nЗапись успешно добавлена!")


def _table_border(col_widths: list[int]) -> str:
    segments = ["-" * (width + 2) for width in col_widths]
    return "+" + "+".join(segments) + "+"


def _table_row(cells: list[str], col_widths: list[int], align: list[str]) -> str:
    parts: list[str] = []
    for cell, width, alignment in zip(cells, col_widths, align):
        if alignment == "center":
            parts.append(f" {cell:^{width}} ")
        elif alignment == "right":
            parts.append(f" {cell:>{width}} ")
        else:
            parts.append(f" {cell:<{width}} ")
    return "|" + "|".join(parts) + "|"


def print_entries_table(entries: list[Entry]) -> None:
    """Выводит записи в виде таблицы и статистику."""
    print("--- Все записи ---")
    if not entries:
        print("Журнал пуст. Записей пока нет.")
        print("\nСтатистика:")
        print("Всего записей: 0")
        print("Средняя оценка: —")
        return

    date_width = max(len("Дата"), max(len(e.date) for e in entries))
    rating_width = max(len("Оценка"), max(len(str(e.rating)) for e in entries))
    text_width = max(len("Текст"), max(len(e.text) for e in entries))

    col_widths = [date_width, rating_width, text_width]
    align = ["center", "center", "left"]

    border = _table_border(col_widths)
    print(border)
    print(_table_row(["Дата", "Оценка", "Текст"], col_widths, align))
    print(border)
    for entry in entries:
        print(
            _table_row(
                [entry.date, str(entry.rating), entry.text],
                col_widths,
                align,
            )
        )
    print(border)

    count = len(entries)
    average = sum(e.rating for e in entries) / count
    print("Статистика:")
    print(f"Всего записей: {count}")
    print(f"Средняя оценка: {average:.2f}")


def show_all_entries() -> None:
    """Показывает все записи."""
    entries = load_entries()
    print_entries_table(entries)


def main() -> None:
    ensure_data_dir()
    while True:
        print()
        print_menu()
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            add_entry()
        elif choice == "2":
            show_all_entries()
        elif choice == "3":
            clear_journal()
            print("\nЖурнал очищен.")
        elif choice == "4":
            print("\nДо свидания!")
            break
        else:
            print("\nНеверный выбор. Введите число от 1 до 4.")


if __name__ == "__main__":
    main()
