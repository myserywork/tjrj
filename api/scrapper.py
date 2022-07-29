'''
Aqui é o scrapper em si. Na maior parte foi utilizado regex, já que o site do tjrj é uma bagunça completa.
O BeutifulSoup foi usado só para soletar a <table>, para a identificação dos padrões ficarem mais fáceis.

A função get_data vai retornar todos os dados da table em forma de dicionário, dado um html(string), o número do processo(string) e a serventia(string).
'''
from bs4 import BeautifulSoup
import re
import bs4

# get keywords
with open('./api/keywords.txt') as f:
	keywords = f.read().split('\n')
	keywords = set(keywords)

def get_data(html, numProcesso, serv):
	try:
		soup = BeautifulSoup(html, 'html.parser')
	except TypeError:
		return None
	data = {'num-antigo':numProcesso, 'serventia-code':serv}

	# distrib date ################
	infos = soup.findAll('td', class_='info')
	data['réu'] = '-'
	data['autor'] = '-'
	for info in infos:
		txt = info.get_text().strip().replace(' ', '').replace(':', '').lower()
		#print(txt)
		if txt in keywords:
			# while until find info as tag
			while info is not None and type(info.next_sibling) is not bs4.element.Tag:
				info = info.next_sibling
			if info is not None:
				data[txt] = info.next_sibling.text.strip().replace('  ', '').replace('\r\n', '|').replace('\xa0', '')


	'''
	table = soup.find('table')
	if table == None:
		return None
	p = re.compile('Distribuído em\n                          (\d\d/\d\d/\d\d\d\d)')
	ps = p.findall(table.get_text())
	if len(ps) > 0:
		data['data-de-distribuicao'] = ps[0]
	else:
		data['data-de-distribuicao'] = '-'

	#Serventia
	p = re.compile('(Comarca|Regional) d[a|o|e] \s*([^\s]*)')
	ps = p.search(html)
	if ps != None:
		data['serventia'] = ps.group()
	else:
		data['serventia'] = '-'
	#n nov
	p = re.compile('\d{7}-\d{2}.\d{4}.\d.\d\d.\d{4}') #0019147-06.2020.8.19.0002
	ps = p.search(html)
	if ps != None:
		data['numProcesso'] = ps.group()
	else:
		data['numProcesso'] = '-'

	# ofício de registro
	p = re.compile('\dº Ofício \s*([^\n]*)')
	ps = p.search(html)
	if ps != None:
		data['oficio'] = ps.group()
	else:
		data['oficio'] = '-'
	# advogados
	p = re.compile('[A-Z]{2}\d{6}\n                           - \n                          .*([^\n]*)')
	ps = p.findall(table.get_text())
	if len(ps) == 0:
		p = re.compile('[A-Z]{2}\d{6}\n                          \xa0-\xa0\n                          \s*([^\n]*)')
		ps = p.findall(table.get_text())
		if len(ps) != 0:
			data['advogados'] = '|'.join(ps)
		else: data['advogados'] = '-'

	else: data['advogados'] = '|'.join(ps)


	#Classe
	p = re.compile('Classe:\n\n                        \s*([^\n]*)')
	ps = p.search(table.get_text())
	if ps != None:
		data['classe'] = ps.group().split('\n\n                        ')[1]
	else: data['classe'] = '-'

	#Polo Ativo
	nomes = 'Autor do Fato|Polo Ativo|Autor|Requerente|Exequente|Embargante|Agravante|Apelante|Demandante|reconvinte|Denunciante|Reclamante|Representante|REPTE|Interessado|Declarante|Credor|Impugnante|Recorrente|Impetrante'
	p = re.compile('({})(\n                        \n\n                          ).*([^\n]*)'.format(nomes))
	ps = p.search(table.get_text())
	if ps != None:
		ps_split = ps.group().split('\n                        \n\n                          ')
		data['polo-ativo'] = '|'.join(ps_split).replace('e outro(s)...', '')
	else: data['polo-ativo'] = '-'

	#Polo passivo
	nomes = 'Envolvido|Polo Passivo|Réu|Requerido|Executado|Embargado|Agravado|Apelado|Demandado|reconvindo|Denunciado|Reclamado|Representado|REPDO|Declarado|Devedor|Impugnado|Recorrido|impetrado'
	p = re.compile('({})(\n                        \n\n                          ).*([^\n]*)'.format(nomes))
	ps = p.search(table.get_text())
	if ps != None:
		ps_split = ps.group().split('\n                        \n\n                          ')
		data['polo-passivo'] = '|'.join(ps_split)
	else: data['polo-passivo'] = '-'

	#Assunto
	p = re.compile('(Assunto:\n\n                        ).*([^\n]*)')
	ps = p.search(table.get_text())
	if ps != None:
		data['assuntos'] = ps.group().split('\n\n                        ')[1]
	else: data['assuntos'] = '-'

	#ação
	p = re.compile('(Ação:\n\n                        ).*([^\n]*)')
	ps = p.search(table.get_text())
	if ps != None:
		data['acao'] = ps.group().split('\n\n                        ')[1]
	else: data['acao'] = '-'

	#endereço
	p = re.compile('(Endereço:\n\n                        ).*([^\n]*)')
	ps = p.search(table.get_text())
	if ps != None:
		data['endereco'] = ps.group().split('\n\n                        ')[1]
	else: data['endereco'] = '-'

	#Bairro
	p = re.compile('(Bairro:\n\n                        ).*([^\n]*)')
	ps = p.search(table.get_text())
	if ps != None:
		data['bairro'] = ps.group().split('\n\n                        ')[1]
	else: data['bairro'] = '-'

	#Cidade
	p = re.compile('(Cidade:\n\n                        ).*([^\n]*)')
	ps = p.search(table.get_text())
	if ps != None:
		data['cidade'] = ps.group().split('\n\n                        ')[1]
	else: data['cidade'] = '-'

	#Pŕoxima Audiência
	p = re.compile('(Próxima\nAudiência:\n\n                        ).*([^\n]*)')
	ps = p.search(table.get_text())
	if ps != None:
		data['proxima-audiencia'] = ps.group().split('\n\n                        ')[1]
	else: data['proxima-audiencia'] = '-'

	#HOra da audiencia
	p = re.compile('(Hora da Audincia:\n\n                        ).*([^\n]*)')
	ps = p.search(table.get_text())
	if ps != None:
		data['hora-audiencia'] = ps.group().split('\n\n                        ')[1]
	else: data['hora-audiencia'] = '-'

	#Tipo da audiencia
	p = re.compile('(Tipo da Audiencia:\n\n                        ).*([^\n]*)')
	ps = p.search(table.get_text())
	if ps != None:
		data['tipo-audiencia'] = ps.group().split('\n\n                        ')[1]
	else: data['tipo-audiencia'] = '-'

	#Data de conclusão
	p = re.compile('(Data da conclusão:\n\n                        ).*([^\n]*)')
	ps = p.search(table.get_text())
	if ps != None:
		data['data-conclusao'] = ps.group().split('\n\n                        ')[1]
	else: data['data-conclusao'] = '-'

	#Localização na serventia:
	p = re.compile('(Localização \nna serventia:\n\n                        ).*([^\n]*)')
	ps = p.search(table.get_text())
	if ps != None:
		data['localizacao-na-serventia'] = ps.group().split('\n\n                        ')[1]
	else: data['localizacao-na-serventia'] = '-'

	# Juiz
	p = re.compile('(Juiz:\n).*([^\n]*)')
	ps = p.search(table.get_text())
	if ps != None:
		data['juiz'] = ps.group().split('\n')[1]
	else: data['juiz'] = '-'

	# INFORMAÇÕES DOS MOVIMENTOS HTML
	p = re.compile('<tr><td colspan=2>&nbsp;</td></tr>')
	start = p.search(html)
	p = re.compile('\n\n                                \n                            \n                            \n                        \n                        <tr>\n                          <td colspan="2">&nbsp;</td>\n')

	end = p.search(html)
	if start != None and end != None:
		data['movimentos'] = html[start.span()[0]:end.span()[0]]
	else: data['movimentos'] = '-'
	'''


	return data
