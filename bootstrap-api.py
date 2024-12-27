lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI, llllllllllllIIl = Exception, print, input, range, KeyboardInterrupt, bool, __name__

from requests.packages.urllib3 import disable_warnings as IIIllllIlllIII
from random import choice as IlIlllIllIllIl, uniform as IIIIIIIlllllII
from requests import post as IllIIIIIIIIlll, get as IllllIIlllIIIl, head as lIlIllIIllIIII
from time import sleep as lIlIllllllIIIl, time as IllIllIIIIIIIl
from concurrent.futures import ThreadPoolExecutor as lllllIIlIIlIlI
from requests.exceptions import RequestException as IIIlllIlllllll
from urllib3.exceptions import InsecureRequestWarning as IlllIIIIIIlIII
IIIllllIlllIII(IlllIIIIIIlIII)

class llIIllIIIIlIIllllI:

    def __init__(lIIlllIIlIIIllIIII):
        lIIlllIIlIIIllIIII.IllIllllIlIlIlllII = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36']
        lIIlllIIlIIIllIIII.IllllllIIIIIlIllII = {'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'en-US,en;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest'}
        lIIlllIIlIIIllIIII.IIIIIIlIlIlllllIll = ['admin', 'dashboard', 'login', 'admin/dashboard', 'admin/login', 'api/v1/auth', 'api/v1/users', 'api/v1/settings', 'components', 'assets/js/bootstrap.min.js', 'assets/css/bootstrap.min.css', 'admin/components', 'admin/settings', 'admin/users', 'admin/profile', 'api/auth/login', 'api/auth/register']
        lIIlllIIlIIIllIIII.IIlIIllIlIIlIllIII = {'auth_test': {'username': 'admin', 'password': 'admin123', 'remember': llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)}, 'component_test': {'type': 'modal', 'title': 'Test Modal', 'content': 'Test Content', 'size': 'lg'}}

    def lIllIIlIllIlIIIIlI(lIIlllIIlIIIllIIII):
        return IlIlllIllIllIl(lIIlllIIlIIIllIIII.IllIllllIlIlIlllII)

    def IIlIllIIIIlllIllIl(lIIlllIIlIIIllIIII, IllIlllIlllIIIlIll, IlIIIllIIlIlIIIlll):
        """Verify endpoint availability before testing"""
        lllIllIllllIIlIIII = f"{IllIlllIlllIIIlIll.rstrip('/')}/{IlIIIllIIlIlIIIlll.lstrip('/')}"
        try:
            llIlIIIIlllllIlIlI = lIlIllIIllIIII(lllIllIllllIIlIIII, headers={'User-Agent': lIIlllIIlIIIllIIII.lIllIIlIllIlIIIIlI()}, timeout=3, verify=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), allow_redirects=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            return 200 <= llIlIIIIlllllIlIlI.status_code < 404
        except:
            return llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

    def IIllIlIllIIllIIlll(lIIlllIIlIIIllIIII, IllIlllIlllIIIlIll):
        """Discover valid Bootstrap-related endpoints"""
        llllllllllllllI('[INFO] Discovering valid Bootstrap endpoints...')
        lIlIlIIIIIllIlIlII = []
        llIIlIlIlIIIIlIlII = ['css/bootstrap.min.css', 'js/bootstrap.min.js', 'js/bootstrap.bundle.min.js', 'admin/templates', 'admin/themes', 'admin/plugins', 'api/components', 'api/themes', 'api/templates', 'bootstrap', 'bootstrap/js', 'bootstrap/css', 'dist/js/bootstrap.min.js', 'dist/css/bootstrap.min.css']
        lIIlllIIlIIIllIIII.IIIIIIlIlIlllllIll.extend(llIIlIlIlIIIIlIlII)
        for IlIIIllIIlIlIIIlll in lIIlllIIlIIIllIIII.IIIIIIlIlIlllllIll:
            if lIIlllIIlIIIllIIII.IIlIllIIIIlllIllIl(IllIlllIlllIIIlIll, IlIIIllIIlIlIIIlll):
                llllllllllllllI(f'[SUCCESS] Found valid endpoint: {IlIIIllIIlIlIIIlll}')
                lIlIlIIIIIllIlIlII.append(IlIIIllIIlIlIIIlll)
        if not lIlIlIIIIIllIlIlII:
            llllllllllllllI('[WARNING] No valid endpoints found. Using default endpoints.')
            return lIIlllIIlIIIllIIII.IIIIIIlIlIlllllIll
        return lIlIlIIIIIllIlIlII

    def lIIlIIIIIllIlIIlII(lIIlllIIlIIIllIIII, lIlIllIllllIIlIlll, IllIlllIlllIIIlIll, IlIIIllIIlIlIIIlll, IlIIlllIllIlIIIIlI=None):
        lllIllIllllIIlIIII = f"{IllIlllIlllIIIlIll.rstrip('/')}/{IlIIIllIIlIlIIIlll.lstrip('/')}"
        lIIlllIIlIIIllIIII.IllllllIIIIIlIllII['User-Agent'] = lIIlllIIlIIIllIIII.lIllIIlIllIlIIIIlI()
        llIlIIIllIlIlIlIll = {'Cache-Control': 'no-cache', 'Pragma': 'no-cache', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty'}
        lIIlllIIlIIIllIIII.IllllllIIIIIlIllII.update(llIlIIIllIlIlIlIll)
        try:
            if lIlIllIllllIIlIlll.upper() == 'GET':
                llIlIIIIlllllIlIlI = IllllIIlllIIIl(lllIllIllllIIlIIII, headers=lIIlllIIlIIIllIIII.IllllllIIIIIlIllII, timeout=5, verify=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), allow_redirects=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            else:
                if IlIIlllIllIlIIIIlI:
                    IlIIlllIllIlIIIIlI['csrf_token'] = lIIlllIIlIIIllIIII.lIllIlllIlIlIIIIII(IllIlllIlllIIIlIll)
                llIlIIIIlllllIlIlI = IllIIIIIIIIlll(lllIllIllllIIlIIII, json=IlIIlllIllIlIIIIlI, headers=lIIlllIIlIIIllIIII.IllllllIIIIIlIllII, timeout=5, verify=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), allow_redirects=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            if llIlIIIIlllllIlIlI.status_code in [404, 403]:
                return None
            llllllllllllllI(f'[{llIlIIIIlllllIlIlI.status_code}] {lIlIllIllllIIlIlll} {lllIllIllllIIlIIII}')
            return llIlIIIIlllllIlIlI.text if llIlIIIIlllllIlIlI.ok else None
        except IIIlllIlllllll as IlIIlIIIlIIIllIlll:
            llllllllllllllI(f'[ERROR] {lIlIllIllllIIlIlll} {lllIllIllllIIlIIII}: {IlIIlIIIlIIIllIlll}')
            return None

    def lIllIlllIlIlIIIIII(lIIlllIIlIIIllIIII, IllIlllIlllIIIlIll):
        """Get CSRF token from the Bootstrap application"""
        try:
            llIlIIIIlllllIlIlI = IllllIIlllIIIl(f"{IllIlllIlllIIIlIll.rstrip('/')}/login", headers={'User-Agent': lIIlllIIlIIIllIIII.lIllIIlIllIlIIIIlI()}, verify=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0))
            return 'dummy_token'
        except:
            return None

    def IIIlIIIlIlllIIllll(lIIlllIIlIIIllIIII, IllIlllIlllIIIlIll, IllIllIIlIIlIIllll=10, lIIIlIlIIlIIlIIlll=60):
        llllllllllllllI(f'[INFO] Starting stress test on {IllIlllIlllIIIlIll} for {lIIIlIlIIlIIlIIlll}s with {IllIllIIlIIlIIllll} threads')
        lIlIlIIIIIllIlIlII = lIIlllIIlIIIllIIII.IIllIlIllIIllIIlll(IllIlllIlllIIIlIll)
        if not lIlIlIIIIIllIlIlII:
            llllllllllllllI('[ERROR] No valid endpoints found. Aborting test.')
            return
        lIIlllIIlIIIllIIII.IIIIIIlIlIlllllIll = lIlIlIIIIIllIlIlII
        llIIlIlIlIlIlIIIIl = IllIllIIIIIIIl()

        def IIIIIllllIllIIIlll():
            while IllIllIIIIIIIl() - llIIlIlIlIlIlIIIIl < lIIIlIlIIlIIlIIlll:
                IlIIIllIIlIlIIIlll = IlIlllIllIllIl(lIIlllIIlIIIllIIII.IIIIIIlIlIlllllIll)
                lIlIllIllllIIlIlll = IlIlllIllIllIl(['GET', 'POST'])
                lIIIlIIIIIIIIIlllI = lIIlllIIlIIIllIIII.IIlIIllIlIIlIllIII.get('component_test') if lIlIllIllllIIlIlll == 'POST' else None
                llIIIllIlIlllllIlI = lIIlllIIlIIIllIIII.lIIlIIIIIllIlIIlII(lIlIllIllllIIlIlll, IllIlllIlllIIIlIll, IlIIIllIIlIlIIIlll, data=lIIIlIIIIIIIIIlllI)
                if llIIIllIlIlllllIlI:
                    lIlIllllllIIIl(IIIIIIIlllllII(0.1, 0.3))
                else:
                    lIlIllllllIIIl(IIIIIIIlllllII(0.5, 1.0))
        with lllllIIlIIlIlI(max_workers=IllIllIIlIIlIIllll) as IlIllIlIllIlllIIIl:
            IllIllIllllIIlllIl = [IlIllIlIllIlllIIIl.submit(IIIIIllllIllIIIlll) for lIlIlIllIlllIIlIIl in lllllllllllllII(IllIllIIlIIlIIllll)]
            for lIllIlIIlIIllllIlI in IllIllIllllIIlllIl:
                lIllIlIIlIIllllIlI.llIIIllIlIlllllIlI()

def IIIIIlllIlIIIIllIl():
    IlIIIIIIlIlllIIlll = lllllllllllllIl('Enter target Bootstrap application URL (e.g., https://example.com): ').strip()
    if not (IlIIIIIIlIlllIIlll.startswith('http://') or IlIIIIIIlIlllIIlll.startswith('https://')):
        llllllllllllllI('[ERROR] Invalid URL. Please include http:// or https://')
        return
    try:
        IlIlIIIllIIllllIlI = llIIllIIIIlIIllllI()
        IlIlIIIllIIllllIlI.IIIlIIIlIlllIIllll(IlIIIIIIlIlllIIlll, workers=30, duration=7200)
    except llllllllllllIll:
        llllllllllllllI('\n[INFO] Test interrupted by user.')
    except lllllllllllllll as IlIIlIIIlIIIllIlll:
        llllllllllllllI(f'[ERROR] Unexpected error occurred: {IlIIlIIIlIIIllIlll}')
if llllllllllllIIl == '__main__':
    IIIIIlllIlIIIIllIl()
