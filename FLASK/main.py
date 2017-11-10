from __future__ import unicode_literals

from    flask       import  Flask, render_template, json, request, redirect, session
from    werkzeug    import  generate_password_hash, check_password_hash

import  MySQLdb     as      mysql 
import  os
import  uuid
import  parse_class 

# TODO: Hacer una clase y  objeto User ?
# TODO: Abstraer todas las llamadas a mysql, en una sola funcion


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/Uploads'
app.secret_key = 'why would I tell you my secret key?'
app.debug = True

# MySQL configurations
username    = 'root'
passwd      = 'NO'
dbname      = 'demo_users'
hostname    = 'localhost'
tablename   = 'userinfo'


# These environnment variables are configured in app.yaml
CLOUDSQL_CONNECTION_NAME    = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER               = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD           = os.environ.get('CLOUDSQL_PASSWORD')

# SignUp
@app.route('/admin')
def admin():

    user        = str(session.get('user'))

    if (user == 'Resonant Digit' or 
        user == 'Roberto'):
        print 'Logged as admin'
        return render_template('demo_admin.html')

    else:
        return render_template('demo_error.html', error='Unauthorized access')

# MySQL connection to either Google App Engine's SQL instance or default to the local database
# The local database has to have the local mysql server running
def connect_to_cloudsql():    
    # Google App Engine:
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
        print 'Using Google cloud sql'
        print conn 

    # If the unix socket is unavailable, then try to connect using TCP. This 
    # will work if you are running a local MySQL server or using the Clud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=abogangster-182717:europe-west3:boletin=tcp:3306
    #

    # Local MySQL:
    else:
        conn = mysql.connect(
            host    = '127.0.0.1',
            user    = 'root',
            passwd  = 'NO',
            db      = dbname)

        print "Using localhost"
        print conn
    return conn

# Call parser, false to not save to database
# use parseToday
# TODO: add options for database name etc.
@app.route('/parseHtml')
def parseHml():
    parser = parse_class.Parser(False) 
    return render_template('demo_signup.html')

# Parse html from link in the url, or local file i.e.
# /parseToday?link=http://www.pjbc.gob.mx/boletinj/2017/my_html/bc171030.htm
# http://www.pjbc.gob.mx/boletinj/2017/my_html/bc171106.htm
# boletin.html
@app.route('/parseFromLink', methods=['GET','POST'])
def parseFromLink():

    # The name of file or URL come from the gui
    link = str(request.form['inputLink'])

    # MySQL connection & query
    query = "SELECT * FROM usercases;"
    print query
    conn                = connect_to_cloudsql()
    cursor              = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    # No_Expediente - Username - nuevaResolucion
    datos = []
    for rows in data:
        datos.append ( [ rows[1], rows[2],  0])

    parser = parse_class.Parser()
    #newdata = parser.parse(datos, writeToDatabase = True, localfile = False, link) 
    newdata = parser.parse(datos, True, False, link) 
    print newdata

    ##### AGGREGATE NEWS INTO USERS PROFILE TO NOTIFY THEM 
    query = "SELECT user_name FROM userinfo;"
    print query
    conn                = connect_to_cloudsql()
    cursor              = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    
    print ' DATA: ' + str(data)

    notificaciones = 0
    for user in data:
        for row in newdata:
            if row[1] == user[0]:
                notificaciones += row[2]
        print notificaciones 

        query = "UPDATE userinfo SET notificaciones = '" + str(notificaciones) + "' where user_name = '" + str(user[0]) + "';"
        print query
        cursor.execute(query)
        try:
            conn.commit()
        except Exception as error:
            print error
        print 'FETCH: ' + str(cursor.fetchall())
        notificaciones = 0 

    cursor.close()
    conn.close()


    return redirect('/admin')

@app.route('/sqlCommand', methods=['GET','POST'])
def sqlCommand():
    query = str(request.form['inputQuery'])
    print query
    conn                = connect_to_cloudsql()
    cursor              = conn.cursor()

    cursor.execute(query)

    data = cursor.fetchall()
    print data

    if(conn.commit()): 
        print 'commit()'
    cursor.close()
    conn.close()

    datos = []

    for rows in data:
        datos.append ( [ rows[1], rows[2],  0])

    return redirect('/admin')

# ################################################# MAIN  
@app.route('/')
def main():
    if session.get('user'):
        url = '/userHome/' + str(session.get('user'))
        return redirect(url)
    else:
        return render_template('index.html')

# SignIn
@app.route('/showSignIn')
def showSignin():
    return render_template('signin.html')

# SignUp
@app.route('/showSignUp')
def showSignUp():
    return render_template('demo_signup.html')

# Search Table 
@app.route('/showCase', methods=['POST'])
def showCase():
    try:
        # MySQL call 
        conn                = connect_to_cloudsql()
        cursor              = conn.cursor()

        # Encode otherwise no one undestands what you wrote
        # expediente          = str(request.form["inputCase"].encode('utf-8').replace('\n', ' ').replace('\r', ''))
        # expediente = str(request.form['inputCase'])
        # expediente = '1892/2015'
        # expediente = unicode(expediente, 'utf-8')
        # expediente = expediente.encode('utf-8')
        expediente = request.form['inputCase']
        print 'expediente ' + str(expediente)
        if expediente == 'all':
            print 'here'
            query = "SELECT no_expediente, autoridad, tipo, contenido from `resoluciones`"
        else:
            query = "SELECT no_expediente, autoridad, tipo, contenido FROM resoluciones WHERE (`autoridad` LIKE '%" + str(expediente) + "%') OR (no_expediente LIKE '%" + str(expediente) + "%') OR (tipo LIKE '%" + str(expediente) + "%');"
        print query
        cursor.execute(query)
        print "after query"
        data = cursor.fetchall()
        print 'len: ' + str(len(data))
        # print data
        # print data[0][0]
        conn.commit() 
        cursor.close() 
        conn.close()
    except Exception as error:
        print "Error in query: " + str(error)

    return render_template('demo_showcase.html', data = data, caso = expediente)

@app.route('/addCase', methods=['POST'])
def addCase():
        case        = request.form["case"].encode('utf-8',"replace" ).replace('\n', ' ').replace('\r', '')
        autoridad   = request.form["auto"].encode('utf-8',"replace" ).replace('\n', ' ').replace('\r', '')

        print case
        print autoridad

        user        = str(session.get('user'))
        if user:
            try:
                conn    = connect_to_cloudsql()
                cursor  = conn.cursor()
                print 'before proc'
                cursor.callproc('sp_insert_usercase', (case, user, autoridad ) )
                print 'after proc'
                data    = cursor.fetchall()
                print data
                if len(data) == 0:
                    conn.commit()
                    cursor.close()
                    conn.close()
                    print 'Added case ' + str(case) + ' to user ' + str(user) 
                    return 'Added case ' + str(case) + ' to user ' + str(user) 
                else:
                    cursor.close()
                    conn.close()
                    print 'Could not add case'
                    return 'Could not add case'
            except Exception as error:
                print " Add case error: " + str(error)
                return error

        return "LSD"

@app.route('/removeCase', methods=['GET','POST'])
def removeCase():
        case        = request.form["case"]
        autoridad   = request.form["auto"]
        user        = str(session.get('user'))
        print case
        print autoridad

        if user:
            try:
                conn    = connect_to_cloudsql()
                cursor  = conn.cursor()
                cursor.callproc('sp_delete_usercase', (case, user, autoridad ) )
                data    = cursor.fetchall()
                conn.commit()
                cursor.close()
                conn.close()
                print data
                path = '/'
                return redirect(path)

            except Exception as error:
                print error 
                return error

        return "LSD"

@app.route('/userHome/<path:path>/',methods=['GET','POST'])
def userHome(path):
    try:

        if str(session.get('user')) == str(path):
            name        = str(session.get('user'))
            conn        = connect_to_cloudsql()
            cursor      = conn.cursor()
            # cursor.callproc('sp_validateLogin',(_username,))
            mysql_userdata_query = "SELECT * FROM userinfo WHERE user_name = '" + str(path) + "';"
            cursor.execute(mysql_userdata_query)
            userdata    = cursor.fetchall()

            mysql_cases_query = "SELECT distinct no_expediente FROM usercases WHERE user_name = '" + str(name) + "' ORDER BY no_expediente;" 

            cursor.execute(mysql_cases_query)
            casesdata   = cursor.fetchall()

            big_query   = "SELECT no_expediente, autoridad, tipo, contenido FROM resoluciones WHERE no_expediente IN ("
            for case in casesdata:
                big_query = big_query + "'" + str(case[0]) + "', "
            big_query   = big_query + " '0000/0000');"
 
            cursor.execute(big_query)
            big_query_data = cursor.fetchall()


            # Clear new notifications
            query = "UPDATE userinfo SET notificaciones = '0' WHERE user_name = '" + str(name) + "';"
            cursor.execute(query)
            try:
                conn.commit()
            except Exception as error:
                print error

            cursor.close()
            conn.close()




            return render_template('demo_userhome.html', 
                username=userdata[0][1],
                data = big_query_data,
                notificaciones = str(userdata[0][4]) + ' Nuevas resoluciones')
        else:
            return render_template('demo_error.html',error = 'Unauthorized Access')

    except Exception as e:
        return render_template('demo_error.html', error = e)

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # Connect to mysql
        conn    = connect_to_cloudsql()
        cursor  = conn.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data    = cursor.fetchall()
 
        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][1]
                path = 'userHome/'+str(session['user'])
                return redirect(path)
            else:
                return render_template('demo_error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('demo_error.html',error = 'Wrong Email address or Password.')
 
 
    except Exception as e:
        return render_template('demo_error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()
        # return render_template('loginerror.html',error = 'Unauthorized Access')

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    print 'simon'
    # fb =   request.args.get('fb')
    fb = request.form['fb']
    print fb
    # Login with Facebook
    if fb == '1':
        print 'facebook'
        _name       = request.form['fbName']
        if request.form['fbEmail']:
            _email   = request.form['fbEmail']
        else: 
            _email = 'Undefined'

        _password   = "default"

    # Request from our interface
    else: 
        _name       = request.form['inputName']
        _email      = request.form['inputEmailSignUp']
        _password   = request.form['inputPasswordSignUp']
        
    try:

        # Validate the received values
        if _name and _email and _password:

            # MySQL process
            conn                = connect_to_cloudsql()
            cursor              = conn.cursor()
            _hashed_password    = generate_password_hash(_password)
            cursor.callproc('sp_create_user',(_name,_email,_hashed_password))
            data                = cursor.fetchall()

            # Creation succesful! 
            if (len(data) == 0):
                conn.commit()   
                session['user'] = _name
                return _name

            # User is already in database
            elif (data[0][0] == 'User Exists!'):   
                session['user'] = _name
                return _name

            # Everything went wrong, cry!
            else:
                print 'DB error'
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:

        return json.dumps({'error':str(e)})

    finally:
        # TODO: This shit is bad, if name email and password are not valid, no cursor nor conn will
        # have been created so here they will be null, fix this!
        cursor.close() 
        conn.close()

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # file upload handler code will be here
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
        return json.dumps({'filename':f_name})


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5555)



