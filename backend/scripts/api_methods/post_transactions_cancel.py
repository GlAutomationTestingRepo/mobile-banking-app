from common import ask_int, request_json


def main() -> None:
    transaction_id = ask_int("Transaction ID to cancel: ")
    status, body = request_json("POST", f"/transactions/{transaction_id}/cancel")
    print(f"POST /transactions/{transaction_id}/cancel -> {status}")
    print(body)


if __name__ == "__main__":
    main()

