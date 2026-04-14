from common import ask_int, request_json


def main() -> None:
    payment_transaction_id = ask_int("Payment transaction ID to cancel: ")
    status, body = request_json("POST", f"/transactions/{payment_transaction_id}/cancel")
    print(f"POST /transactions/{payment_transaction_id}/cancel -> {status}")
    print(body)


if __name__ == "__main__":
    main()

