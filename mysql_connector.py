from flask_mysqldb import MySQL
import _mysql_exceptions 

import helpers

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

        cur = mysql.connection.cursor()
        result_args = cur.execute("SELECT account_id FROM ACCOUNTS WHERE account_username = %s", [args[1]])
        a_id = cur.fetchone();
        cur.close()
        mysql.connection.commit()
        return (True, a_id[0])
    except _mysql_exceptions.OperationalError as e:
        print(e)
        return (False, 0)

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
    return data[0] #donation_id

def get_requests(mysql, a_id):
    cur = mysql.connection.cursor()
    cur.execute(" SELECT ORG.organization_name, ORG.organization_picture, OFF.offer_title, OFF.offer_id, ORG.account_id FROM REQUEST R INNER JOIN ORGANIZATIONS ORG ON R.account_id = ORG.account_id INNER JOIN OFFERS OFF ON R.offer_id = OFF.offer_id WHERE R.request_status = 0 AND OFF.account_id = %s;",[a_id])
    data = cur.fetchall() #returns a list of tuples
    myrequests = [(r[0], r[1], r[2], r[3],r[4]) for r in data]
    cur.close()
    return myrequests
    
def get_number_requests (mysql, a_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(R.account_id) FROM REQUEST R INNER JOIN OFFERS OFF ON R.offer_id = OFF.offer_id WHERE OFF.account_id = %s AND R.request_status=0",[a_id])
    n_requests = cur.fetchall() #returns a list of tuples
    cur.close()
    return n_requests
def cancel_request(mysql,args):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE REQUEST SET request_status = -1 WHERE account_id = %s AND offer_id = %s;",(args[1],args[0]))
    cur.close()
    mysql.connection.commit()
    
def accept_request(mysql,args):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE REQUEST SET request_status = 1 WHERE account_id = %s AND offer_id = %s;",(args[1],args[0]))
    cur.execute("UPDATE REQUEST SET request_status = -1 WHERE account_id <> %s AND offer_id = %s;",(args[1],args[0]))
    cur.close()
    mysql.connection.commit()

def generate_index(mysql,a_id):
    cur = mysql.connection.cursor()
    result_args = cur.callproc('get_followed_offers', [a_id])
    followed = cur.fetchall()
    cur.close()
    mysql.connection.commit()
    
    cur = mysql.connection.cursor()
    result_args = cur.callproc('get_favorite_types', [a_id])
    favorite = cur.fetchall()
    cur.close()
    mysql.connection.commit()

    cur = mysql.connection.cursor()
    result_args = cur.callproc('get_offers')
    rest_offers = cur.fetchall()
    cur.close()
    mysql.connection.commit()
    rest_offers = tuple( set(rest_offers)- set(followed+favorite))
    rest_offers = tuple(sorted(rest_offers, key=lambda item: item[5], reverse=True))
    return helpers.group_list(followed + favorite + rest_offers, 3)
    
def get_username(mysql, a_id):
    a_id = int(a_id)
    cur = mysql.connection.cursor()
    result_args = cur.execute("SELECT account_username FROM ACCOUNTS WHERE account_id = %s", [a_id])
    account_username = cur.fetchall()
    cur.close()
    mysql.connection.commit()
    return account_username[0][0]

def get_donation(mysql, d_id):
    d_id = int(d_id)
    cur = mysql.connection.cursor()
    result_args = cur.execute("SELECT * FROM OFFERS WHERE offer_id = %s", [d_id])
    offer = cur.fetchone()
    cur.close()
    mysql.connection.commit()
    return offer

def get_type_user(mysql, username):
    cur = mysql.connection.cursor()
    result_args = cur.execute("SELECT account_type FROM ACCOUNTS WHERE account_username = %s", [username])
    user_type = cur.fetchone()
    cur.close()
    mysql.connection.commit()
    return user_type[0]

def get_account_id(mysql, username):
    cur = mysql.connection.cursor()
    result_args = cur.execute("SELECT account_id FROM ACCOUNTS WHERE account_username = %s", [username])
    account_id = cur.fetchone()
    cur.close()
    mysql.connection.commit()
    return account_id[0]

def get_user(mysql, username):
    cur = mysql.connection.cursor()
    user_type = get_type_user(mysql, username)
    account_id = get_account_id(mysql, username)
    if int(user_type) == 1: 
        result_args = cur.execute("SELECT A.account_id, A.account_type, A.account_email, A.account_username, A.account_bio, D.donor_picture, CONCAT(D.donor_first_name, ' ', D.donor_last_name), D.donor_address, D.donor_city, D.donor_phone_number, D.donor_followers FROM ACCOUNTS A INNER JOIN DONORS D WHERE A.account_id = %s and A.account_id = D.account_id", [account_id])
    else:
        result_args = cur.execute("SELECT A.account_id, A.account_type, A.account_email, A.account_username, A.account_bio, O.organization_picture, O.organization_name, O.organization_address, O.organization_city, O.organization_phone_number, O.organization_followers FROM ACCOUNTS A INNER JOIN ORGANIZATIONS O WHERE A.account_id = %s and A.account_id = O.account_id", [account_id])
    user = cur.fetchone() 
    cur.close()
    mysql.connection.commit()
    return user

def get_requests(mysql, a_id):
    cur = mysql.connection.cursor()
    cur.execute(" SELECT ORG.organization_name, ORG.organization_picture, OFF.offer_title, OFF.offer_id, ORG.account_id FROM REQUEST R INNER JOIN ORGANIZATIONS ORG ON R.account_id = ORG.account_id INNER JOIN OFFERS OFF ON R.offer_id = OFF.offer_id WHERE R.request_status = 0 AND OFF.account_id = %s;",[a_id])
    data = cur.fetchall() #returns a list of tuples
    myrequests = [(r[0], r[1], r[2], r[3],r[4]) for r in data]
    cur.close()
    return myrequests
    
def get_number_requests (mysql, a_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(R.account_id) FROM REQUEST R INNER JOIN OFFERS OFF ON R.offer_id = OFF.offer_id WHERE OFF.account_id = %s AND R.request_status=0",[a_id])
    n_requests = cur.fetchall() #returns a list of tuples
    cur.close()
    return n_requests
def get_requests_answer(mysql, args):
    cur = mysql.connection.cursor()
    cur.execute("SELECT OFF.offer_title,A.account_username,  OFF.offer_picture, OFF.offer_id,D.account_id FROM REQUEST R INNER JOIN OFFERS OFF ON OFF.offer_id = R.offer_id INNER JOIN DONORS D ON D.account_id = OFF.account_id INNER JOIN ACCOUNTS A ON A.account_id = D.account_id WHERE R.account_id = %s AND R.request_status = 1;",[args])
    data = cur.fetchall() #returns a list of tuples
    myrequests = [(r[0], r[1], r[2], r[3], r[4]) for r in data]
    cur.close()
    return myrequests

def get_number_answers_requests (mysql, a_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM REQUEST WHERE account_id = %s AND request_status=1;",[a_id])
    n_requests = cur.fetchall() #returns a list of tuples
    cur.close()
    return n_requests

def view_notifications(mysql,user_status,args):
    if user_status == 1: #donor
        myrequests = get_requests(mysql,args)
    else:
        myrequests = get_requests_answer(mysql,args)
    return myrequests

def view_number_notifications(mysql,user_status,args):
    if user_status == 1: #donor
        n_requests = get_number_requests(mysql,args)
    else:
        n_requests = get_number_answers_requests(mysql,args)
    return n_requests
def send_request(mysql, args):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO REQUEST (offer_id, account_id, request_status,request_date) VALUES (%s, %s, 0,'2017-01-11')",(args[1], args[0]))
    n_requests = cur.fetchall() #returns a list of tuples
    cur.close()
    mysql.connection.commit()

def get_donor_donations(mysql, a_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM OFFERS WHERE account_id = %s",[a_id])
    donations = cur.fetchall() #returns a list of tuples
    cur.close()
    mysql.connection.commit()
    return donations

def get_organization_donations(mysql, a_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM OFFERS O INNER JOIN REQUEST R WHERE  R.account_id = %s and O.offer_id = R.offer_id",[a_id])
    donations = cur.fetchall() #returns a list of tuples
    cur.close()
    mysql.connection.commit()
    return donations

def add_comment(mysql, args):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO COMMENTS(comment_text, account_id, offer_id, comment_date) VALUES (%s, %s, %s, NOW())",[args[0], args[1], args[2]])
    cur.close()
    mysql.connection.commit()

def get_comments(mysql, d_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT comment_text, account_id, comment_date FROM COMMENTS WHERE offer_id = %s", [d_id])
    comments = cur.fetchall()
    cur.close()
    mysql.connection.commit()
    return comments


