from    flask       import  Flask, render_template, json, request, redirect, session
from    werkzeug    import  generate_password_hash, check_password_hash
import  MySQLdb     as      mysql 
import  os
import  uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/Uploads'
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
username    = 'root'
passwd      = 'NO'
dbname      = 'Boletin0'
hostname    = 'localhost'
tablename   = 'tbl_user'


# These environnment variables are configured in app.yaml
CLOUDSQL_CONNECTION_NAME    = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER               = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD           = os.environ.get('CLOUDSQL_PASSWORD')

def connect_to_cloudsql():
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
            db      = 'Boletin0')

    return conn

@app.route('/')
@app.route('/main')
def main():

    return render_template('index.html')

# This is a dummy function to test cathing any path and using it to render content
# @app.route('/public/<path:path>/')
@app.route('/public')
def bla():
    # print path
    return render_template('index_carousel.html', first_slider="path")



@app.route('/showSignIn')
def showSignin():
    return render_template('signin.html')

@app.route('/showSignUp')
def showSignUp():
    # return render_template('signup.html')
    return render_template('demo_signup.html')


@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userhome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')



@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        print _username
        print _password

        # connect to mysql
        conn    = connect_to_cloudsql()
        cursor  = conn.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data    = cursor.fetchall()
 
        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
 
 
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()
        # return render_template('loginerror.html',error = 'Unauthorized Access')


@app.route('/getProfile')
def getProfile():
    try:
        print "1"
        if session.get('user'):
            print "2"
            _user = session.get('user')

            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetWishByUser',(_user,))
            wishes = cursor.fetchall()
            print "3"
            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                        'Id': wish[0],
                        'Title': wish[1],
                        'Description': wish[2],
                        'Date': wish[4]}
                wishes_dict.append(wish_dict)

            return json.dumps(wishes_dict)
        else:
            print "4"
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        print "5"
        return render_template('error.html', error = str(e))


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    # return render_template('index.html')
    print ("/../" + request.form['filePath1'])

    try:
        _name       = request.form['inputName']
        _email      = request.form['inputEmail']
        _password   = request.form['inputPassword']
        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL
            # conn              = mysql.connect(host=hostname,user=username,passwd=passwd,db=dbname)
            conn                = connect_to_cloudsql()
            cursor              = conn.cursor()
            _hashed_password    = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data                = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully!'})
                # return render_template('index_table.html', data = data)
            else:
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


@app.route('/display')        
def display():
    conn                = connect_to_cloudsql()
    cursor              = conn.cursor()
    # query               = 'SELECT * from tbl_user'
    cursor.execute('SELECT user_id, user_name, user_username from tbl_user')
    # cursor.execute('SELECT * from tbl_user')

    data = cursor.fetchall()
    conn.commit()
    cursor.close() 
    conn.close()
    return render_template('index_table.html', data = data)

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
    app.run()



