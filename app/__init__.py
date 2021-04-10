import os
import sqlalchemy
from yaml import load, Loader
from flask import Flask

app = Flask(__name__)

def init_engine():
    if os.environ.get('GAE_ENV') != 'standard':
        variables = load(open('app.yaml'), loader=Loader)
        env_vars = variables['env_variables']
        for var in env_vars:
            os.environ[var] = env_vars[var]

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername='mysql+pymysql',
            username=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB'),
            host=os.environ.get('MYSQL_HOST')
        )
    )

    return pool
    
db = init_engine()
conn = db.connect()

conn.execute('SELECT * FROM matchHistory')


from app import routes

