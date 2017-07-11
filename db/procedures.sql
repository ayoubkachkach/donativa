
USE DONATIVA;
-- ********************************************* CREATE DONOR ***********************************
-- Donor picture needs to be handled
DROP PROCEDURE IF EXISTS createDonor;
DELIMITER #
CREATE PROCEDURE createDonor(
    IN a_email VARCHAR(30),
    IN a_username VARCHAR(15),
    IN a_password VARCHAR(30),
    IN a_bio VARCHAR(120),
    IN a_type INTEGER,
    IN d_first_name VARCHAR(15),
    IN d_last_name VARCHAR(15),
    IN d_address VARCHAR(30),
    IN d_city VARCHAR(20),
    IN d_phone_number VARCHAR(15)
)
BEGIN
    if ( select exists (select 1 from ACCOUNTS where account_username = a_username 
        OR account_email = a_email) ) THEN
        
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username or Email already exists.';
     
    ELSE
     
        insert into ACCOUNTS
        (
            account_email,
            account_username,
            account_password,
            account_date,
            account_bio,
            account_type
        )
        values
        (
            a_email,
            a_username,
            a_password,
            CURDATE(),
            a_bio,
            a_type
        );
        set @id := (SELECT account_id FROM ACCOUNTS WHERE account_username=a_username);
        insert into DONORS
        (
			account_id,
            donor_first_name,
			donor_last_name,
			donor_address,
			donor_city,
			donor_phone_number
        )
        values
        (
			@id,
            d_first_name,
            d_last_name,
            d_address,
            d_city,
            d_phone_number
        );
     
    END IF;
END#
DELIMITER ;
-- ********************************************* CREATE ORGANIZATION ***********************************
DROP PROCEDURE IF EXISTS createOrganization;
DELIMITER #
CREATE PROCEDURE createOrganization(
    IN a_email VARCHAR(30),
    IN a_username VARCHAR(15),
    IN a_password VARCHAR(30),
    IN a_bio VARCHAR(120),
    IN a_type INTEGER,
    IN o_name VARCHAR(80),
    IN o_address VARCHAR(30),
    IN o_city VARCHAR(20),
    IN o_phone_number VARCHAR(15),
    IN o_certification_code VARCHAR(20)
)
BEGIN
    if  ( select exists (select 1 from ACCOUNTS where account_username = a_username 
        OR account_email = a_email) ) THEN
        
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username or Email already exists.';
     
    ELSE
        insert into ACCOUNTS
        (
            account_email,
            account_username,
            account_password,
            account_date,
            account_bio,
            account_type
        )
        values
        (
            a_email,
            a_username,
            a_password,
            CURDATE(),
            a_bio,
            a_type
        );
        set @id := (SELECT account_id FROM ACCOUNTS WHERE account_username=a_username);
        insert into ORGANIZATIONS
        (
            account_id,
            organization_name,
            organization_address,
            organization_city,
            organization_phone_number,
            organization_certification_code
        )
        values
        (
            @id,
            o_name,
            o_address,
            o_city,
            o_phone_number,
            o_certification_code
        );
     
    END IF;
END#
DELIMITER ;
-- *************************CREATE OFFER**********************************************--
USE DONATIVA;
DROP PROCEDURE IF EXISTS createOffer;
DELIMITER #
CREATE PROCEDURE createOffer(
    IN account_id INTEGER,
    IN o_title VARCHAR(80),
    IN o_description VARCHAR(120),
    IN o_city VARCHAR(40),
    IN o_type INTEGER,
    IN o_date DATE,
    IN o_address VARCHAR(80),
    IN o_picture VARCHAR(60)
)
BEGIN
		
		if(o_picture <> 'none.jpg') THEN
        insert into OFFERS
        (
            account_id,
            offer_title,
            offer_description,            
            offer_city,
            offer_type_id,
            offer_expiration_date,
            offer_address,
            offer_date
        )
        values
        (
			account_id,
			o_title,
			o_description,
			o_city,
			o_type,
			o_date,
			o_address,
            NOW()
        );
        set @last_id := (SELECT MAX(offer_id) from OFFERS);
        UPDATE OFFERS
        SET offer_picture = CONCAT(@last_id, '.jpg');
        ELSE
        insert into OFFERS
        (
            account_id,
            offer_title,
            offer_description,            
            offer_city,
            offer_type_id,
            offer_expiration_date,
            offer_address,
            offer_picture,
            offer_date
        )
        values
        (
			account_id,
			o_title,
			o_description,
			o_city,
			o_type,
			o_date,
			o_address,
			'none.jpg',
            NOW()
        );
        END IF;
		SELECT @last_id;
END#
DELIMITER ;
-- ********************************************* GET OFFERS FOR INDEX ***********************************
USE DONATIVA;
DROP PROCEDURE IF EXISTS get_followed_offers;
DELIMITER $$

CREATE PROCEDURE get_followed_offers (IN a_id INTEGER)
BEGIN
	SELECT * FROM OFFERS
	WHERE account_id = (SELECT followed_account_id FROM ACCOUNT_FOLLOWS
    WHERE follower_account_id = a_id) ORDER BY offer_date DESC;
END $$
DELIMITER ;

-- ********************************************* GET OFFERS FROM FAVORITE TYPE ***********************************

USE DONATIVA;
DROP PROCEDURE IF EXISTS get_favorite_types;
DELIMITER $$

CREATE PROCEDURE get_favorite_types (IN a_id INTEGER)
BEGIN
	SELECT 
    *
FROM
    OFFERS
WHERE
    offer_type_id = (SELECT 
            type_id
        FROM
            ACCOUNT_FAVORITE_TYPES
        WHERE
            account_id = a_id) ORDER BY offer_date DESC;
END $$
DELIMITER ;

-- ********************************************* GET OFFERS EXCEPT FAVORITE TYPE ***********************************

USE DONATIVA;
DROP PROCEDURE IF EXISTS get_offers;
DELIMITER $$

CREATE PROCEDURE get_offers ()
BEGIN
	SELECT * FROM OFFERS;
END $$
DELIMITER ;
