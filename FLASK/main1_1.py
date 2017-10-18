# Import the Flask frameworkand the Flask interfaces 
from flask import Flask, render_template, request
import 	MySQLdb 	as 		mysql
# import MySQLdb

# Create an instance of Flask class and assign it to a variable
app = Flask(__name__)



@app.route('/')
def main():
    return render_template('index.html')

# Create a request handler that displays a form using the form.htl template
# When the user navigates to the /form/ directory within the application
# the form.html template will be displayed
@app.route('/form')
def form():
	return render_template('form.html')

# Create a request handler that handles the information from the 
# submitted form:
# Store the form info into these variables. To post them into the 
# submitted_form.html template 
@app.route('/submitted' , methods=['POST'])
def submitted_form():
	name = request.form['name']
	email = request.form['email']
	site = request.form['site_url']
	comments = request.form['comments']

	return render_template(
		'submitted_form.html',
		name=name,
		email=email,
		site=site,
		comments=comments)




if __name__ == "__main__":
	app.run()


