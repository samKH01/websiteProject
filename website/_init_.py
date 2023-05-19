import dbm
import dbus
from flask import Flask
from flask_login import LoginManager
import mysql.connector

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'xyzsdfg'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'SignaNume'

from website import user

login_manager = LoginManager(app)

from website import user, models

# ... rest of your code ...

# Create a cursor object to execute SQL queries
cursor = dbm.cursor()

# Create your database tables using SQL queries
# Modify the queries according to your specific table structures
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(100) NOT NULL
    )
""")
# Create more tables if needed

# Commit the changes to the database
dbus.commit()

# Close the cursor and database connection
cursor.close()
dbus.DBusException.close()