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
    tr_no VARCHAR(5) PRIMARY KEY,
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



INSERT INTO train_table (tr_no, tr_name, stoppage, class) VALUES
('12041', 'HWH NJP SHATABDI EXPRESS',
 '["howrah","bolpur","farakka","malda","barsoi","kishanganj","new jalpaiguri"]',
 '["CC"]'),
('12035', 'SDAH NDLS RAJDHANI EXPRESS',
 '["sealdah","durgapur","asansol","dhanbad","gaya","new delhi"]',
 '["AC3","AC2","AC1"]'),
('22387', 'HWH DHN BLACKDIAMOND EXPRESS',
 '["howrah","bandel","barddhaman","durgapur","asansol","dhanbad"]',
 '["CC","2S"]');

INSERT INTO availability_table (tr_no, AC1, AC2, AC3, SL, CC, `2S`) VALUES
('12041', 0, 0, 0, 0, 200, 0),
('12035', 100, 100, 100, 0, 0, 0),
('22387', 0, 0, 0, 0, 200, 200);