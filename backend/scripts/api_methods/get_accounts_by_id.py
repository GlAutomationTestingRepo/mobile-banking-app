from common import ask_int, request_json


def main() -> None:
    account_id = ask_int("What Account ID do you want to see? ")
    status, body = request_json("GET", f"/accounts/{account_id}")
    print(f"GET /accounts/{account_id} -> {status}")
    print(body)


if __name__ == "__main__":
    main()

