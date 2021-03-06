import re
import urllib2
from bs4 import BeautifulSoup
import  MySQLdb     as      mysql 
import os
import argparse


#===========================   PARSER CONFIG =======================
finished = False
DB_ENTRIES 		= [""] * 7
levelOptions 	= [0] * 7
#AUTORIDAD
levelOptions[0] = [	'H. TRIBUNAL SUPERIOR DE JUSTICIA',
					'JUZGADO']
# SECRETARIA
levelOptions[1] = [ 'ACUERDOS EN EL RAMO',
					'SECCION DE AMPAROS RAMO',
					'NUEVO SISTEMA DE JUSTICIA PENAL']

levelOptions[2] = [ 'SALA',
					'SECRETARIA']

# TIPO_RESOLUCION
levelOptions[3] = [ 'Acuerdos',
					'Admisiones',
					'Audiencias',
					'Sentencias',
					'Exhortos',
					'Cuadernos de Amparo',
					'Cuadernos De Antecedentes']
#===========================  PARSER CONFIG =======================



#===========================  MYSQL  CONFIG =======================
username    = 'root'
passwd      = 'NO'
dbname      = 'demo_users'
hostname    = 'localhost'
tablename   = 'resoluciones'



# These environnment variables are configured in app.yaml
CLOUDSQL_CONNECTION_NAME    = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER               = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD           = os.environ.get('CLOUDSQL_PASSWORD')
#===========================  MYSQL  CONFIG =======================


# ==========================    SQL     =============================
class MySQLConnection:

	def connect_to_cloudsql(self):


	    # When deployed to App Engine, the 'SERVER_SOFTWARE' environment variable
	    # will be set to 'Google App Engine/version'.
	    if os.getenv('SERVER_SOFTWARE','').startswith('Google App Engine/'):
	        # Connect using the unix socket located at
	        # /cloudsql/cloudsql-connection-name.
	        cloudsql_unix_socket = os.path.join(
	            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

	        conn = mysql.connect(
	            unix_socket = cloudsql_unix_socket,
	            user        = CLOUDSQL_USER,
	            passwd      = CLOUDSQL_PASSWORD,
	            db          = dbname)

	    # If the unix socket is unavailable, then try to connect using TCP. This 
	    # will work if you are running a local MySQL server or using the Clud SQL
	    # proxy, for example:
	    #
	    #   $ cloud_sql_proxy -instances=abogangster-182717:europe-west3:boletin=tcp:3306
	    #

	    else:
	        print "local mysql"
	        conn = mysql.connect(
	            host    = '127.0.0.1',
	            user    = 'root',
	            passwd  = 'NO',
	            db      = dbname)
	        print conn

	    return conn
# ==========================    SQL     =============================

class Parser():

	# ==========================  MAIN ================================
	def __init__(self	):
		
		return None
	# ==========================    MAIN    ===============================

	def parse(self, writeToDatabase = False, localfile = False, link = 'http://www.pjbc.gob.mx/boletinj/2017/my_html/bc171030.htm', datos = None):
	
		# link = 'http://www.pjbc.gob.mx/boletinj/2017/my_html/bc171030.htm'
		# http://www.pjbc.gob.mx/boletinj/2017/my_html/bc171106.htm
		print 'Scraping: ' + link

		self.database = writeToDatabase
		if self.database:
			print 'Saving to database'
		else:
			print 'Printing to Terminal only'

		if not localfile:
			html = urllib2.urlopen(link)
			soup = BeautifulSoup(html, 'html.parser')
		else:
			soup = BeautifulSoup(open(link), 'html.parser')

		firstElement = soup.find(text = re.compile(r'H. TRIBUNAL SUPERIOR'))

		AUTORIDAD = firstElement
		i = 0
		DB_ENTRIES[i] = AUTORIDAD.encode('utf-8').replace('\n', ' ').replace('\r', '')

		next_element = firstElement.find_next('span')

		newdata = self.scanHTML(next_element , i+1, datos)

		return newdata

	# ===========================   PARSER  =============================
	# i = El numero de columna en la base de datos
	def scanHTML(self, next_element, i, datos ):

		finished = False
		alreadyIncremented = False
		prev_element = next_element;

		mysql_connection = MySQLConnection()
		conn = mysql_connection.connect_to_cloudsql()
		cursor = conn.cursor()

		while not finished:
			alreadyIncremented = False

			# =======EXIT CONDITION=======
			if next_element.text.find('EDICTO') != -1:
				print 'The End'
				finished = True
				cursor.close()
				conn.close()
			#==============================

			for option in levelOptions[i]:
				# If we find a match, but only if the matchin text is a title, 
				# ignore table content 
				if next_element.text.find(option) != -1	: 

					# Solo si las coincidencias tienen tag b o i, asi esta el formato del boletin
					if (next_element.parent.name.find('b') != -1 or 
						next_element.parent.name.find('i') != -1):

						if i == 0:	
							# Nueva Autoridad, limpiando columnas		
							DB_ENTRIES[0] = ''
							DB_ENTRIES[1] = ''
							DB_ENTRIES[2] = ''

						DB_ENTRIES[i] = next_element.text.strip()

					
					if (next_element.find_next().find_next().name.find('table') != -1):
					# 	next_element.find_next().find_next().find_next().name.find('table') != -1):
						i = 3
						# Limpiar la columna siguiente
						DB_ENTRIES[i] = ''

					# Tabla
					if i == 3:

						nextd = next_element.find_next('td')

						while  ((nextd.name.find('td') != -1) or
								(nextd.name.find('tr') != -1) or
								 nextd.parent.name.find('td') != -1):

							# find the next td
							if (nextd.name.find('tr') != -1):
								nextd = nextd.find_next('td')
							# find the next td	
							if (nextd.parent.name.find('td') != -1):
								nextd = nextd.parent

							# NUMERO DE CASO EN LA HOJA 
							if nextd.text.find('/') == -1: # el if revisa si no hay este campo (numero de acuerdo)
								DB_ENTRIES[i+1] = nextd.text.strip()
								nextd = nextd.find_next('td')
							else: 
								DB_ENTRIES[i+1] = ''
							
							# NUMERO DE EXPEDIENTE
							DB_ENTRIES[i+2] = nextd.text.strip()

							# TEXTO DE LA RESOLUCION
							nextd = nextd.find_next('td')
							DB_ENTRIES[i+3] = nextd.text.strip()

							#print str(i) + ': DB: ' + str(DB_ENTRIES)
							
							# MYSQL QUERY!!!!!!!!
							if self.database:

								cursor.callproc('sp_insert_resolucion',(
									DB_ENTRIES[0].encode('utf-8').replace('\n', ' ').replace('\r', ''),
									DB_ENTRIES[1].encode('utf-8').replace('\n', ' ').replace('\r', ''),
									DB_ENTRIES[2].encode('utf-8').replace('\n', ' ').replace('\r', ''),
									DB_ENTRIES[3].encode('utf-8').replace('\n', ' ').replace('\r', ''),
									DB_ENTRIES[4].encode('utf-8').replace('\n', ' ').replace('\r', ''),
									DB_ENTRIES[5].encode('utf-8').replace('\n', ' ').replace('\r', ''),
									DB_ENTRIES[6].encode('utf-8').replace('\n', ' ').replace('\r', ''),))

								data = cursor.fetchall()
								if len(data) is 0:
									conn.commit()

								# See if new data is relevant to users and count it
								if datos:
									for rows in datos:
										if rows[0] == str(DB_ENTRIES[5]):
											# print "ENTRIES" + str(DB_ENTRIES[5])
											rows[2] += 1

							next_element = nextd

							# Find out if the table continues
							nextd = nextd.find_next().find_next().find_next().find_next().find_next().find_next()
							
						i = 0; 

					next_element = next_element.find_next('span')
					i = -1
					break

			i += 1
			if i >3:
				
				i = 0
				next_element = next_element.find_next('span')

		if datos:
			return datos
	# ===========================   PARSER  =============================



if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	# store to the databes true or false
	parser.add_argument("-db",
						"--database", 
						help="save to database",
	                    action="store_true",
	                    default = False)

	# use a localfile instead of a link
	parser.add_argument("-l",
						"--localfile", 
						help="save to database",
	                    action="store_true",
	                    default = False)

	args = parser.parse_args()

	boletinParse = Parser.parse(args.database, args.localfile)
	