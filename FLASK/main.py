from    flask       import  Flask, render_template, json, request, redirect, session
from    werkzeug    import  generate_password_hash, check_password_hash
import  MySQLdb     as      mysql 
import  os
import  uuid
import  parse_class 

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

def connect_to_cloudsql():    # When deployed to App Engine, the 'SERVER_SOFTWARE' environment variable
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
        print "Using local mysql:"
        conn = mysql.connect(
            host    = '127.0.0.1',
            user    = 'root',
            passwd  = 'NO',
            db      = dbname)
        print conn

    return conn

@app.route('/parseHtml')
def parseHml():
    # Call parser, false to not save to database
    # TODO: add options for database name etc.
    parser = parse_class.Parser(False) 
    return render_template('demo_signup.html')

@app.route('/parseToday', methods=['GET','POST'])
def parseToday():
    todayslink = str(request.args.get('link'))
    parser = parse_class.Parser(True, False, todayslink)
    return 'Finished'

@app.route('/')
def main():
    # URL arguments:
    # print str(request.args.get('expediente'))
    if session.get('user'):
        url = '/userHome/' + str(session.get('user'))
        return redirect(url)
    else:
        return render_template('index.html')

# This is a dummy function to test cathing any path and using it to render content
# @app.route('/public/<path:path>/')
@app.route('/public')
def bla():
    return render_template('index_carousel.html', first_slider="path")

@app.route('/showSignIn')
def showSignin():
    return render_template('signin.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('demo_signup.html')

@app.route('/showCase', methods=['POST'])
def showCase():

    conn                = connect_to_cloudsql()
    cursor              = conn.cursor()
    expediente          = request.form["inputCase"]
    query = "SELECT no_expediente, autoridad, contenido FROM `resoluciones` WHERE (`autoridad` LIKE '%" + str(expediente) + "%') OR (no_expediente LIKE '%" + str(expediente) + "%');"

    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit() 
    cursor.close() 
    conn.close()

    return render_template('demo_showcase.html', data = data, caso = expediente)

@app.route('/addCase', methods=['POST'])
def addCase():
        case        = request.form["case"]
        autoridad   = request.form["auto"]
        user        = str(session.get('user'))
        if user:
            try:
                conn    = connect_to_cloudsql()
                cursor  = conn.cursor()
                cursor.callproc('sp_insert_usercase', (case, user, autoridad ) )
                data    = cursor.fetchall()
                print data[0][0]
                print len(data)
                
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
                return error

        return "LSD"

@app.route('/removeCase', methods=['GET','POST'])
def removeCase():
        print 'Remove...'
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
            name = str(session.get('user'))
            conn    = connect_to_cloudsql()
            cursor  = conn.cursor()
            # cursor.callproc('sp_validateLogin',(_username,))
            mysql_userdata_query = "SELECT * FROM userinfo WHERE user_name = '" + str(path) + "';"
            cursor.execute(mysql_userdata_query)
            userdata    = cursor.fetchall()

            mysql_cases_query = "SELECT distinct no_expediente FROM usercases WHERE user_name = '" + str(name) + "' ORDER BY no_expediente;" 

            cursor.execute(mysql_cases_query)
            casesdata    = cursor.fetchall()

            big_query = "SELECT no_expediente, autoridad, contenido FROM resoluciones WHERE no_expediente IN ("
            for case in casesdata:
                big_query = big_query + "'" + str(case[0]) + "', "
            big_query = big_query + " '0000/0000');"

            cursor.execute(big_query)
            big_query_data = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template('demo_userhome.html', 
                username=userdata[0][1],
                data = big_query_data)
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

        # connect to mysql
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

    try:
        if request.form['fb']:
            _name       = request.form['fbName']
            if request.form['fbEmail']:
                _email   = request.form['fbEmail']
            else: 
                _email = 'Undefined'

            _password   = "default"

            print _name
            print _email
            print _password
            
        else:
            print "Using own Signup"
            _name       = request.form['inputName']
            _email      = request.form['inputEmailSignUp']
            _password   = request.form['inputPasswordSignUp']
        
        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            # conn                = mysql.connect(host=hostname,user=username,passwd=passwd,db=dbname)
            conn                = connect_to_cloudsql()
            cursor              = conn.cursor()
            _hashed_password    = generate_password_hash(_password)
            cursor.callproc('sp_create_user',(_name,_email,_hashed_password))
            data                = cursor.fetchall()
           
            # if data[0][0]:

            if (len(data) == 0):
                conn.commit()   
                session['user'] = _name
                print "Saved new user"
                return _name

            elif ((data[0][0] == 'Email Exists !!') or
                (data[0][0] == 'Name Exists !!' )):   
                session['user'] = _name
                print "User already exists"
                return _name


            else:
                print 'error here'
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



