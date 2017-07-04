
-- ********************************************* CREATE DONOR ***********************************
-- Donor picture needs to be handled
DELIMITER $$
CREATE PROCEDURE createDonor(
    IN a_email VARCHAR(30),
    IN a_username VARCHAR(15),
    IN a_password VARCHAR(30),
    IN a_bio VARCHAR(120),
    
)
BEGIN
    if ( select exists (select 1 from ACCOUNTS where account_username = a_username 
        OR account_email = a_email) ) THEN
     
        select 'Error. The Username you specified already exists.';
     
    ELSE
     
        insert into ACCOUNTS
        (
            account_email,
            account_username,
            account_password,
            account_date,
            account_bio
        )
        values
        (
            a_email,
            a_username,
            a_password,
            CURDATE(),
            a_bio
        );
     
    END IF;
END$$
DELIMITER ;
-- ********************************************* CREATE DONOR ***********************************
