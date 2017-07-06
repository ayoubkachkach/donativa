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
    result = cur.execute("SELECT account_username, account_password, account_type FROM ACCOUNTS WHERE account_username = %s ", [args[0]])
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
    return (True, data[2])

def get_types(mysql):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT DISTINCT type_id, type_name FROM OFFER_TYPES")
    data = cur.fetchall()
    choices = [(g[0], g[1]) for g in data]
    return choices

