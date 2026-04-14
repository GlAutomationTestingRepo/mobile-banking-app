from decimal import Decimal

from common import ask_int, request_json


def _ask_currency(i: int) -> str:
    raw = input(f"Currency for balance #{i} (e.g. USD/EUR/GBP): ").strip()
    return raw or "USD"


def _ask_decimal(prompt: str, default: str) -> Decimal:
    raw = input(f"{prompt} (default {default}): ").strip()
    return Decimal(raw or default)


def main() -> None:
    account_id = ask_int("Account ID: ")
    count = ask_int("How many balances to create (2 or 3): ")
    if count not in (2, 3):
        print("Only 2 or 3 are supported.")
        return

    for i in range(1, count + 1):
        payload = {
            "balance": str(_ask_decimal(f"Initial amount for balance #{i}", "0.00")),
            "currency": _ask_currency(i),
            "is_limited": False,
        }
        status, body = request_json("POST", f"/accounts/{account_id}/balances", payload)
        print(f"POST /accounts/{account_id}/balances -> {status}")
        print(body)


if __name__ == "__main__":
    main()

