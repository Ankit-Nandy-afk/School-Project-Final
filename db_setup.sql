DROP DATABASE IF EXISTS train;
CREATE DATABASE train;
USE train;

CREATE TABLE train_table (
    tr_no VARCHAR(5) PRIMARY KEY,
    tr_name VARCHAR(60) NOT NULL,
    stoppage JSON NOT NULL,
    class JSON NOT NULL
);

CREATE TABLE availability_table (
    tr_no VARCHAR(5) NOT NULL,
    AC1 INT DEFAULT 0,
    AC2 INT DEFAULT 0,
    AC3 INT DEFAULT 0,
    SL INT DEFAULT 0,
    CC INT DEFAULT 0,
    `2S` INT DEFAULT 0,
    FOREIGN KEY (tr_no) REFERENCES train_table(tr_no)
);

CREATE TABLE customer_table (
    pnr INT AUTO_INCREMENT PRIMARY KEY,
    tr_no VARCHAR(5) NOT NULL,
    customer_name VARCHAR(60) NOT NULL,
    customer_phone VARCHAR(15),
    customer_address VARCHAR(150),
    boarding_station VARCHAR(60) NOT NULL,
    destination_station VARCHAR(60) NOT NULL,
    tr_class VARCHAR(10) NOT NULL,
    no_seats INT NOT NULL,
    price INT NOT NULL,
    status VARCHAR(10) NOT NULL,
    FOREIGN KEY (tr_no) REFERENCES train_table(tr_no)
);

ALTER TABLE customer_table AUTO_INCREMENT = 10000001;
