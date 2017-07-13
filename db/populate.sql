USE DONATIVA;

INSERT INTO ACCOUNTS(account_email, account_username, account_password, account_date, account_bio, account_type) 
		VALUES ('manal.hamdi@aui.ma','noula', 'demo','2017-07-05','I donate cats',1);
        
INSERT INTO DONORS (account_id, donor_first_name, donor_last_name, donor_address, donor_city, donor_phone_number)
		VALUES (1, 'Manal', 'Hamdi', '17 appt', 'Rabat', '0688261704');

INSERT INTO ACCOUNTS(account_email,account_username,account_password,account_date,account_bio,account_type) 
		VALUES ('ayoub.kachkach@aui.ma','theayoubkach', 'demo','2017-07-06','I donate cats to Manal',1);
INSERT INTO DONORS (account_id, donor_first_name, donor_last_name, donor_address, donor_city, donor_phone_number)
		VALUES (2, 'Ayoub', 'Kachkach', '23 appt', 'Mohammadia', '0688261704');

INSERT INTO ACCOUNTS(account_email,account_username,account_password,account_date,account_bio,account_type) 
		VALUES ('bayti@gmail.com','bayti', 'demo','2017-07-07','I operate for the sake of kids',2);
        
INSERT INTO ORGANIZATIONS (account_id, organization_name, organization_address, organization_city, organization_phone_number, organization_certification_code)
		VALUES (3, 'bayti', '23 rt', 'Rabat', '0566666666', '43-23');
        
INSERT INTO ACCOUNTS(account_email,account_username,account_password,account_date,account_bio,account_type) 
		VALUES ('unicef@gmail.com','uniced', 'demo','2017-07-02','We operate for the sake of kids',2);
        
INSERT INTO ORGANIZATIONS (account_id, organization_name, organization_address, organization_city, organization_phone_number, organization_certification_code)
		VALUES (4, 'unicef', '23 tt', 'FES', '0566666666', '43-25');

INSERT INTO OFFERS (account_id, offer_title, offer_description, offer_date, offer_city, offer_status, offer_type_id, offer_expiration_date)
		VALUES(1, 'Cats to give', 'Just take them','2017-12-06', 'Rabat', 0, 2, '2017-02-01');

INSERT INTO REQUEST (account_id, offer_id, request_status, request_date) 
		VALUES (2, 1, 0, '2017-12-09 04:21:32');
        
INSERT INTO OFFERS (account_id, offer_title, offer_description, offer_date, offer_city, offer_status, offer_type_id, offer_expiration_date)
		VALUES(1, 'Ayoub to give', 'Just take him','2017-12-06', 'Anywhere', 0, 2, '2017-02-01');

INSERT INTO REQUEST (account_id, offer_id, request_status, request_date) 
		VALUES (2, 2, 0, '2017-12-09 04:21:32');
                
COMMIT;
SELECT A.account_username, A.account_id FROM ACCOUNT_FOLLOWS AF INNER JOIN ACCOUNTS A ON AF.follower_account_id = A.account_id WHERE AF.followed_account_id = '';

INSERT INTO ACCOUNT_FOLLOWS (follower_account_id, followed_account_id,followed_date)VALUES ('', '', '2017-01-23');

DELETE FROM ACCOUNT_FOLLOWS WHERE follower_account_id > 0;
DELETE FROM ORGANIZATIONS WHERE account_id > 0;
DELETE FROM DONORS WHERE account_id > 0;
DELETE  FROM OFFERS WHERE offer_id > 0;
DELETE  FROM REQUEST WHERE account_id > 0;


DELETE FROM ACCOUNT_FOLLOWS WHERE follower_account_id = '' and followed_account_id ='';

SELECT * FROM ACCOUNT_FOLLOWS;
SELECT * FROM ACCOUNTS;


SELECT A.account_username FROM ACCOUNT_FOLLOWS AF INNER JOIN ACCOUNTS A ON A.account_id = AF.followed_account_id WHERE follower_account_id = '';



ALTER TABLE ACCOUNTS AUTO_INCREMENT=100;
SELECT ORG.organization_name, ORG.organization_picture, OFF.offer_title FROM REQUEST R INNER JOIN ORGANIZATIONS ORG ON R.account_id = ORG.account_id INNER JOIN OFFERS OFF ON R.offer_id = OFF.offer_id WHERE R.request_status = 0 AND OFF.account_id = 1;

SELECT COUNT(R.account_id) 
FROM REQUEST R INNER JOIN OFFERS OFF
ON R.offer_id = OFF.offer_id
WHERE OFF.account_id = 1;


DELETE FROM OFFER_TYPES 
WHERE
    type_id >= 0;
INSERT INTO OFFER_TYPES(type_name) VALUES('Clothing');
INSERT INTO OFFER_TYPES(type_name) VALUES('Food');
INSERT INTO OFFER_TYPES(type_name) VALUES('Entertainment');
INSERT INTO OFFER_TYPES(type_name) VALUES('Education');
INSERT INTO OFFER_TYPES(type_name) VALUES('Misc.');
SELECT * FROM OFFER_TYPES;