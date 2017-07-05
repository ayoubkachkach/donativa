
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

