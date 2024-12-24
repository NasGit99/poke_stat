import uuid
import pandas as pd
import numpy as np
import requests
#from pokemon_stat import *
import sqlite3 
from sqlalchemy import create_engine
from datetime import datetime
import json
import * from poke_functions
# from airflow import DAG
# from airflow.operators.python import PythonOperator

# # #Goal is to import all pokemon data and write it to a database
# # #Future iterations will allow you to select 6 pokemon and randomize the moves for them.

# default_args = {
#      'owner': 'airpoke',
#      'start_date': datetime(2024, 6, 18, 8, 00)
#      }

# # #entrypoint for dag


def stream_data():
    from kafka import KafkaProducer
    data = insert_into_dex()
    #defining the kafka producer
    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=10000)
    #pushing the data to the topic
    producer.send('poke_data', json.dumps(data).encode('utf-8'))
    

    # except Exception as e:
    #     logging.error(f'An error occurred: {e}')
    #     continue

# connection = sqlite3.connect('POKEDATA.db')
# engine = create_engine("sqlite:///POKEDATA.db", echo = False)




# file = "POKEDATA"
# try: 
#   conn = sqlite3.connect(file) 
#   print("Database formed.") 
# except: 
#   print("Database not formed.")

# with DAG('poke_automation',
#         default_args=default_args,
#         schedule_interval='@daily',
#         catchup=False) as dag:
    
#     kafka_stream_task = PythonOperator(
#         task_id ='stream_data_from_api',
#         python_callable=stream_data
#     )





