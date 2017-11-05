import re
import urllib2
from bs4 import BeautifulSoup
import  MySQLdb     as      mysql 
import os


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


# ==========================  MAIN ================================
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
# ==========================    MAIN    ===============================


# ==========================    SQL     =============================
def connect_to_cloudsql():
    print 'here'
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



# ===========================   PARSER  =============================
# i = El numero de columna en la base de datos
def scanHTML(next_element, i ):

	finished = False
	alreadyIncremented = False
	prev_element = next_element;


	conn = connect_to_cloudsql()
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

						print str(i) + ': DB: ' + str(DB_ENTRIES)
						
						# MYSQL QUERY!!!!!!!!
						cursor.callproc('sp_insert_resolucion',(
							DB_ENTRIES[0].encode('utf-8'),
							DB_ENTRIES[1].encode('utf-8'),
							DB_ENTRIES[2].encode('utf-8'),
							DB_ENTRIES[3].encode('utf-8'),
							DB_ENTRIES[4].encode('utf-8'),
							DB_ENTRIES[5].encode('utf-8'),
							DB_ENTRIES[6].encode('utf-8')))
						# cursor.callproc('sp_insert_resolucion',(
						# 	DB_ENTRIES[0].encode('latin-1', 'replace') ,
						# 	DB_ENTRIES[1].encode('latin-1', 'replace') ,
						# 	DB_ENTRIES[2].encode('latin-1', 'replace') ,
						# 	DB_ENTRIES[3].encode('latin-1', 'replace') ,
						# 	DB_ENTRIES[4].encode('latin-1', 'replace') ,
						# 	DB_ENTRIES[5].encode('latin-1', 'replace') ,
						# 	DB_ENTRIES[6].encode('latin-1', 'replace')))

						data = cursor.fetchall()
						if len(data) is 0:
							conn.commit()



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
# ===========================   PARSER  =============================



if __name__ == "__main__":
	main()