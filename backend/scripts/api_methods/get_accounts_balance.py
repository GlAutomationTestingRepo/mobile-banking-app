from common import ask_int, request_json


def main() -> None:
    account_id = ask_int("What Account ID balance do you want to see? ")
    status, body = request_json("GET", f"/accounts/{account_id}/balance")
    print(f"GET /accounts/{account_id}/balance -> {status}")
    print(body)


if __name__ == "__main__":
    main()

