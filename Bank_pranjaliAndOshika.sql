use Bank_Management;
show databases;
-- BANK Table

CREATE TABLE BANK (
    CODE INT PRIMARY KEY,
    BANK_NAME VARCHAR(50),
    CITY VARCHAR(50),
    ADDRESS VARCHAR(100)
);

-- BRANCH Table
CREATE TABLE BRANCH (
    BRANCH_CODE INT PRIMARY KEY,
    BRANCH_NAME VARCHAR(50),
    ADDRESS VARCHAR(100),
    BANK_CODE INT,
    FOREIGN KEY (BANK_CODE) REFERENCES BANK(CODE)
);

-- CUSTOMER Table
CREATE TABLE CUSTOMER (
    CUSTOMER_ID INT PRIMARY KEY,
    PASSWORD varchar(225),
    F_NAME VARCHAR(50),
    L_NAME VARCHAR(50),
    MOBILE_NO VARCHAR(15),
    ADDRESS VARCHAR(100)
);

-- ACCOUNT Table
CREATE TABLE ACCOUNT (
    ACCOUNT_NO INT PRIMARY KEY,
    BALANCE DECIMAL(15, 2),
    CUSTOMER_ID INT,
    FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMER(CUSTOMER_ID)
);

-- EMPLOYEE Table
CREATE TABLE EMPLOYEE (
    EMP_ID INT PRIMARY KEY,
    EMP_NAME VARCHAR(50),
    MOBILE_NO VARCHAR(15),
    ADDRESS VARCHAR(100)
);

-- LOAN Table
CREATE TABLE LOAN (
    LOAN_NUMBER INT PRIMARY KEY,
    AMOUNT DECIMAL(15, 2),
    CUSTOMER_ID INT,
    FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMER(CUSTOMER_ID)
);

-- PAYMENT Table
CREATE TABLE PAYMENT (
    PAYMENT_NO INT PRIMARY KEY,
    PAYMENT_DATE DATE,
    PAYMENT_AMOUNT DECIMAL(15, 2),
    REFER varchar(40)
);

-- Account Types (for inheritance relationship)
-- SAVING Account Table
CREATE TABLE SAVING (
    ACCOUNT_NO INT PRIMARY KEY,
    FOREIGN KEY (ACCOUNT_NO) REFERENCES ACCOUNT(ACCOUNT_NO)
);

-- CURRENT Account Table
CREATE TABLE CURRENT (
    ACCOUNT_NO INT PRIMARY KEY,
    FOREIGN KEY (ACCOUNT_NO) REFERENCES ACCOUNT(ACCOUNT_NO)
);

-- MANAGE (relationship between EMPLOYEE and ACCOUNT)
CREATE TABLE MANAGE (
    ACCOUNT_NO INT,
    EMP_ID INT,
    PRIMARY KEY (ACCOUNT_NO, EMP_ID),
    FOREIGN KEY (ACCOUNT_NO) REFERENCES ACCOUNT(ACCOUNT_NO),
    FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID)
);

-- AVAIL (relationship between CUSTOMER and LOAN)
CREATE TABLE AVAIL (
    CUSTOMER_ID INT,
    LOAN_NUMBER INT,
    PRIMARY KEY (CUSTOMER_ID, LOAN_NUMBER),
    FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMER(CUSTOMER_ID),
    FOREIGN KEY (LOAN_NUMBER) REFERENCES LOAN(LOAN_NUMBER)
);

-- HAVE (relationship between BANK and BRANCH)
CREATE TABLE HAVE (
    BANK_CODE INT,
    BRANCH_CODE INT,
    PRIMARY KEY (BANK_CODE, BRANCH_CODE),
    FOREIGN KEY (BANK_CODE) REFERENCES BANK(CODE),
    FOREIGN KEY (BRANCH_CODE) REFERENCES BRANCH(BRANCH_CODE)
);

show tables;

-- inserting the values
INSERT INTO BANK (CODE, BANK_NAME, CITY, ADDRESS)
VALUES 
(1, 'ABC Bank', 'New York', '123 Main St, New York, NY 10001'),
(2, 'XYZ Bank', 'Los Angeles', '456 Elm St, Los Angeles, CA 90001');

INSERT INTO CUSTOMER (CUSTOMER_ID, PASSWORD, F_NAME, L_NAME, MOBILE_NO, ADDRESS)
VALUES
(1001, 'password123', 'John', 'Doe', '1234567890', '123 Main St, Springfield, IL'),
(1002, 'securepass456', 'Jane', 'Smith', '0987654321', '456 Oak St, Metropolis, NY'),
(1003, 'mypassword789', 'Alice', 'Johnson', '1122334455', '789 Pine St, Rivertown, TX'),
(1004, 'pass9876', 'Bob', 'Brown', '6677889900', '321 Birch St, Lakeview, FL'),
(1005, 'adminpass123', 'Charlie', 'Davis', '5544332211', '654 Cedar St, Hilltop, CA');

INSERT INTO EMPLOYEE (EMP_ID, EMP_NAME, MOBILE_NO, ADDRESS)
VALUES 
(1, 'John Doe', '1234567890', '123 Elm Street'),
(2, 'Jane Smith', '0987654321', '456 Oak Avenue'),
(3, 'Alice Brown', '1122334455', '789 Pine Road'),
(4, 'Bob White', '2233445566', '321 Maple Lane'),
(5, 'Charlie Green', '3344556677', '654 Cedar Court');

INSERT INTO LOAN (LOAN_NUMBER, AMOUNT, CUSTOMER_ID)
VALUES
(2001, 5000.00, 1001),
(2002, 15000.50, 1003), 
(2003, 2500.75, 1004);  

-- Inserting values into the BRANCH table
INSERT INTO BRANCH (BRANCH_CODE, BRANCH_NAME, ADDRESS, BANK_CODE)
VALUES
(101, 'Central Branch', '101 Main St, New York, NY 10001', 1),
(102, 'Downtown Branch', '202 Elm St, New York, NY 10001', 1),
(201, 'Westside Branch', '303 Sunset Blvd, Los Angeles, CA 90001', 2),
(202, 'North Branch', '404 Ocean Ave, Los Angeles, CA 90001', 2);

-- Inserting values into the ACCOUNT table
INSERT INTO ACCOUNT (ACCOUNT_NO, BALANCE, CUSTOMER_ID)
VALUES
(3001, 1200.50, 1001),
(3002, 3500.75, 1002),
(3003, 800.25, 1003),
(3004, 1500.00, 1004),
(3005, 2300.60, 1005);

-- Inserting values into the PAYMENT table
INSERT INTO PAYMENT (PAYMENT_NO, PAYMENT_DATE, PAYMENT_AMOUNT, REFER)
VALUES
(4001, '2024-01-15', 200.00, 'Loan Payment'),
(4002, '2024-02-18', 500.00, 'Account Deposit'),
(4003, '2024-03-10', 150.75, 'Service Fee'),
(4004, '2024-04-22', 300.00, 'Loan Payment'),
(4005, '2024-05-05', 1000.00, 'Account Deposit');

-- Inserting values into the SAVING account table (Inheritance relationship)
INSERT INTO SAVING (ACCOUNT_NO)
VALUES
(3001),
(3003);

-- Inserting values into the CURRENT account table (Inheritance relationship)
INSERT INTO CURRENT (ACCOUNT_NO)
VALUES
(3002),
(3004),
(3005);

-- Inserting values into the MANAGE table (relationship between EMPLOYEE and ACCOUNT)
INSERT INTO MANAGE (ACCOUNT_NO, EMP_ID)
VALUES
(3001, 1),
(3002, 2),
(3003, 3),
(3004, 4),
(3005, 5);

-- Inserting values into the AVAIL table (relationship between CUSTOMER and LOAN)
INSERT INTO AVAIL (CUSTOMER_ID, LOAN_NUMBER)
VALUES
(1001, 2001),
(1003, 2002),
(1004, 2003);

-- Inserting values into the HAVE table (relationship between BANK and BRANCH)
INSERT INTO HAVE (BANK_CODE, BRANCH_CODE)
VALUES
(1, 101),
(1, 102),
(2, 201),
(2, 202);

ALTER TABLE ACCOUNT
ADD CONSTRAINT account_ibfk_1
FOREIGN KEY (CUSTOMER_ID)
REFERENCES CUSTOMER(CUSTOMER_ID)
ON DELETE CASCADE;
SELECT CONSTRAINT_NAME 
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_NAME = 'ACCOUNT' 
AND TABLE_SCHEMA = 'bank_management';
SELECT CONSTRAINT_NAME, DELETE_RULE
FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS
WHERE TABLE_NAME = 'ACCOUNT'
AND CONSTRAINT_SCHEMA = 'bank_management';

ALTER TABLE current DROP FOREIGN KEY current_ibfk_1;
ALTER TABLE current
ADD CONSTRAINT current_ibfk_1
FOREIGN KEY (ACCOUNT_NO)
REFERENCES account(ACCOUNT_NO)
ON DELETE CASCADE;

ALTER TABLE manage DROP FOREIGN KEY manage_ibfk_1;
ALTER TABLE manage
ADD CONSTRAINT manage_ibfk_1
FOREIGN KEY (ACCOUNT_NO)
REFERENCES account(ACCOUNT_NO)
ON DELETE CASCADE;

ALTER TABLE ACCOUNT DROP FOREIGN KEY fk_customer_account;
SHOW CREATE TABLE ACCOUNT;

ALTER TABLE ACCOUNT 
ADD CONSTRAINT fk_customer_account
FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMER(CUSTOMER_ID)
ON UPDATE CASCADE
ON DELETE CASCADE;

select * from customer;
select * from account;
SELECT 
    TABLE_NAME AS `Table Name`,
    COLUMN_NAME AS `Primary Key Column`
FROM 
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE 
    TABLE_SCHEMA = 'bank_management'
    AND CONSTRAINT_NAME = 'PRIMARY'
ORDER BY TABLE_NAME, COLUMN_NAME;

SELECT 
    TABLE_NAME AS `Table Name`,
    COLUMN_NAME AS `Foreign Key Column`,
    REFERENCED_TABLE_NAME AS `Referenced Table`,
    REFERENCED_COLUMN_NAME AS `Referenced Column`
FROM 
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE 
    TABLE_SCHEMA = 'bank_management'
    AND REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY TABLE_NAME, COLUMN_NAME;


