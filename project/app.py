from flask import Flask, request, render_template, request, redirect, url_for, session ,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from functools import wraps

app=Flask(__name__)

app.secret_key = 'xyzsdfg'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gcms'

mysql = MySQL(app)

# -----------------------------------------------------------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('home.html')

# -----------------------------------------------------------------------------------------------------------------------


@app.route('/flogin', methods=['POST','GET'])
def flogin():

    print("=========================================")
    val1 = [i for i in request.form.values()]
    print(val1)

    mesage = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM FARMER WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['fid'] = account['fid']
            session['username'] = account['username']
            mesage = 'Logged in successfully !'
            # flash('Logged in successfully !')
            return render_template('fdashboard.html', mesage = mesage)

        elif not username or not password :
            mesage = 'Please fill out the form !'
        else:
            
            mesage = 'Incorrect username / password !'
            return  render_template('flogin.html', mesage = mesage)
    return render_template('flogin.html')

# -----------------------------------------------------------------------------------------------------------------------


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('fid', None)
    session.pop('username', None)
    return redirect(url_for('home'))


# -----------------------------------------------------------------------------------------------------------------------

@app.route('/fregister', methods=['POST','GET'])
def fregister():
    print("=========================================")
    val2 = [j for j in request.form.values()]
    print(val2)
    
    mesage = ''
    if request.method == 'GET':
        return  render_template('fregister.html')
     
    if request.method == 'POST' and 'name' in request.form and 'address' in request.form and 'phone' in request.form and 'username' in request.form and 'password' in request.form:
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM FARMER WHERE username = % s ', (username, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Username already exists !'
        elif not username or not password :
            mesage = 'Please fill out the form !'
        else:
            cursor.execute(' INSERT INTO FARMER VALUES(NULL, %s , %s , %s , %s ,%s)',(name,address,phone,username,password))
            mesage = 'You have successfully registered !'
        mysql.connection.commit()
        cursor.close()
        return  render_template('flogin.html', mesage = mesage)
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return  render_template('fregister.html', mesage = mesage)
    


# -----------------------------------------------------------------------------------------------------------------------


@app.route('/gclogin', methods=['POST','GET'])
def gclogin():

    print("=========================================")
    val1 = [i for i in request.form.values()]
    print(val1)

    mesage = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM GRASS_CUTTER WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['gid'] = account['gid']
            session['username'] = account['username']
            mesage = 'Logged in successfully !'
            return render_template('gcdashboard.html', mesage = mesage)

        elif not username or not password :
            mesage = 'Please fill out the form !'
        else:
            
            mesage = 'Incorrect username / password !'
            return  render_template('home.html', mesage = mesage)
    return render_template('gclogin.html')


# -----------------------------------------------------------------------------------------------------------------------


@app.route('/gcregister', methods=['POST','GET'])
def gcregister():
    print("=========================================")
    val2 = [j for j in request.form.values()]
    print(val2)
    
    mesage = ''
    if request.method == 'GET':
        return  render_template('gcregister.html')
     
    if request.method == 'POST' and 'name' in request.form and 'address' in request.form and 'phone' in request.form and 'username' in request.form and 'password' in request.form and 'charges' in request.form:
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']
        charges = request.form['charges']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM GRASS_CUTTER WHERE username = % s ', (username, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Username already exists !'
        elif not username or not password :
            mesage = 'Please fill out the form !'
        else:
            cursor.execute(' INSERT INTO GRASS_CUTTER VALUES(NULL, %s , %s , %s , %s ,%s,%s)',(name,address,phone,username,password,charges))
            mesage = 'You have successfully registered !'
        mysql.connection.commit()
        cursor.close()
        return  render_template('gclogin.html', mesage = mesage)
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return  render_template('gcregister.html', mesage = mesage)



# -----------------------------------------------------------------------------------------------------------------------


@app.route('/fdashboard')
def fdashboard():

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM GRASS_CUTTER")
    data=cursor.fetchall()
    cursor.close()

    
    return  render_template('fdashboard.html', data=data)



# -----------------------------------------------------------------------------------------------------------------------



@app.route('/booking',methods=['POST','GET'])
def booking():

    print("=========================================")
    val2 = [j for j in request.form.values()]
    print(val2)
    
    mesage = ''
    if request.method == 'GET':
        return  render_template('booking.html')
     
    if request.method == 'POST' and 'fname' in request.form and 'address' in request.form and 'phone' in request.form and 'gid' in request.form:
        fname = request.form['fname']
        address = request.form['address']
        phone = request.form['phone']
        gid = request.form['gid']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM BOOKING WHERE fname = % s ', (fname, ))
        account = cursor.fetchone()
        if account:
            mesage = 'already booked !'
        else:
            cursor.execute(' INSERT INTO BOOKING VALUES(NULL, %s , %s , %s, %s)',(fname,address,phone,gid))
            mesage = 'You have successfully booked !'
        mysql.connection.commit()
        cursor.close()
        return  render_template('fdashboard.html', mesage = mesage)
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return  render_template('fdashboard.html', mesage = mesage)

# -----------------------------------------------------------------------------------------------------------------------



@app.route('/gcdashboard')
def gcdashboard():

    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * from BOOKING where gid={0}""".format(session['gid']))
    data=cursor.fetchall()
    cursor.execute("""SELECT * from REPAIR_SHOP where gid={0}""".format(session['gid']))
    result=cursor.fetchall()
    cursor.close()
    return  render_template('gcdashboard.html', data=data,result=result)

# -----------------------------------------------------------------------------------------------------------------------

@app.route('/shop',methods=['POST','GET'])
def shop():

    print("=========================================")
    val2 = [j for j in request.form.values()]
    print(val2)
    
    mesage = ''
    if request.method == 'GET':
        return  render_template('shop.html')
     
    if request.method == 'POST' and 'shop_name' in request.form and 'tools' in request.form and 'tool_cost' in request.form and 'gid' in request.form:
        shop_name = request.form['shop_name']
        tools = request.form['tools']
        tool_cost = request.form['tool_cost']
        gid = request.form['gid']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM REPAIR_SHOP WHERE tools = % s ', (tools, ))
        account = cursor.fetchone()
        if account:
            mesage = 'already bought !'
        else:
            cursor.execute(' INSERT INTO REPAIR_SHOP VALUES( %s , %s , %s, %s)',(shop_name,tools,tool_cost,gid))
            mesage = 'You have successfully bought !'
        mysql.connection.commit()
        cursor.close()
        return  render_template('gcdashboard.html', mesage = mesage)
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return  render_template('gcdashboard.html', mesage = mesage)




# -----------------------------------------------------------------------------------------------------------------------

if __name__=="__main__":
    app.run(debug=True)
