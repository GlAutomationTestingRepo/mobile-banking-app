from common import ask_int, request_json, unique_suffix


def main() -> None:
    account_id = ask_int("Account ID for new card: ")
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
    print(f"POST /cards -> {status}")
    print(body)


if __name__ == "__main__":
    main()

