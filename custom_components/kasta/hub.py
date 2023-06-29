import requests


class BasicHub:
    def __init__(self, host: str) -> None:
        self.host = host

    def verify_connection(self):
        try:
            r = requests.get(f"http://{self.host}/verify", timeout=10000)
            return r.status_code == 200
        except:
            return False

    def get_devices(self):
        r = requests.get(f"http://{self.host}/ha_status", timeout=10000)
        return r.json()

    def toggle(self, name):
        r = requests.get(f"http://{self.host}/toggle?name=" + name, timeout=10000)
        return r.json()
