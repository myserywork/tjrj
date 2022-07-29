from pprint import pprint
import requests
import digits
import threading
import sys
import json

TIMEOUT = 10

proxies = {
    'http':'socks5://localhost:9050',
    'https':'socks5://localhost:9050'
}

def get_firsts(servs, serv):
    l, n = 0, 1000
    num=None
    while l==0:
        if n > 0: print(f'{num} does not exists')
        num = digits.format_novo(str(n), serv)
        params = {'numProcesso':num}
        print(num)
        try:
            with requests.get('http://www4.tjrj.jus.br/numeracaoUnica/faces/index.jsp', timeout=TIMEOUT, params=params) as r:
                l = len(r.history)
                with open('lasts.json', 'w') as f:
                    json.dump(servs, f, indent=4)
                n += 1
        except KeyboardInterrupt:
            return
        except Exception as e:
            print('could not access website', e, file=sys.stderr)
    servs[serv]=n

if __name__ == '__main__':
    with open('lasts.json') as f:
        servs = json.load(f)

    threads = list()
    for serv in servs:
        if serv in sys.argv:
            t = threading.Thread(target=get_firsts, args=(servs, serv))
            threads.append(t)
            t.start()

    while threading.active_count() > 0:
        try:
            pass
        except KeyboardInterrupt:
            pass
    with open('lasts.json', 'w') as f:
        json.dump(servs, f, indent=4)
