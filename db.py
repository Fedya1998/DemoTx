import sqlite3
from sqlite3 import Error

class DB:
	def create_connection(self, path):
	    connection = None
	    try:
	        connection = sqlite3.connect(path, check_same_thread=False)
	        print("Connection to SQLite DB successful")
	    except Error as e:
	        print(f"The error '{e}' occurred")
	
	    return connection
	
	def execute_query(self, query):
	    cursor = self.connection.cursor()
	    try:
	        cursor.execute(query)
	        self.connection.commit()
	        print("Query executed successfully")
	    except Error as e:
	        print(f"The error '{e}' occurred")
	
	def execute_read_query(self, query):
		cursor = self.connection.cursor()
		result = None
		try:
		    cursor.execute(query)
		    result = cursor.fetchall()
		    return result
		except Error as e:
		    print(f"The error '{e}' occurred")
	
	def view_users(self):
		select_users = "SELECT * from users"
		users = self.execute_read_query(select_users)
		
		for user in users:
		    print(user)

	def __init__(self, path):
		self.connection = self.create_connection(path)
		create_users_table = """
		CREATE TABLE IF NOT EXISTS users (
		  tgid INTEGER PRIMARY KEY,
		  step INTEGER,
		  source_ch TEXT,
		  dest_ch TEXT,
		  value DOUBLE,
		  source_ad TEXT,
		  dest_ad TEXT,
		  source_tx TEXT,
		  dest_tx TEXT,
		  val1 INTEGER,
		  val2 INTEGER,
		  val3 INTEGER
		);
		"""
	
		self.execute_query(create_users_table)


	def update_field(self, tgid, field, value):
		if isinstance(value, str):
			query = f'UPDATE users SET {field}="{value}" WHERE tgid={tgid}'
		else:
			query = f'UPDATE users SET {field}={value} WHERE tgid={tgid}'
		print(query)
		return self.execute_query(query)


	def update_user(self, tgid, step, alpha, beta, value, source_ad, dest_ad, source_tx, dest_tx, val1, val2, val3):
		query = f'REPLACE INTO users (tgid, step, source_ch, dest_ch, value, source_ad, dest_ad, source_tx, dest_tx, val1, val2, val3) VALUES({tgid}, {step}, "{alpha}", "{beta}", {value}, "{source_ad}", "{dest_ad}", "{source_tx}", "{dest_tx}", {val1}, {val2}, {val3})'
		print(query)
		return self.execute_query(query)
	
	def get_user(self, tgid):
		select_users = f"SELECT * from users WHERE tgid={tgid}"
		users = self.execute_read_query(select_users)
		return users[0]


