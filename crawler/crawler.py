from crawler.digits import format_antigo
from database import Processo, getDbSession
from datetime import datetime
import requests
import threading
import time
import json

URL = 'https://www3.tjrj.jus.br/consultaprocessual/api/processos/por-numero/movimentos'

TIMESET = 300

def proc_parse(data: dict) -> Processo:
    if 'personagens' not in data:
        data['personagens'] = []
    if 'advogados' not in data:
        data['advogados'] = []
    proc = Processo(
        numero_cnj=data['codCnj'],
        numero_antigo=data['codProc'],
        date_dist=datetime.strptime(data.get('dataDis'), '%d/%m/%Y'),
        datetime_in=datetime.now(),
        segredo=data['indSegrJust']=='S',
        idoso=data.get('descricaoPrioridadeIdoso'),
        acao=data.get('txtAcao'),
        assunto=data.get('txtAssunto'),
        serventia=data.get('descServ'),
        vara=data.get('descVara'),
        rito=data.get('descRito'),
        tipo_recurso=data.get('tipoDeRecurso'),
        informacoes_autos=data.get('textoInformacoesAutosProcesso'),
        polo_ativo = '|'.join([f"{p.get('descPers')}:{p['nome']}" for p in data['personagens'] if p['tipoPolo']=='A']),
        polo_passivo = '|'.join([f"{p.get('descPers')}:{p['nome']}" for p in data['personagens'] if p['tipoPolo']=='P']),
        advogados = '|'.join([f'{adv["nomeAdv"]}:{adv["numOab"]}' for adv in data['advogados']]),
        dividas_ativas=json.dumps(data.get('dividaAtivas')),
        movimentos=json.dumps(data.get('movimentosProc')),
        serv_code=data['serv_code']
    )
    return proc

def commit_lasts(lasts):
    f = open('lasts.json', 'w')
    json.dump(lasts, f, indent=4)
    f.close()

def checksLive(lasts: dict, serv: str, timeout: float = 10.0):
    n = int(lasts[serv])
    db_session = getDbSession()
    with db_session.begin():
        while True:
            num_formated = format_antigo(str(n), serv)
            print(f'{serv}\tGetting {num_formated}...')

            data = {'codigoProcesso':num_formated}
            r = requests.post(URL, json=data, timeout=timeout)
            lasts[serv]=n
            commit_lasts(lasts)
            if r.status_code == 200:
                print('Adding to database')
                proc_data = r.json()
                proc_data['serv_code'] = serv
                db_session.add(proc_parse(proc_data))

                n+=1
            else:
                fail=True
                while fail:
                    try:
                        db_session.commit()
                        time.sleep(300)
                        fail=False
                    except Exception as e:
                        print(e)
                        time.sleep(60)


class Crawler:

    def __init__(self, lasts: dict, timeout: float = 10.0):
        self.lasts = lasts
        self.threads = list()
        self.timeout = timeout

    def start(self):
        for serv in self.lasts:
            t = threading.Thread(target=checksLive, args=(self.lasts, serv, self.timeout))
            self.threads.append(t)
            t.start()

        for t in self.threads:
            t.join()
