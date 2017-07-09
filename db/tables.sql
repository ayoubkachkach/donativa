DROP DATABASE DONATIVA;
CREATE DATABASE DONATIVA;
USE DONATIVA;

CREATE TABLE ACCOUNTS (
    account_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    account_email VARCHAR(30) NOT NULL UNIQUE,
    account_username VARCHAR(15) NOT NULL UNIQUE,
    account_password VARCHAR(30) NOT NULL,
    account_date DATE NOT NULL,
    account_bio VARCHAR(120),
    account_type INT NOT NULL
);

CREATE TABLE ACCOUNT_FOLLOWS (
    follower_account_id INTEGER,
    followed_account_id INTEGER,
    PRIMARY KEY (follower_account_id , followed_account_id),
    FOREIGN KEY (follower_account_id)
        REFERENCES ACCOUNTS (account_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (followed_account_id)
        REFERENCES ACCOUNTS (account_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    followed_date DATE
);

CREATE TABLE OFFER_TYPES (
    type_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(30)
);


CREATE TABLE ACCOUNT_FAVORITE_TYPES (
    account_id INTEGER,
    type_id INTEGER,
    PRIMARY KEY (account_id , type_id),
    FOREIGN KEY (account_id)
        REFERENCES ACCOUNTS (account_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (type_id)
        REFERENCES OFFER_TYPES (type_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE DONORS (
    account_id INTEGER PRIMARY KEY,
    FOREIGN KEY (account_id)
        REFERENCES ACCOUNTS (account_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    donor_picture VARCHAR(60) DEFAULT 'none',
    donor_first_name VARCHAR(15) NOT NULL,
    donor_last_name VARCHAR(15) NOT NULL,
    donor_address VARCHAR(30) NOT NULL,
    donor_city VARCHAR(20),
    donor_phone_number VARCHAR(15) NOT NULL,
    donor_likes INT DEFAULT 0,
    donor_followers INT DEFAULT 0
);

CREATE TABLE ORGANIZATIONS (
    account_id INTEGER PRIMARY KEY,
    FOREIGN KEY (account_id)
        REFERENCES ACCOUNTS (account_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    organization_picture VARCHAR(60) DEFAULT 'none',
    organization_name VARCHAR(80) NOT NULL,
    organization_address VARCHAR(30) NOT NULL,
    organization_city VARCHAR(20) NOT NULL,
    organization_phone_number VARCHAR(15) NOT NULL,
    organization_certification_code VARCHAR(20) NOT NULL,
    organization_likes INT DEFAULT 0,
    organization_followers INT DEFAULT 0
);



CREATE TABLE OFFERS (
    offer_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    account_id INTEGER NOT NULL,
    FOREIGN KEY (account_id)
        REFERENCES DONORS (account_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    offer_picture VARCHAR(60) DEFAULT 'none',
    offer_title VARCHAR(80) NOT NULL,
    offer_description VARCHAR(120) NOT NULL,
    offer_date DATETIME NOT NULL,
    offer_city VARCHAR(40) NOT NULL,
    offer_status INT DEFAULT 0,
    offer_type_id INTEGER,
    FOREIGN KEY (offer_type_id)
        REFERENCES OFFER_TYPES (type_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    offer_expiration_date DATE
);

CREATE TABLE DONATIONS_ARCHIVE (
    donation_id INTEGER PRIMARY KEY,
    donation_picture VARCHAR(60) DEFAULT 'none',
    donation_title VARCHAR(80) NOT NULL,
    donation_description VARCHAR(120) NOT NULL,
    donation_city VARCHAR(40) NOT NULL,
    donation_date DATETIME NOT NULL,
    donation_type_id INTEGER,
    donation_expiration_date DATE,
    FOREIGN KEY (donation_type_id)
        REFERENCES OFFER_TYPES (type_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    account_id INTEGER NOT NULL,
    FOREIGN KEY (account_id)
        REFERENCES DONORS (account_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS REQUEST;
CREATE TABLE REQUEST (
    account_id INTEGER,
    FOREIGN KEY (account_id)
        REFERENCES ORGANIZATIONS (account_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    offer_id INTEGER NOT NULL,
    FOREIGN KEY (offer_id)
        REFERENCES OFFERS (offer_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (offer_id , account_id),
    request_status INTEGER DEFAULT 0,
    request_date DATETIME
);



CREATE TABLE COMMENTS (
    comment_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    comment_text VARCHAR(120),
    account_id INTEGER,
    offer_id INTEGER,
    FOREIGN KEY (offer_id)
        REFERENCES OFFERS (offer_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    comment_date DATETIME,
    FOREIGN KEY (account_id)
        REFERENCES ACCOUNTS (account_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

SELECT 
    *
FROM
    ACCOUNTS;
CREATE EVENT remove_expired_offers
  ON SCHEDULE
    EVERY 1 DAY
    STARTS '2017-06-30 00:20:00' ON COMPLETION PRESERVE ENABLE 
  DO
      DELETE FROM OFFERS
      WHERE offer_expiration_date <= CURDATE();
      
      
DELIMITER $$