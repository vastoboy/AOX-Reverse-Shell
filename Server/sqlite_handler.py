import json
import sqlite3
from prettytable import from_db_cursor


class SqlHandler:
	def __init__(self, database_name, database_table_name):
		self.database_name = "ClientDB.db"
		self.database_table_name = "clientDetails"



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
		# Connect to the database
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
		    for client_id, conn_obj in client_conn_dict.items():
		        try:
		            conn_obj.send("conn check".encode())
		        except:
		            del self.client_conn_dict[client_id]
		    # SELECT query to retrieve all client information from the database
		    cursor.execute(f"SELECT * FROM {self.database_table_name}")
		    connected_client = from_db_cursor(cursor)  # Insert retrieved client information into a table
		    print(connected_client)



	def get_mac_address(self, client_id):
	    with sqlite3.connect(self.database_name) as client_database_conn:
	        cursor = client_database_conn.cursor()
	        # SELECT query to retrieve the MAC address using the primary key
	        cursor.execute(f"SELECT Mac_Address FROM {self.database_table_name} WHERE Client_ID = ?", (client_id,))
	        mac_address = cursor.fetchone()
	        return mac_address[0] if mac_address else None



