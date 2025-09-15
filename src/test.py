import requests
import uuid


def test():
    data = {"uuid": str(uuid.uuid4()), "is_ready": True}
    res = requests.post("http://localhost:8000/set-user-status", json=data)
    print(res.json())


if __name__ == "__main__":
    test()
