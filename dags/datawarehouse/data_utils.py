from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2.extras import RealDictCursor # Import RealDictCursor for fetching results as dictionaries

def get_conn_cursor(): # Function to establish a connection and cursor to the PostgreSQL database. 
    hook = PostgresHook(postgres_conn_id='postgres_db_yt_elt', database='elt_db') # Create a PostgresHook using the connection ID and database name
    conn = hook.get_conn() # Get a connection object from the hook
    cur = conn.cursor(cursor_factory=RealDictCursor) # Create a cursor object for executing SQL and fetching rows as dictionaries
    return conn, cur # Return the connection and cursor objects
    
def close_conn_cursor(conn, cur): # Function to close the cursor and connection to the PostgreSQL database.
    cur.close() # Close the cursor to free up resources
    conn.close() # Close the connection to free up resources