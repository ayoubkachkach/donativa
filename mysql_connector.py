from flask_mysqldb import MySQL
import _mysql_exceptions 

def create_donor(mysql, args):
    try:
        cur = mysql.connection.cursor()
        result_args = cur.callproc('createDonor', args)
        cur.close()
        mysql.connection.commit()
        return True
    except _mysql_exceptions.OperationalError as e:
        print(e) 
        return False
    
def create_organization(mysql, args):
    try:
        cur = mysql.connection.cursor()
        result_args = cur.callproc('createOrganization', args)
        cur.close()
        mysql.connection.commit()
        return True
    except _mysql_exceptions.OperationalError as e:
        print(e)
        return False

def login_user(mysql, args):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT account_username, account_password, account_type, account_id FROM ACCOUNTS WHERE account_username = %s ", [args[0]])
    #if no user with username is found
    if result == 0:
    	cur.close()
    	return (False, 0)
    data = cur.fetchone()
    password_candidate = args[1]
    password = data[1]
    cur.close()
    #if passwords do not match
    if password_candidate != password:
        return (False, 0)
    return (True, data[2], data[3])

def get_types(mysql):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM OFFER_TYPES", [])
    data = cur.fetchall()
    choices = [(g[0], g[1]) for g in data]
    cur.close()
    return choices

def add_donation(mysql, args):
    cur = mysql.connection.cursor()
    result_args = cur.callproc('createOffer', args)
    data = cur.fetchone()
    print(data)
    cur.close()
    mysql.connection.commit()

def get_requests(mysql, a_id):
    cur = mysql.connection.cursor()
    cur.execute(" SELECT ORG.organization_name, ORG.organization_picture, OFF.offer_title, OFF.offer_id FROM REQUEST R INNER JOIN ORGANIZATIONS ORG ON R.account_id = ORG.account_id INNER JOIN OFFERS OFF ON R.offer_id = OFF.offer_id WHERE R.request_status = 0 AND OFF.account_id = %s;",[a_id])
    data = cur.fetchall() #returns a list of tuples
    myrequests = [(r[0], r[1], r[2]) for r in data]
    cur.close()
    return myrequests
    
def get_number_requests (mysql, a_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(R.account_id) FROM REQUEST R INNER JOIN OFFERS OFF ON R.offer_id = OFF.offer_id WHERE OFF.account_id = %s;",[a_id])
    n_requests = cur.fetchall() #returns a list of tuples
    cur.close()
    return n_requests

