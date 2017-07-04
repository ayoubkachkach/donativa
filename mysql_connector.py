def create_donor(mysql, args):
	cur = mysql.connection.cursor()
	result_args = cur.callproc('createDonor', args)
	mysql.connection.commit()
	cur.close()