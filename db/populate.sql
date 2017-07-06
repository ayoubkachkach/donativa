USE DONATIVA;

INSERT INTO ACCOUNT(account_email,account_username,account_password,account_date,account_bio,account_type) 
		VALUES ('manal.hamdi@aui.ma','noula', 'azerty','2017-07-05','I donate cats','1');
INSERT INTO DONORS (account_id, donor_first_name, donor_last_name, donor_address, donor_city, donor_phone_number)
		VALUES (2, 'Manal', 'Hamdi', '17 appt', 'Rabat', '0688261704')

INSERT INTO ACCOUNT(account_email,account_username,account_password,account_date,account_bio,account_type) 
		VALUES ('manal.hamdi@aui.ma','noula', 'azerty','2017-07-05','I donate cats','1');

INSERT INTO ORGANIZATIONS (account_id, organization_name, organization_address, organization_city, organization_phone_number, organization_certification_code)
		VALUES (3, 'Bayti', '23 rt', 'Rabat', '0566666666', '43-23');
