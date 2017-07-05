USE DONATIVA;

INSERT INTO ACCOUNT(account_email,account_username,account_password,account_date,account_bio,account_type) 
		VALUES ('manal.hamdi@aui.ma','noula', 'azerty','2017-07-05','I donate cats','1');
INSERT INTO DONORS (account_id, donor_first_name, donor_last_name, donor_address, donor_city, donor_phone_number)
		VALUES (2, 'Manal', 'Hamdi', '17 appt', 'Rabat', '0688261704')




