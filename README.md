Run the bank_interface file as the data will be stored in the Postgresql give th host and username 
the given data will be stored oin this format and below are given some commands
bank_system=# \c bank_system
You are now connected to database "bank_system" as user "postgres".
bank_system=# \dt
           List of relations
 Schema |   Name    | Type  |  Owner
--------+-----------+-------+----------
 public | customers | table | postgres
(1 row)


bank_system=# SELECT * FROM customers;
 id | name  | account_number | password  | pin
----+-------+----------------+-----------+------
  1 | Yash  | 101            | 123456789 | 1234
  2 | Omkar | 102            | 12345678  | 1234
(2 rows)


bank_system=# SELECT * FROM customers;
 id |  name  | account_number | password  | pin
----+--------+----------------+-----------+------
  1 | Yash   | 101            | 123456789 | 1234
  2 | Omkar  | 102            | 12345678  | 1234
  4 | Jayesh | 104            | 00000000  | 6787
(3 rows)


bank_system=# \dt
           List of relations
 Schema |   Name    | Type  |  Owner
--------+-----------+-------+----------
 public | customers | table | postgres
(1 row)


bank_system=# SELECT * FROM customers;
 id |  name  | account_number | password  | pin
----+--------+----------------+-----------+------
  1 | Yash   | 101            | 123456789 | 1234
  2 | Omkar  | 102            | 12345678  | 1234
  4 | Jayesh | 104            | 00000000  | 6787
  5 | Akhil  | 202            | 123456789 | 0000
(4 rows)