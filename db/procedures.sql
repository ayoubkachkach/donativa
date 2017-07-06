
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
-- ********************************************* CREATE DONOR ***********************************
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
