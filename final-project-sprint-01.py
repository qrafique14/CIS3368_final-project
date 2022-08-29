from flask import Flask, request, make_response, jsonify
import mysql.connector
from mysql.connector import Error


def conn_connection(hostname,connp, username, passwd, dbname):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = hostname,
            port = connp,
            user = username,
            password = passwd,
            database = dbname
        )
        print("Connection Success")
    except Error as e:
        print(f'The error {e}')
    return connection
conn = conn_connection('', '', '', '', '')
curr = conn.cursor(dictionary = True)

app = Flask(__name__)
#i started the code with the db connection
#then i started to write the crud functions ofr each of the tables
def get_login(username, passwd):
    sql = 'select username from login where username = %s and password=%s'
    data = (username, passwd)
    curr.execute(sql, data)
    if curr.fetchall() != 0:
        return True
    return False
# to endure my sanity it used sql and data as the vars to execute the sql and pass data if needed
def create_login(username, password):
    sql = 'insert into login values (null, %s, %s);'
    data = (username, password)
    curr.execute(sql, data)
    curr.execute('commit;')
    return
def reset_login(username, password, id):
    sql = 'update login set username=%s, password=%s where id =%s;'
    data = (username, password, id)
    curr.execute(sql, data)
    curr.execute('commit;')
    return
def delete_login(id):
    sql = 'DELETE FROM login WHERE id=%s;'
    curr.execute(sql, (id,))
    curr.execute('commit;')
    return
def get_trips():
    sql = 'select * from trips;'
    curr.execute(sql)
    return curr.fetchall()
def edit_trips(dest, trans, sdate, edate, name, id):
    sql = 'update trips set destID=%s, transportation=%s, start_date=%s, end_date=%s, tripname=%s where id=%s;'
    data = (dest,trans,sdate,edate,name, id)
    curr.execute(sql, data)
    curr.execute('commit;')
    return
def add_trips(dest, trans, sdate, edate, name):
    sql = 'insert into trips values (null,%s,%s,%s,%s,%s);'
    data = (dest,trans,sdate,edate,name)
    curr.execute(sql, data)
    curr.execute('commit;')
    return
def delete_trips(id):
    sql = 'DELETE FROM trips WHERE id=%s;'
    curr.execute(sql, (id,))
    curr.execute('commit;')
    return
def get_dest():
    sql = 'select * from dest;'
    curr.execute(sql)
    return curr.fetchall()
def edit_dest(con, city, sight, id):
    sql = 'update dest set country=%s, city=%s, sightseeing=%s where id = %s;'
    data = (con, city, sight, id)
    curr.execute(sql, data)
    curr.execute('commit;')
    return
def add_dest(con, city, sight):
    sql = 'insert into dest values(null, %s, %s, %s);'
    data = (con, city, sight)
    curr.execute(sql, data)
    curr.execute('commit;')
    return
def del_dest(id):
    sql = 'DELETE FROM dest WHERE id=%s;'
    curr.execute(sql, (id,))
    curr.execute('commit;')
    return
# I started to make the login route after the sql side of the crud opreations
masterUsername = 'resr'
masterPassword = 'password'
@app.route('/api/login', methods=['GET', 'PUT', 'POST', 'DELETE'])
def home():
    page = request.form
    meth = request.method
    #i have added all the crud methods and put a pass as placeholder, then added all the crud sql functions
    #making sure geting the right values for the functions
    if meth == 'GET':
        #the code below was provide in class
        if request.authorization:
            username = request.authorization.username
            password=request.authorization.password
            if get_login(username,password):
                return '<h1> WE ARE ALLOWED TO BE HERE </h1>'
            return make_response('COULD NOT VERIFY!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
    elif meth == 'PUT':
        username = page['username']
        password = page['password']
        id = page['id']
        reset_login(username, password, id)
        return 'success'
    elif meth == 'POST':
        username = page['username']
        password = page['password']
        create_login(username, password)
        return 'success'
    elif meth == "DELETE":
        id = page['id']
        delete_login(id)
        return 'success'
   # after the login route i create both the trips and dest with the if request methods passholders 
@app.route('/api/trips', methods=['GET', 'POST', 'PUT', 'DELETE'])
def end_trips():
    # i added this to save time
    page = request.form
    # went thought eadt get, post, put and delete and addd their following function
    if request.method == 'GET':
        trips = get_trips()
        return jsonify([trip for trip in trips])
    elif request.method == 'POST':
        dest = page['destination']
        trans = page['transportation']
        sdate = page['start date']
        edate = page['end date']
        name = page['trip name']
        add_trips(dest, trans, sdate,edate,name)
        return 'success'
    elif request.method == 'PUT':
        dest = page['destination']
        trans = page['transportation']
        sdate = page['start date']
        edate = page['end date']
        name = page['trip name']
        id = page['id']
        edit_trips(dest, trans, sdate,edate,name,id)
        return 'success'
    elif request.method == 'DELETE':
        id = page['id']
        delete_trips(id)
        return 'success'
#after coding the last route i started to test each crud opreatrion to ensure they work
#made the following correction as needed
@app.route('/api/destination', methods=['GET', 'POST', 'PUT', 'DELETE'])
def end_dest():
    page = request.form
    if request.method == 'GET':
        dests = get_dest()
        return jsonify([dest for dest in dests])
    elif request.method == 'POST':
        con = page['country']
        city = page['city']
        sight = page['sightseeing']
        add_dest(con,city,sight)
        return 'success'
    elif request.method == 'PUT':
        con = page['country']
        city = page['city']
        sight = page['sightseeing']
        id = page['id']
        edit_dest(con,city,sight, id)
        return 'success'
    elif request.method == 'DELETE':
        id = page['id']
        del_dest(id)
        return 'success'

app.run()
