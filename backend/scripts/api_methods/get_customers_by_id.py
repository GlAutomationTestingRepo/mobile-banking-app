from common import ask_int, request_json


def main() -> None:
    customer_id = ask_int("What Customer ID do you want to see? ")
    status, body = request_json("GET", f"/customers/{customer_id}")
    print(f"GET /customers/{customer_id} -> {status}")
    print(body)


if __name__ == "__main__":
    main()

