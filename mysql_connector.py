def create_donor(mysql, args):
	cur = mysql.connection.cursor()
	result_args = cur.callproc('createDonor', args)
	cur.close()
	mysql.connection.commit()

def login_user(mysql, args):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT account_username, account_password FROM ACCOUNTS WHERE account_username = %s ", [args[0]])
    #if no user with username is found
    if result == 0:
    	cur.close()
    	return False
    data = cur.fetchone()
    password_candidate = args[1]
    password = data[1]
    cur.close()
    #if passwords do not match
    if password_candidate != password:
        return False
    return True