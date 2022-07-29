import requests

url = 'https://www3.tjrj.jus.br/consultaprocessual/api/processos/por-numero/publica'

def get_processo(number, tipo):
    data = {'numProcesso':number, 'tipoProcesso':str(tipo)}
    with requests.post(url, json=data) as r:
        try:
            proc = r.json()
        except KeyboardInterrupt:
            return None
        except Exception as e:
            print(e)
            return None
    return proc
