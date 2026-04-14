from common import ask_int, request_json


def main() -> None:
    print("Leave one input empty if you don't want to filter by it.")
    account_id = ask_int("Account ID to filter (Enter to skip): ", allow_empty=True)
    customer_id = ask_int("Recipient Customer ID to filter (Enter to skip): ", allow_empty=True)

    params = {}
    if account_id is not None:
        params["account_id"] = account_id
    if customer_id is not None:
        params["customer_id"] = customer_id

    status, body = request_json("GET", "/transactions/history", params=params)
    print("GET /transactions/history ->", status)
    print(body)


if __name__ == "__main__":
    main()

