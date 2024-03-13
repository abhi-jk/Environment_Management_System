from flask import Flask, render_template, request,send_file,jsonify
import mysql.connector
import matplotlib.pyplot as plt
import io
import numpy as np

app = Flask(__name__)
 
 
mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="abhij226024",
    database="env"
)
 
mycursor = mydb.cursor()
 
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/login')
def login():
    return render_template('login.html')
 
@app.route('/register')
def user_register():
    return render_template('user_register.html')

@app.route('/adminlogin')
def admin():
    return render_template('admin_login.html')

@app.route('/air')
def air():
    return render_template('air_quality.html')

@app.route('/temp')
def temp():
    return render_template('temp.html')

@app.route('/water')
def water():
    return render_template('water.html')
 
@app.route('/adduser',methods=['get','post'])
def addemp():
    if request.method == 'POST' or request.method =='post':
        name = request.form.get('name')
        uname = request.form.get('username')
        password = request.form.get('password')
       
        query="insert into register(name,user, password) values (%s,%s,%s)"
        data = (name,uname,password)
        mycursor.execute(query,data)
        mydb.commit()
        return render_template('login.html')
    return render_template('user_register.html')
 
data = {}
 
@app.route('/home',methods=['post'])
def search():
    error = None
    uname = request.form.get('username')
    upass = request.form.get('password')
    query = f"select * from register where user like '{uname}' and password like '{upass}'"
    mycursor.execute(query)
    data = mycursor.fetchall()
    if data:
        return render_template('user.html')
    else:
        error = 'Invalid Credentials. Please try again.'
    return render_template('login.html',error=error)
    
@app.route('/admins',methods=['post'])
def admins():
    error = None
    id = request.form.get('admin_id')
    password = request.form.get('password')
    query = f"select * from admins where id like '{id}' and password like '{password}'"
    mycursor.execute(query)
    data = mycursor.fetchall()
    if data:
        return render_template('admin.html')
    else:
        error = 'Invalid Credentials. Please try again.'

    return render_template('admin_login.html', error=error)

@app.route('/data')
def data():

    # Execute a query to fetch the data
    mycursor.execute("SELECT * FROM water_quality")

    # Fetch all the rows
    rows = mycursor.fetchall()

    # Close the cursor and connection

    # Convert the rows to a list of dictionaries and return as JSON
    data = [dict(zip(mycursor.column_names, row)) for row in rows]
    return jsonify(data)

@app.route('/admin/water_quality', methods=['GET'])
def get_water_quality():

    mycursor.execute("SELECT * FROM water_quality")
    data = mycursor.fetchall()
    return render_template('water_quality.html', data=data)

@app.route('/admin/water_quality', methods=['POST'])
def create_water_quality():
    # Get the data from the form
    loc = request.form.get('location')
    pH = request.form.get('pH')
    Chlorine = request.form.get('Chlorine')
    hardness = request.form.get('hardness')

    mycursor.execute("INSERT INTO water_quality (Location,pH, Chlorine,Hardness) VALUES (%s,%s, %s,%s)", (loc,pH, Chlorine, hardness))
    mydb.commit()

    mycursor.execute("SELECT * FROM water_quality")
    data = mycursor.fetchall()
    return render_template('water_quality.html', data=data)

@app.route('/admin/water_quality/<int:id>', methods=['POST'])
def handle_water_quality(id):
    # Get the operation from the form
    operation = request.form.get('_method')

    # Get the data from the form
    loc = request.form.get('location')
    pH = request.form.get('pH')
    Chlorine = request.form.get('Chlorine')
    hardness = request.form.get('hardness')

    if operation == 'update':
        # Update the data in the database
        mycursor.execute("UPDATE water_quality SET Location = %s,pH = %s, Chlorine = %s,Hardness=%s WHERE id = %s", (loc,pH, Chlorine,hardness, id))
    elif operation == 'delete':
        # Delete the data from the database
        mycursor.execute("DELETE FROM water_quality WHERE id = %s", (id,))

    mycursor.execute("SELECT * FROM water_quality")
    data = mycursor.fetchall()
    return render_template('water_quality.html', data=data)
 
if __name__ == '__main__':
    app.run(debug=True)