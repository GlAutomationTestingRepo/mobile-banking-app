from common import ask_int, request_json


def main() -> None:
    account_id = ask_int("Source Account ID for transaction: ")
    recipient_account_id = ask_int("Recipient Account ID (or same as source): ")
    recipient_customer_id = ask_int("Recipient Customer ID: ")

    payload = {
        "account_id": account_id,
        "amount": "150",
        "type_name": "Deposit",
        "status": "Created",
        "details": "Manual script transaction",
        "recipient_account_id": recipient_account_id,
        "recipient_customer_id": recipient_customer_id,
    }
    status, body = request_json("POST", "/transactions", payload)
    print(f"POST /transactions -> {status}")
    print(body)


if __name__ == "__main__":
    main()

