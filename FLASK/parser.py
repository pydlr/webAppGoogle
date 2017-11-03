import re
import urllib2
from bs4 import BeautifulSoup

finished = False
levelNames 		= [""] * 7
levelOptions 	= [0] * 7

#

# ======================================================================
def scanHTML(prev_element, i ):

	#AUTORIDAD
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
	for option in levelOptions[i]:
		print 'OPTION: ' +  str(option)


	finished = False
	previous = prev_element
	while not finished:
		next = previous.find_next('span')

		if next == 'EDICTO':
			finished = True 

		for option in levelOptions[i]:

			if option in next:
				
				levelNames[i] = next
				i =+ 1

				if i >= 5:
					i = 3


				break
		previous = next
# ======================================================================


link = 'http://www.pjbc.gob.mx/boletinj/2017/my_html/bc171030.htm'

html = urllib2.urlopen(link)

soup = BeautifulSoup(html, 'html.parser')

firstElement = soup.find(text = re.compile(r'H. TRIBUNAL SUPERIOR'))

AUTORIDAD = firstElement
print 'Autoridad: ' + str(AUTORIDAD)

scanHTML(firstElement, 1)

# while not found:

# 	next = firstElement.find_next('span')
# 	if ('ACUERDOS EN EL RAMO' in next.text):
# 	 	found = True

# 	previous = next
# 	next = next.find_next('span')

# print previous.text

















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

