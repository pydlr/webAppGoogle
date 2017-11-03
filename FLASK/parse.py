import re
import urllib2
from bs4 import BeautifulSoup

finished = False
DB_ENTRIES 		= [""] * 7
levelOptions 	= [0] * 7


#AUTORIDAD
levelOptions[0] = [	'H. TRIBUNAL SUPERIOR DE JUSTICIA',
					'JUZGADO']
# SECRETARIA
levelOptions[1] = [ 'ACUERDOS EN EL RAMO',
					'SECCION DE AMPAROS RAMO',
					'NUEVO SISTEMA DE JUSITICIA',
					'SALA',
					'SECRETARIA']

# TIPO_RESOLUCION
levelOptions[2] = [ 'Acuerdos',
					'Admisiones',
					'Audiencias',
					'Sentencias',
					'Exhortos',
					'Cuadernos de Amparo',
					'Cuadernos de Antecedentes']

# ======================================================================
def main():
	

	link = 'http://www.pjbc.gob.mx/boletinj/2017/my_html/bc171030.htm'
	print 'Scraping: ' + link
	html = urllib2.urlopen(link)

	soup = BeautifulSoup(html, 'html.parser')

	firstElement = soup.find(text = re.compile(r'H. TRIBUNAL SUPERIOR'))

	AUTORIDAD = firstElement
	i = 0
	DB_ENTRIES[i] = AUTORIDAD
	print 'Autoridad: ' + str(AUTORIDAD)

	scanHTML(firstElement , i+1)
# ======================================================================


# ======================================================================
# i = El numero de columna en la base de datos
def scanHTML(prev_element, i ):
	finished = False
	while not finished:
		# print 'before'
		# print prev_element 
		next_element = prev_element.find_next('span')
		if next_element.text.find('EDICTO') != -1:
			print 'finishing'
			print 'Edicto: ' + str(next_element.text.find('EDICTO'))
			finished = True
		# print 'after'
		# print 'i: ' + str(i)
		# print levelOptions[i]
		for option in levelOptions[i]:
			# if option.find(str(next_element.text.strip())) != -1:
			# print next_element.text
			if next_element.text.find(option) != -1:

				# print 'in for cycle: '
				# print next_element.text.strip()
				DB_ENTRIES[i] = next_element.text.strip()

				if i == 2:
					nextd = next_element.find_next('td')

					while nextd.name.find('td') != -1:

						# NUMERO DE CASO EN LA HOJA 
						DB_ENTRIES[i+1] = nextd.text.strip()

						# NUMERO DE EXPEDIENTE
						nextd = nextd.find_next('td')
						DB_ENTRIES[i+2] = nextd.text.strip()


						# TEXTO DE LA RESOLUCION
						nextd = nextd.find_next('td')
						DB_ENTRIES[i+3] = nextd.text.strip()

						print 'DB: ' + str(DB_ENTRIES)

						next_element = nextd

						# Find out if the table continues
						nextd = next_element.find_next().find_next().find_next().find_next().find_next().find_next()

					# scanHTML(next_element, 0)
					
				# scanHTML( next_element, i+1)
				i += 1
				if i > 2:
					i = 2
				# print 'new i: '  + str(i)

				break
		prev_element = next_element
		# scanHTML(next_element,i













	# for option in levelOptions[i]:
	# 	print 'OPTION: ' +  str(option)


	# finished = False
	# previous = prev_element
	# while not finished:
	# 	next = previous.find_next('span')

	# 	if next == 'EDICTO':
	# 		finished = True 

	# 	for option in levelOptions[i]:

	# 		if option in next:
				
	# 			levelNames[i] = next
	# 			i =+ 1

	# 			if i >= 5:
	# 				i = 3


	# 			break
	# 	previous = next
# ======================================================================


if __name__ == "__main__":
	main()