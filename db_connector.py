import mysql.connector
from mysql.connector import Error
import json

def get_connection(isolation_level=None):
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)

        connection = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            port=config["port"]
        )

        if isolation_level:
            connection.set_isolation_level(isolation_level)

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"create database if not exists {config['database']};")
            cursor.execute(f"use {config['database']};")
            return connection
        else:
            print("Failed to connect to database")
            return None
    except Error as e:
        print(f"Error: {e}")
        return None