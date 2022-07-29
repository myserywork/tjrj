# funções úteis para a numeração

def digito_v_antigo(antigoId):
	#soma = (int(antigoId[-1]) + int(antigoId[0]))*2
	a = 2
	mult = 2
	for i in range(len(antigoId)-1, -1, -1):
		a += int(antigoId[i])*mult
		mult+=1
		if mult > 12: mult=2
	#print(a)
	b = a % 11
	if b == 10:
		return '0'
	return str(b)

def digito_v_antigo2020(antigoId):
	a = (int(antigoId[-1]) + int(antigoId[0]))*2

	for i in range(11):
		a += int(antigoId[i+1])*(13-i)
	b = a % 11
	if b == 10:
		return '0'
	return str(b)

#def digito_antigo(antigoId):


# Coloca no formato antigo já com o dígito
def format_antigo(num, serv, ano='2022'):
	if len(serv) == 4:
		serv = serv[1:]
	num = (6-len(num))*'0' + num
	num = ano+serv+num
	if ano=='2020':
		digito = digito_v_antigo2020(num)
	else:
		digito = digito_v_antigo(num)
	processoNum = '{}.{}.{}-{}'.format(ano, serv, num[7:13], digito)
	return processoNum


# Recebe numeração nova (NNNNNNNNNNNNNNNNNNN) e retona o dígito (string)
def digito_v_novo(novoId):

	if len(novoId) != 18:
		return None
	novoId += '00'
	num = 0
	for i in range(20):
		num += int(novoId[i])*10**(19-i)
	digito = 98 - (num % 97)
	if digito >= 10:
		return str(digito)

	elif digito < 10 and digito >= 1:
		return '0'+str(digito)

	elif digito == 0:
		return '00'

#recebe um número e uma serventia. Coloca no formato padrão novo, já com o dígito.
def format_novo(num: str, serv, trib='2022819'):
	num = '0'*(7-len(num))+num
	num += trib+serv
	digito = digito_v_novo(num)
	processoNum = '{}{}{}{}{}{}{}-{}{}.{}{}{}{}.{}.{}{}.{}{}{}{}'.format(num[0], num[1], num[2], num[3], num[4], num[5], num[6], digito[0], digito[1], num[7], num[8], num[9], num[10], num[11], num[12], num[13], num[14], num[15], num[16], num[17])
	return processoNum
