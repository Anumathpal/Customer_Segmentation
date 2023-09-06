import psycopg2
import pandas as pd


def connect_to_redshift(dbname, host, port, user, password):
    """Method that connects to redshift. This gives a warning so will look for another solution"""

    connect = psycopg2.connect(
        dbname=dbname, host=host, port=port, user=user, password=password
    )

    print("connection to redshift made")

    return connect


def extract_transactional_data(dbname, host, port, user, password):
    """
   
    """


    # connect to redshift
    connect = connect_to_redshift(dbname, host, port, user, password)

    # read the sql query which does the following

    query = """
    SELECT *
    FROM bootcamp.online_transactions_cleaned
    """
    online_trans_cleaned = pd.read_sql(query, connect)

    print(f"The shape of the extracted and transformed data is {online_trans_cleaned.shape}")

    return online_trans_cleaned