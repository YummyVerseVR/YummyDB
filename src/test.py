import requests


def test():
    data = {"uuid": "024381f3-9b86-41df-abbf-c264d0241c8d", "is_ready": True}
    res = requests.post("http://192.168.11.101:8000/set-user-status", json=data)
    print(res.json())


if __name__ == "__main__":
    test()
