import os

DATABASE = {
    'drivername': 'mysql',
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT'],
    'username': os.environ['DB_USERNAME'],
    'password': os.environ['DB_PASSWORD'],
    'database': os.environ['DB_DATABASE'],
}
