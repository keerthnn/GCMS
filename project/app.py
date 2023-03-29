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

# -----------------------------------------   HOME ----------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('home.html')

# -------------------------------------------  LOGIN FOR FARMER   ------------------------------------------------------


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

# ---------------------------------------LOGOUT ----------------------------------------------------------------


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('fid', None)
    session.pop('username', None)
    return redirect(url_for('home'))


# --------------------------------------------REGISTER FOR FARMER-------------------------------------------------------------

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
    


# ---------------------------------------LOGIN FOR GRASS CUTTER---------------------------------------------------------


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
            return  render_template('gclogin.html', mesage = mesage)
    return render_template('gclogin.html')


# -----------------------------------------REGISTER FOR GRASS CUTTER----------------------------------------------------


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
            return  render_template('gcregister.html', mesage = mesage)
        elif not username or not password :
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO GRASS_CUTTER VALUES(NULL, %s , %s , %s , %s ,%s,%s)',(name,address,phone,username,password,charges))
            mesage = 'You have successfully registered !'
        mysql.connection.commit()
        cursor.close()
        return  render_template('gclogin.html', mesage = mesage)
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return  render_template('gcregister.html', mesage = mesage)



# ----------------------------------------FARMER DASHBOARD----------------------------------------------------


@app.route('/fdashboard')
def fdashboard():

    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * FROM LAND where fid={0}""".format(session['fid']))
    land=cursor.fetchall()
    cursor.execute("""SELECT * FROM LAND_TYPE where fid={0}""".format(session['fid']))
    details=cursor.fetchall()
    # Stored procedure
    cursor.execute("CALL `getGrassCutter`()")
    data=cursor.fetchall()
    cursor.execute("""SELECT * from BOOK_LIST where fid={0}""".format(session['gid']))
    available=cursor.fetchall()
    cursor.execute("""SELECT * FROM BILL where fid={0}""".format(session['fid']))
    result=cursor.fetchall()
    cursor.close()

     
    return  render_template('fdashboard.html', details=details,land=land,data=data,available=available,result=result)



# -------------------------------------- BOOKING ---------------------------------------------------------



@app.route('/booking',methods=['POST','GET'])
def booking():

    print("=========================================")
    val2 = [j for j in request.form.values()]
    print(val2)
    
    mesage = ''
    if request.method == 'GET':
        return  render_template('booking.html')
     
    if request.method == 'POST' and 'fid' in request.form and 'fname' in request.form and 'address' in request.form and 'phone' in request.form and 'gid' in request.form:
        fid = request.form['fid']
        fname = request.form['fname']
        address = request.form['address']
        phone = request.form['phone']
        gid = request.form['gid']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM BOOK_LIST WHERE fid = % s AND gid = % s', (fid,gid, ))
        account = cursor.fetchone()
        if account:
            mesage = 'already booked !'
            return  render_template('booking.html', mesage = mesage)
        else:
            cursor.execute(' INSERT INTO BOOK_LIST VALUES(NULL, %s, %s , %s , %s, %s)',(fid,fname,address,phone,gid))
            mesage = 'You have successfully booked !'
        mysql.connection.commit()
        cursor.close()
        return  render_template('fdashboard.html', mesage = mesage)
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return  render_template('fdashboard.html', mesage = mesage)

# ------------------------------------GRASS CUTTER DASHBOARD-------------------------------------------------------------

#-------------------------------------DISPLAY  ---------------------------------------------------------------------------

@app.route('/gcdashboard')
def gcdashboard():

    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * from BOOK_LIST where gid={0}""".format(session['gid']))
    data=cursor.fetchall()
    cursor.execute("""SELECT * from REPAIR_SHOP where gid={0}""".format(session['gid']))
    result=cursor.fetchall()
    cursor.execute("""SELECT * FROM BILL where gid={0}""".format(session['gid']))
    bill=cursor.fetchall()
    cursor.close()
    return  render_template('gcdashboard.html', data=data,result=result,bill=bill)

# -------------------------------------  SHOP OPTION FOR GRASS CUTTER------------------------------------------------

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
        cursor.execute('SELECT * FROM REPAIR_SHOP WHERE gid = % s AND tools =%s'  , (gid, tools,))
        account = cursor.fetchone()
        if account:
            mesage = 'already bought !'
            return  render_template('shop.html', mesage = mesage)
        else:
            cursor.execute(' INSERT INTO REPAIR_SHOP VALUES( %s , %s , %s, %s)',(shop_name,tools,tool_cost,gid))
            mesage = 'You have successfully bought !'
            
        mysql.connection.commit()
        cursor.close()
        return  render_template('gcdashboard.html', mesage = mesage)
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return  render_template('gcdashboard.html', mesage = mesage)


# -------------------------------------- BILLING ---------------------------------------------------------



@app.route('/billing',methods=['POST','GET'])
def billing():

    print("=========================================")
    val2 = [j for j in request.form.values()]
    print(val2)
    
    mesage = ''
    if request.method == 'GET':
        return  render_template('billing.html')
     
    if request.method == 'POST' and 'fid' in request.form and 'fname' in request.form and 'gid' in request.form and 'gcname' in request.form and 'charges' in request.form:
        # bill_id = request.form['bill_id']
        fid = request.form['fid']
        fname = request.form['fname']
        gid = request.form['gid']
        gcname = request.form['gcname']
        charges = request.form['charges']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM BILL WHERE fid = % s AND gid = % s', (fid,gid, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Bill already generated !'
            return  render_template('billing.html', mesage = mesage)
        else:
            cursor.execute(' INSERT INTO BILL VALUES(NULL, %s , %s , %s, %s, %s)',(fid,fname,gid,gcname,charges))
            mesage = 'Bill successfully generated ! !'
        mysql.connection.commit()
        cursor.close()
        return  render_template('gcdashboard.html', mesage = mesage)
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return  render_template('gcdashboard.html', mesage = mesage)


# -------------------------------------  LAND    -------------------------------------------------------------------------------

@app.route('/land',methods=['POST','GET']) 
def land():

    print("=========================================")
    val2 = [j for j in request.form.values()]
    print(val2)
    
    mesage = ''
    if request.method == 'GET':
        return  render_template('land.html')
     
    if request.method == 'POST' and 'srvy_no' in request.form and 'area' in request.form and 'fid' in request.form:
        srvy_no = request.form['srvy_no']
        area = request.form['area']
        fid = request.form['fid']
        # gid = request.form['gid']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM LAND WHERE srvy_no = % s ', (srvy_no, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Survey number already exist!'
            return  render_template('land.html', mesage = mesage)
        else:
            cursor.execute(' INSERT INTO LAND VALUES( %s , %s , %s)',(srvy_no,area,fid))
            
        mysql.connection.commit()
        cursor.close()
        return  render_template('fdashboard.html', mesage = mesage)
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return  render_template('fdashboard.html', mesage = mesage)

# -------------------------------------  LAND  DETAILS   -------------------------------------------------------------------------------



#used trigger to automatically fill land type
# ------------------------------------------------  ---TRIGGER    -----------------------------------------
@app.route('/details',methods=['POST','GET']) 
def details():

    print("=========================================")
    val2 = [j for j in request.form.values()]
    print(val2)
    
    mesage = ''
    if request.method == 'GET':
        return  render_template('details.html')
     
    if request.method == 'POST' and 'srvy_no ' in request.form and 'fid' in request.form and 'land_type' in request.form :
        srvy_no  = request.form['srvy_no ']
        fid = request.form['fid']
        land_type = request.form['land_type']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute("""Update LAND_TYPE set srvy_no ='{0}',fid ='{1}' ,land_type = '{2}' where srvy_no ={0}""".format(request.form['srvy_no '], request.form['fid'],request.form['land_type']))
            
        mysql.connection.commit()
        cursor.close()
    return  render_template('fdashboard.html', mesage = mesage)


# ---------------------------------------------------- UPDATE--------------------------------------------------------

@app.route('/updatebill',methods=['POST','GET'])
def updatebill():

    print("=========================================")
    val2 = [j for j in request.form.values()]
    print(val2)

    mesage = ''
    if request.method == 'GET':
        return  render_template('updatebill.html')
     
    if request.method == 'POST' and 'bill_id' in request.form and 'fid' in request.form and 'fname' in request.form and 'gid' in request.form and 'gcname' in request.form and 'charges' in request.form:
        bill_id = request.form['bill_id']
        fid = request.form['fid']
        fname = request.form['fname']
        gid = request.form['gid']
        gcname = request.form['gcname']
        charges = request.form['charges']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""Update BILL set charges = {5} where bill_id={0} AND fid = {1} AND gid= {3} """.format(request.form['bill_id'], request.form['fid'],
                                                                request.form['fname'],request.form['gid'],
                                                                request.form['gcname'],request.form['charges']))

        mysql.connection.commit()
        cursor.close()
        return  render_template('gcdashboard.html', mesage = mesage)
    return  render_template('gcdashboard.html', mesage = mesage)


# -------------------------------------- DELETE BOOKING ---------------------------------------------------------




@app.route('/delete',methods=['POST','GET'])
def delete():

    print("=========================================")
    val2 = [j for j in request.form.values()]
    print(val2)
    
    mesage = ''
    if request.method == 'GET':
        return  render_template('delete.html')
     
    if request.method == 'POST' and 'bid' in request.form and 'fid' in request.form and 'fname' in request.form and 'gid' in request.form:
        bid = request.form['bid']
        fid = request.form['fid']
        fname = request.form['fname']
        # address = request.form['address']
        # phone = request.form['phone']
        gid = request.form['gid']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""DELETE from BOOK_LIST where bid = {0}""".format(request.form['bid']))

        
        mesage = 'You have successfully booked !'
        mysql.connection.commit()
        cursor.close()
        return  render_template('fdashboard.html', mesage = mesage)
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return  render_template('fdashboard.html', mesage = mesage)



# -----------------------------------------------------------------------------------------------------------------------

if __name__=="__main__":
    app.run(debug=True)