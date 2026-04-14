from common import ask_int, request_json, unique_suffix


def main() -> None:
    customer_id = ask_int("Customer ID for new account: ")
    token = unique_suffix()
    payload = {
        "customer_id": customer_id,
        "account_name": f"Main {token[-6:]}",
        "account_type": "Savings",
        "initial_balance": "1000.50",
        "currency": "USD",
        "limit_type": "daily",
        "limit_max_amount": "5000.00",
    }
    status, body = request_json("POST", "/accounts", payload)
    print(f"POST /accounts -> {status}")
    print(body)


if __name__ == "__main__":
    main()

