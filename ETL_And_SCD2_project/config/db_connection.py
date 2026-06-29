import pandas as pd
import pyodbc

def db_connection():
    from sqlalchemy import create_engine

    # Define your server and database
    server = r'LAPTOP-89GPQ3HC\SQLEXPRESS'
    database = 'ETLSCD'

    # Create SQLAlchemy engine
    engine = create_engine(
        f"mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    # Test connection
    with engine.connect() as conn:
        df = pd.read_sql_query('select @@version',conn )
        print(df, "Connection successful!")
db_connection()

    # server=r'LAPTOP-89GPQ3HC\SQLEXPRESS'
    # database='ETLSCD'
    # connection = pyodbc.connect(
    #     f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    #     f'SERVER={server};'
    #     f'DATABASE={database};'
    #     f'Trusted_Connection=yes;'
    # )
    # return connection


#helpful:
#     df = pd.read_sql_query('SELECT * FROM Orders', connection)
#     print(df)
#
# db_connection()