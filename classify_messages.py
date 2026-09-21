"""Классификация обращений по правилам, без внешних зависимостей."""

import argparse
from pathlib import Path


def classify_message(message: str) -> tuple[str, str]:
    """Вернуть категорию и один черновик ответа на русском языке."""
    text = message.casefold().replace("ё", "е")

    # Жалобы проверяются первыми: проблема может касаться и выдачи справки.
    if any(word in text for word in ("очередь", "холодная", "пропал", "не работает", "жалоб")):
        if "столов" in text:
            reply = (
                "Спасибо за сообщение. Уточните, пожалуйста, время посещения "
                "и расположение столовой, чтобы можно было разобраться "
                "с очередью и температурой еды."
            )
        elif any(word in text for word in ("wi-fi", "wifi", "вай-фай")):
            reply = (
                "Уточните, пожалуйста, этаж, аудиторию и время отключения Wi-Fi. "
                "Эти сведения помогут технической поддержке проверить проблему."
            )
        else:
            reply = "Пожалуйста, уточните, где и когда возникла проблема и что произошло."
        return "жалоба", reply

    if "справк" in text:
        return "справка", (
            "Чтобы узнать порядок получения справки о месте учёбы, "
            "обратитесь в учебную часть. Уточните способ подачи заявки "
            "и срок подготовки документа."
        )

    if "консультац" in text:
        return "другое", (
            "Уточните, пожалуйста, предмет, преподавателя и удобное время завтра. "
            "Возможность записи нужно согласовать с преподавателем."
        )

    if "парковк" in text:
        return "другое", (
            "Уточните, пожалуйста, какой корпус вы планируете посетить. "
            "Расположение гостевой парковки и правила въезда можно уточнить у охраны."
        )

    return "другое", "Пожалуйста, уточните ваш вопрос, чтобы мы могли помочь."


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path", nargs="?", type=Path,
        default=Path(__file__).with_name("messages.txt"),
        help="Текстовый файл UTF-8: одно обращение на строку",
    )
    args = parser.parse_args()
    try:
        messages = [
            line.strip()
            for line in args.path.read_text(encoding="utf-8-sig").splitlines()
            if line.strip()
        ]
    except (OSError, UnicodeError) as exc:
        parser.exit(1, f"Не удалось прочитать обращения: {exc}\n")

    for number, message in enumerate(messages, start=1):
        category, reply = classify_message(message)
        print(f"{number}. {message}")
        print(f"Категория: {category}")
        print(f"Черновик ответа: {reply}\n")


if __name__ == "__main__":
    main()
