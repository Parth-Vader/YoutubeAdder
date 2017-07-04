import getpass
import sqlite3
import shutil
import os

def Find_path():
	User_profile = getpass.getuser()
	History_path = "/home/"+ User_profile + r"/.config/google-chrome/Default/History" #Usually this is where the chrome history file is located, change it if you need to.
	new = os.getcwd() + "/temp.db"
	#print History_path
	return History_path, new

def Main():
	data_base, new_location = Find_path()
	
	conn = sqlite3.connect(data_base)
	c = conn.cursor()

	try:
		c.execute("SELECT url FROM urls WHERE url LIKE 'https://www.youtube.com/watch?v=%' ORDER BY last_visit_time;")
		all_rows = c.fetchall()
		c.executescript("""ATTACH DATABASE 'test.db' AS other;
                        INSERT INTO other.urls
                        SELECT url 
                        FROM urls
                        WHERE url 
                        LIKE 'https://www.youtube.com/watch?v=%' 
                        ORDER BY last_visit_time;""")
	
	except sqlite3.OperationalError:
		shutil.copyfile(data_base,new_location)
		conn = sqlite3.connect(new_location)
		c = conn.cursor()
		c.execute("SELECT url FROM urls WHERE url LIKE 'https://www.youtube.com/watch?v=%' ORDER BY last_visit_time;")
		all_rows = c.fetchall()
		c.executescript("""ATTACH DATABASE 'test.db' AS other;
                        INSERT INTO other.urls
                        SELECT url 
                        FROM urls
                        WHERE url 
                        LIKE 'https://www.youtube.com/watch?v=%' 
                        ORDER BY last_visit_time;""")

		os.remove("temp.db")

if __name__ == '__main__':
	Main()
