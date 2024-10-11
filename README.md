For demo how will the file will be ruuning
Step 1: Run the bank_interface file every information you give to it will stored in postgre
Step 2: Open SQL:(follow the instruction below)
Server [localhost]:
Database [postgres]:
Port [5432]:
Username [postgres]:
psql (17.0)

postgres=# \c bank_system
You are now connected to database "bank_system" as user "postgres".
bank_system=# \c SELECT * FROM customers;
invalid integer value "customers" for connection option "port"
Previous connection kept
bank_system=# \d
                      List of relations
 Schema |             Name              |   Type   |  Owner
--------+-------------------------------+----------+----------
 public | accounts                      | table    | postgres
 public | accounts_accounts_numbers_seq | sequence | postgres
 public | customers                     | table    | postgres
 public | customers_id_seq              | sequence | postgres
(4 rows)


bank_system=# SELECT * FROM accounts;
 account_number | holder_name | balance | account_type | username | password | pin
----------------+-------------+---------+--------------+----------+----------+------
              1 | Manoj       | 3083.00 | savings      | manoj12  | 12345678 | 0000
              2 | Yash        | 9000.00 | savings      | Yash@12  | 12345678 | 0000
(2 rows)

Step 3 : Now for Running the main.py(run the file and every information will stored in the database)


#Create a Table for transactions where all the transctions will be saved 

bank_system=# CREATE TABLE transactions (
bank_system(# transaction_id SERIAL PRIMARY KEY,
bank_system(# account_number INT NOT NULL,
bank_system(# transaction_type VARCHAR(50) NOT NULL,
bank_system(# transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
bank_system(# );
CREATE TABLE


bank_system=# \d ---------------------------(To see all the Tables)



                       List of relations
 Schema |              Name               |   Type   |  Owner
--------+---------------------------------+----------+----------
 public | accounts                        | table    | postgres
 public | accounts_accounts_numbers_seq   | sequence | postgres
 public | customers                       | table    | postgres
 public | customers_id_seq                | sequence | postgres
 public | transactions                    | table    | postgres
 public | transactions_transaction_id_seq | sequence | postgres
(6 rows)


bank_system=# ALTER TABLE transactions ADD COLUMN amount DECIMAL(10,2);----------------------------added a column

ALTER TABLE

bank_system=# SELECT * FROM transactions; --------------------------------(to select transaction)


 transaction_id | account_number | transaction_type |      transaction_date      | amount
----------------+----------------+------------------+----------------------------+---------
              1 |              3 | deposit          | 2024-10-11 12:32:27.388628 | 2345.00
              2 |              3 | withdraw         | 2024-10-11 12:32:37.037283 |  345.00
(2 rows)


bank_system-# \d
                       List of relations
 Schema |              Name               |   Type   |  Owner
--------+---------------------------------+----------+----------
 public | accounts                        | table    | postgres
 public | accounts_accounts_numbers_seq   | sequence | postgres
 public | customers                       | table    | postgres
 public | customers_id_seq                | sequence | postgres
 public | transactions                    | table    | postgres
 public | transactions_transaction_id_seq | sequence | postgres
(6 rows)


bank_system-# SELECT * FROM accounts;

        ^
bank_system=# SELECT * FROM accounts;
 account_number | holder_name | balance  | account_type | username | password | pin
----------------+-------------+----------+--------------+----------+----------+------
              1 | Manoj       |  3083.00 | savings      | manoj12  | 12345678 | 0000
              2 | Yash        |  9000.00 | savings      | Yash@12  | 12345678 | 0000
              3 | mubashir    | 12500.00 | savings      | mubbu@31 | 1010     | 1010
(3 rows)


bank_system=# SELECT * FROM customers;
 id |  name  | account_number | password  | pin
----+--------+----------------+-----------+------
  1 | Yash   | 101            | 123456789 | 1234
  2 | Omkar  | 102            | 12345678  | 1234
  4 | Jayesh | 104            | 00000000  | 6787
  5 | Akhil  | 202            | 123456789 | 0000
  6 | Manoj  | 234            | 00909090  | 6789
(5 rows)


bank_system=# SELECT * FROM accounts;

 account_number | holder_name | balance  | account_type | username | password | pin
----------------+-------------+----------+--------------+----------+----------+------
              1 | Manoj       |  3083.00 | savings      | manoj12  | 12345678 | 0000
              2 | Yash        |  9000.00 | savings      | Yash@12  | 12345678 | 0000
              3 | mubashir    | 12500.00 | savings      | mubbu@31 | 1010     | 1010
(3 rows)


bank_system=# SELECT * FROM transactions;

 transaction_id | account_number | transaction_type |      transaction_date      | amount
----------------+----------------+------------------+----------------------------+---------
              1 |              3 | deposit          | 2024-10-11 12:32:27.388628 | 2345.00
              2 |              3 | withdraw         | 2024-10-11 12:32:37.037283 |  345.00