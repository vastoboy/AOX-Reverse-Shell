# Created by Vasto Boy

# Disclaimer: This reverse shell should only be used in the lawful, remote administration of authorized systems. Accessing a computer network without authorization or permission is illegal.


import json
import sqlite3
from prettytable import from_db_cursor


class SqlHandler:
	def __init__(self, database_name, database_table_name):
		self.database_name = database_name
		self.database_table_name = database_table_name



	# creates database where connected client info will be stored
	def create_database(self):
		with sqlite3.connect(self.database_name) as client_database_conn:
		    cursor = client_database_conn.cursor()
		    # Create the table if it does not exist
		    cursor.execute("""CREATE TABLE IF NOT EXISTS {}(
		                        Client_ID INTEGER PRIMARY KEY NOT NULL,
		                        Date_Joined DATETIME DEFAULT CURRENT_TIMESTAMP,
		                        IP_Address TEXT NULL,
		                        Mac_Address TEXT NULL,
		                        System TEXT NULL,
		                        Node_Name TEXT NULL,
		                        Release TEXT NULL,
		                        Version TEXT NULL,
		                        Processor TEXT NULL
		                        );
		                        """.format(self.database_table_name)
		                    )
		    # Delete whatever is in the table if it already exists
		    cursor.execute(f'DELETE FROM {self.database_table_name};')
		    client_database_conn.commit()
		return client_database_conn



	def store_client_info(self, ip, conn, client_info):
		with sqlite3.connect(self.database_name) as client_database_conn:
		    cursor = client_database_conn.cursor()	    
		    # Insert client info into the database
		    client_info = tuple(client_info.values())
		    cursor.execute(f"INSERT INTO {self.database_table_name}(IP_Address, Mac_Address, System, Node_Name, Release, Version, Processor) VALUES(?, ?, ?, ?, ?, ?, ?)", (ip, *client_info))
		    client_database_conn.commit()



	# retrive and display all client information in the database
	def get_connected_client_info(self, client_conn_dict):
	    with sqlite3.connect(self.database_name) as client_database_conn:
	        cursor = client_database_conn.cursor()
	        # Check if clients listed in the database are still connected to the server
	        clients_to_remove = []
	        for mac_address, conn in client_conn_dict.items():
	            try:
	                conn.send("conn check".encode())
	            except:
	                clients_to_remove.append(mac_address)
	        # Remove disconnected clients from the dictionary and database
	        for mac_address in clients_to_remove:
	            client_conn_dict.pop(mac_address)
	            cursor.execute(f"DELETE FROM {self.database_table_name} WHERE Mac_Address=?", (mac_address,))

	        # Retrieve all client information from the database
	        cursor.execute(f"SELECT * FROM {self.database_table_name}")
	        connected_clients = from_db_cursor(cursor)  
	        print(connected_clients)



	def get_mac_address(self, client_id):
	    with sqlite3.connect(self.database_name) as client_database_conn:
	        cursor = client_database_conn.cursor()
	        # SELECT query to retrieve the MAC address using the primary key
	        cursor.execute(f"SELECT Mac_Address FROM {self.database_table_name} WHERE Client_ID = ?", (client_id,))
	        mac_address = cursor.fetchone()
	        return mac_address[0] if mac_address else None



	def remove_client_by_mac(self, mac_address):
		with sqlite3.connect(self.database_name) as client_database_conn:
		    cursor = client_database_conn.cursor()
		    # SQL delete statement to remove client with the specified ID
		    cursor.execute(f"DELETE FROM {self.database_table_name} WHERE Mac_Address=?", (mac_address,))
		    client_database_conn.commit()

