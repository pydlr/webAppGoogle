import re
import urllib2
from bs4 import BeautifulSoup

found = False
link = 'http://www.pjbc.gob.mx/boletinj/2017/my_html/bc171030.htm'

html = urllib2.urlopen(link)

soup = BeautifulSoup(html, 'html.parser')

firstElement = soup.find(text = re.compile(r'H. TRIBUNAL SUPERIOR'))

AUTORIDAD = firstElement
print 'Autoridad: ' + str(AUTORIDAD)

while not found:

	next = firstElement.find_next('span')
	if ('ACUERDOS EN EL RAMO' in next.text):
	 	found = True

	previous = next
	next = next.find_next('span')

print previous.text	



levelNames[] = [""] * 7

levelNames[0] = {	'H. TRIBUNAL SUPERIOR DE JUSTICIA DEL ESTADO DE BAJA CALIFORNIA',
					'JUZGADO PRIMERO CIVIL DE MEXICALI, B.C. 25 DE OCTUBRE DE 2017',
					''}

w, h = 7dela, 5;
levelOptions = [[0 for x in range(w)] for y in range(h)] 

levelOptions = [0] * 7

# AUTORIDAD
levelOptions[0] = {	'H. TRIBUNAL SUPERIOR DE JUSTICIA',
					'JUZGADO'}
# SECRETARIA
levelOptions[1] = { 'ACUERDOS EN EL RAMO',
					'SECCION DE AMPAROS RAMO',
					'NUEVO SISTEMA DE JUSITICIA',
					'SALA',
					'SECRETARIA'}

# TIPO_RESOLUCION
levelOptions[2] = { 'Acuerdos',
					'Admisiones',
					'Audiencias',
					'Sentencias',
					'Exhortos',
					'Cuadernos de Amparo',
					'Cuadernos de Antecedentes'}



def scanHTML(prev_element):

	int i = 0

	while not found:
		next = previous.find_next('span')

		for option in levelOptions[i]:

			if option in next.text:
				found = True 
				levelNames[i] = next.text
				break
		previous = next










# levelOptions = ['simon', 'laura', 'roberto']
# found = False
# while not found:
# 	for option in levelOptions:
# 		print option
# 		if option in 'laura esta aqui':
# 			found = True 
# 			break
# 		print 'in'
# 	print 'out'

