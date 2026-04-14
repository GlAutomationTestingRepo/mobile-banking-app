from common import ask_int, request_json


def main() -> None:
    from_account_id = ask_int("From Account ID: ")
    to_account_id = ask_int("To Account ID: ")
    amount = input("Transfer amount (example 50.00): ").strip() or "50.00"
    details = input("Transfer details: ").strip() or "Manual transfer from terminal"

    payload = {
        "from_account_id": from_account_id,
        "to_account_id": to_account_id,
        "amount": amount,
        "details": details,
    }
    status, body = request_json("POST", "/transactions/transfer", payload)
    print(f"POST /transactions/transfer -> {status}")
    print(body)


if __name__ == "__main__":
    main()

