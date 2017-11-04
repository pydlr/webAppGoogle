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
					'Cuadernos De Antecedentes']

# ======================================================================
def main():
	

	link = 'http://www.pjbc.gob.mx/boletinj/2017/my_html/bc171030.htm'
	print 'Scraping: ' + link
	# html = urllib2.urlopen(link)
	# html = urllib2.urlopen("file://boletin.html")

	# soup = BeautifulSoup(html, 'html.parser')
	soup = BeautifulSoup(open("boletin.html"), 'html.parser')

	firstElement = soup.find(text = re.compile(r'H. TRIBUNAL SUPERIOR'))

	AUTORIDAD = firstElement
	i = 0
	DB_ENTRIES[i] = AUTORIDAD
	print 'Autoridad: ' + str(AUTORIDAD)

	next_element = firstElement.find_next('span')

	scanHTML(next_element , i+1)
# ======================================================================

# ======================================================================
# i = El numero de columna en la base de datos
def scanHTML(next_element, i ):

	finished = False
	alreadyIncremented = False
	prev_element = next_element;


	while not finished:
		alreadyIncremented = False
		# next_element = prev_element.find_next('span')

		# =======EXIT CONDITION=======
		if next_element.text.find('EDICTO') != -1:
			print 'finishing'
			# print 'Edicto: ' + str(next_element.text.find('EDICTO'))
			finished = True
		#==============================

		# =======EXIT CONDITION=======
		# if next_element.text.find('MARIA DOLORES MORENO ROMERO') != -1:
		# 	print 'finishing'
		# 	# print 'Edicto: ' + str(next_element.text.find('EDICTO'))
		# 	finished = True
		#============================== 
		

		# print next_element
		# print str(i) + 'looking for: ' + str(next_element)
		for option in levelOptions[i]:

			if next_element.text.find(option) != -1:

				DB_ENTRIES[i] = next_element.text.strip()
				print str(i) + ' : Entry : ' + str(DB_ENTRIES[i].encode('utf-8'))

				# Tabla
				if i == 2:
					nextd = next_element.find_next('td')
					# print 'find_next'

					while  ((nextd.name.find('td') != -1) or
							(nextd.name.find('tr') != -1)):

						if (nextd.name.find('tr') != -1):
							# print 'here'
							nextd = nextd.find_next('td')
							# print nextd

						# NUMERO DE CASO EN LA HOJA 
						DB_ENTRIES[i+1] = nextd.text.strip()

						# NUMERO DE EXPEDIENTE
						nextd = nextd.find_next('td')
						DB_ENTRIES[i+2] = nextd.text.strip()

						# TEXTO DE LA RESOLUCION
						nextd = nextd.find_next('td')
						DB_ENTRIES[i+3] = nextd.text.strip()

						print str(i) + ': DB: ' + str(DB_ENTRIES)
						next_element = nextd
						# print next_element.name

						# Find out if the table continues
						nextd = nextd.find_next().find_next().find_next().find_next().find_next()
						
						# print 'nextd'
						# print nextd
						
					i = 0; 
				# print str(i) + ' : AFTER WHILE : ' + str(next_element)

				# print str(i) + 'pre-break: ' + str(next_element)
				next_element = next_element.find_next('span')
				i = 0
				#print next_element
				alreadyIncremented = True
				# print str(i) +  ' : break: ' + str(next_element)
				break
				# if i <= 2:
				# 	i += 1
				# else:
				# 	i = 2 
				# 	next_element = prev_element.find_next('span')

			# if not alreadyIncremented:# CREO QUE ESTE FIND NEXT NO DEBERIA ESTAR AQUI, SOLO CUANDO SE LLEGA A 3 SE INCREMENTA
			# 	next_element = next_element.find_next('span')
			# 	print str(i) + 'next_element: ' + str(next_element)
			# 	alreadyIncremented = True
			# Not finding next because we did not find nothing
			# next_element = next_element.find_next('span')
			# alreadyIncremented = True
			# # break
			# i += 1
			# if i > 2:
			# 	i = 0

		i += 1
		if i >2:
			
			i = 0
			# if not incremented yet!!!!!! TODO
			next_element = next_element.find_next('span')
			# print str(i) +  ' : past_3: ' + str(next_element)
			# print 'blah' + str(next_element.text.find(levelOptions[2][6]))

			# exit()

		# if not alreadyIncremented:
		# 	if i < 2:
		# 		i += 1
		# 	else:
		# 		i = 0 
		# 		if not alreadyIncremented:
		# 			next_element = next_element.find_next('span')
		# 			alreadyIncremented = True



		prev_element = next_element



# # ======================================================================
# # i = El numero de columna en la base de datos
# def scanHTML(prev_element, i ):
# 	finished = False
# 	while not finished:
		
# 		
# 		next_element = prev_element.find_next('span')
# 		if next_element.text.find('EDICTO') != -1:
# 			print 'finishing'
# 			print 'Edicto: ' + str(next_element.text.find('EDICTO'))
# 			finished = True

# 		for option in levelOptions[i]:

# 			if next_element.text.find(option) != -1:

# 				DB_ENTRIES[i] = next_element.text.strip()

# 				if i == 2:
# 					nextd = next_element.find_next('td')

# 					while nextd.name.find('td') != -1:

# 						# NUMERO DE CASO EN LA HOJA 
# 						DB_ENTRIES[i+1] = nextd.text.strip()

# 						# NUMERO DE EXPEDIENTE
# 						nextd = nextd.find_next('td')
# 						DB_ENTRIES[i+2] = nextd.text.strip()


# 						# TEXTO DE LA RESOLUCION
# 						nextd = nextd.find_next('td')
# 						DB_ENTRIES[i+3] = nextd.text.strip()

# 						print 'DB: ' + str(DB_ENTRIES)
# 						next_element = nextd

# 						# Find out if the table continues
# 						nextd = next_element.find_next().find_next().find_next().find_next().find_next().find_next()

# 				i += 1
# 				if i > 2:
# 					i = 2

# 				break
# 		prev_element = next_element





if __name__ == "__main__":
	main()