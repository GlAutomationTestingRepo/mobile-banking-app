from common import ask_int, request_json


def main() -> None:
    card_id = ask_int("What Card ID do you want to see? ")
    status, body = request_json("GET", f"/cards/{card_id}")
    print(f"GET /cards/{card_id} -> {status}")
    print(body)


if __name__ == "__main__":
    main()

