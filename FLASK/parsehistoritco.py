import urllib2
import parse_class

location = 'bc'
 
parser = parse_class.Parser()


# Esta madre tarda com 12 horas en la mac!!!

startyear = 15
startmonth = 04
startday = 23

for year in xrange(startyear,04,-1):
	if year < 10:
		year_string = '0' + str(year)
	else:
		year_string =  str(year)

	for month in xrange(startmonth, 0, -1):
		if month < 10:
			month_string = '0' + str(month)
		else:
			month_string = str(month)

		for day in range(31, 0, -1):
			if day < 10:
				day_string = '0' + str(day)
			else:
				day_string = str(day)


			link = 'http://www.pjbc.gob.mx/boletinj/20' + year_string + '/my_html/bc' +  year_string + month_string + day_string + '.htm'

			try:
				html = urllib2.urlopen(link)
				print link 
				parser.parse(True, False, link)
				
			except Exception as error:
				pass
				
		startday = 31

	startmonth = 12

# http://www.pjbc.gob.mx/boletinj/2015/my_html/bc150423.htm