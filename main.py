# import the libraries needed
import os
import sys
from datetime import datetime
import pandas as pd


from src.extract import extract_transactional_data
from src.RFM_transform import calculate_rfm_metrics

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from dotenv import load_dotenv
load_dotenv()  # only for local testing

# import variables from .env file
dbname = os.getenv("dbname")
host = os.getenv("host")
port = os.getenv("port")
user = os.getenv("user")
password = os.getenv("password")
aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key_id = os.getenv("aws_secret_access_key_id")

# this creates a variable that tracks the time we executed the script
start_time = datetime.now()

# make a connection to redshift and extract transactional data with transformation tasks
print("Extracting and transforming data in sql")
online_trans_cleaned = extract_transactional_data(dbname, host, port, user, password)
rfm_online_transaction = calculate_rfm_metrics(online_trans_cleaned)
print(rfm_online_transaction.head())


# next step, load the new data "customer_segmentation" in local folder
print("Loading data to local folder data")

# customer_segmentation.to_csv("./data/customer_segmentation_data.csv")
# customer_segmentation= pd.read_csv('./data/customer_segmentation_data.csv')


