from common import ask_int, request_json, unique_suffix


def main() -> None:
    account_id = ask_int("Account ID for cards: ")
    how_many = ask_int("How many cards to create (1 or 2): ")
    if how_many not in (1, 2):
        print("Only 1 or 2 are supported.")
        return

    for i in range(1, how_many + 1):
        token = unique_suffix()
        payload = {
            "account_id": account_id,
            "card_number": f"4{token.replace('_', '')[:15]}",
            "card_type": "Debit Card",
            "expiration_date": "2031-12-31T00:00:00",
            "status": "Active",
            "is_active": True,
        }
        status, body = request_json("POST", "/cards", payload)
        print(f"[{i}/{how_many}] POST /cards -> {status}")
        print(body)


if __name__ == "__main__":
    main()

