# db_operations.py

import psycopg2
from psycopg2 import sql
import config_init

def get_db_connection():
    """ Establish and return a connection to the database. """
    try:
        connection = psycopg2.connect(
            host=config_init.DB_HOST,
            database=config_init.DB_NAME,
            user=config_init.DB_USER,
            password=config_init.DB_PASSWORD,
            port=config_init.DB_PORT
        )
        return connection
    except Exception as e:
        print("Error: Unable to connect to the database")
        print(e)
        return None

def save_flight(flight_data):
    """ Save flight data into the database. """
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        
        # Insert flight data into 'flights' table
        insert_flight_query = sql.SQL("""
            INSERT INTO flights (fare_id, departure_airport, destination_airport, departure_date, ticket_timelimit, class, cos)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """)
        
        cursor.execute(insert_flight_query, (
            flight_data['fare_id'], 
            flight_data['departure_airport'], 
            flight_data['destination_airport'],
            flight_data['departure_date'], 
            flight_data['ticket_timelimit'], 
            flight_data['class'], 
            flight_data['cos']
        ))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Error saving flight data: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return False

def save_passenger(passenger_data, flight_fare_id):
    """ Save passenger data into the database. """
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        
        # Insert passenger data into 'passengers' table
        insert_passenger_query = sql.SQL("""
            INSERT INTO passengers (surname, firstname, dob, gender, flight_id)
            VALUES (%s, %s, %s, %s, (SELECT id FROM flights WHERE fare_id = %s LIMIT 1))
        """)
        
        cursor.execute(insert_passenger_query, (
            passenger_data['surname'], 
            passenger_data['firstname'], 
            passenger_data['dob'], 
            passenger_data['gender']
        ))
        
        connection.commit()
        print(f"Passenger {passenger_data['surname']} {passenger_data['firstname']} added successfully.")
        
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Error saving passenger data: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return False
