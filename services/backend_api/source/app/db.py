from flask import g, current_app
import psycopg2

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(host=current_app.config['POSTGRES_HOST'],
                                database=current_app.config['POSTGRES_DB'],
                                user=current_app.config['POSTGRES_USER'])
                                #password=current_app.config['POSTGRES_PASSWORD'])

    return g.db

