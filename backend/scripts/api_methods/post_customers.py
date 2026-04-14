from common import request_json, unique_suffix


def main() -> None:
    token = unique_suffix()
    payload = {
        "name": f"User{token[-4:]}",
        "lastname": "Demo",
        "email": f"user_{token}@example.com",
        "phone": f"+1{token[-9:]}",
        "gender": "M",
        "birth_date": "1998-02-12T00:00:00",
        "status": "Active",
        "country": "USA",
        "nationality": "American",
        "login": f"login_{token}",
        "password": f"Pwd_{token}",
    }
    status, body = request_json("POST", "/customers", payload)
    print(f"POST /customers -> {status}")
    print(body)


if __name__ == "__main__":
    main()

