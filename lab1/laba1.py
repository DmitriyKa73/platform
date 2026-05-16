from datetime import datetime

FRAME_WIDTH = 40
FRAME_CHAR = "*"


def print_frame_line(text: str = "") -> None:
    """Печатает строку внутри рамки с выравниванием."""
    inner_width = FRAME_WIDTH - 4  # пробелы по краям и символы * *
    if len(text) > inner_width:
        text = text[:inner_width]
    print(f"{FRAME_CHAR} {text:<{inner_width}} {FRAME_CHAR}")


def print_horizontal_border() -> None:
    """Печатает горизонтальную границу рамки."""
    print(FRAME_CHAR * FRAME_WIDTH)


def print_centered_title(title: str) -> None:
    """Печатает заголовок по центру внутри рамки."""
    inner_width = FRAME_WIDTH - 4
    print_frame_line(title.center(inner_width))


def read_int(prompt: str) -> int:
    """Запрашивает целое число с проверкой ввода."""
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Ошибка! Введите целое число.")


def read_float(prompt: str) -> float:
    """Запрашивает число с плавающей точкой с проверкой ввода."""
    while True:
        value = input(prompt).strip().replace(",", ".")
        try:
            return float(value)
        except ValueError:
            print("Ошибка! Введите число (например: 185.5).")


def age_word(age: int) -> str:
    """Возвращает правильное склонение слова «год»."""
    n = abs(age) % 100
    n1 = n % 10
    if 11 <= n <= 19:
        return "лет"
    if n1 == 1:
        return "год"
    if 2 <= n1 <= 4:
        return "года"
    return "лет"


def main() -> None:
    current_year = datetime.now().year

    print_horizontal_border()
    print_centered_title("Личная визитка")
    print_horizontal_border()

    name = input("Введите ваше имя: ").strip()
    surname = input("Введите вашу фамилию: ").strip()
    birth_year = read_int("Введите год рождения: ")
    height = read_float("Введите ваш рост (см): ")

    age = current_year - birth_year

    print_horizontal_border()
    print_centered_title("ВАША ВИЗИТКА")
    print_horizontal_border()
    print_frame_line(f"Имя: {name}")
    print_frame_line(f"Фамилия: {surname}")
    print_frame_line(f"Год рождения: {birth_year}")
    print_frame_line(f"Возраст: {age} {age_word(age)}")
    print_frame_line(f"Рост: {height} см")
    print_horizontal_border()


if __name__ == "__main__":
    main()
