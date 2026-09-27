import json
import sys

WORDS_PATH = "words.json"

REQUIRED_STRING_FIELDS = [
    "id",
    "text",
    "reading",
    "category",
    "meaning",
    "misunderstanding",
    "note",
]

CATEGORIES = [
    "ことわざ",
    "慣用句",
    "四字熟語",
    "故事成語",
    "言葉",
    "副詞",
]

MAXIMUM_TEXT_LENGTH = 20


def load_document(path):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def validate_document(document):
    errors = []

    if not isinstance(document.get("version"), int):
        errors.append("version は整数にしてください")

    words = document.get("words")
    if not isinstance(words, list) or len(words) == 0:
        errors.append("words は 1 件以上の配列にしてください")
        return errors

    seen_ids = set()
    for index, word in enumerate(words):
        expected_no = index + 1
        label = f"words[{index}]"

        if word.get("no") != expected_no:
            errors.append(f"{label}: no は {expected_no} にしてください（実際: {word.get('no')}）")

        for field in REQUIRED_STRING_FIELDS:
            value = word.get(field)
            if not isinstance(value, str) or value.strip() == "":
                errors.append(f"{label}: {field} は空でない文字列にしてください")

        text = word.get("text")
        if isinstance(text, str) and len(text) > MAXIMUM_TEXT_LENGTH:
            errors.append(f"{label}: text は {MAXIMUM_TEXT_LENGTH} 文字以内にしてください（実際: {len(text)} 文字）")

        category = word.get("category")
        if category not in CATEGORIES:
            errors.append(f"{label}: category「{category}」は未定義です。定義済み: {' / '.join(CATEGORIES)}")

        word_id = word.get("id")
        if word_id in seen_ids:
            errors.append(f"{label}: id「{word_id}」が重複しています")
        seen_ids.add(word_id)

    return errors


def main():
    try:
        document = load_document(WORDS_PATH)
    except json.JSONDecodeError as error:
        print(f"{WORDS_PATH} は JSON として読めません: {error}")
        return 1

    errors = validate_document(document)
    if errors:
        for message in errors:
            print(message)
        print(f"{len(errors)} 件のエラーがあります")
        return 1

    print(f"{len(document['words'])} words OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
