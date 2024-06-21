import logging

from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

#Note to self, can turn off control center and schedule

def create_keyspace(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS spark_streams
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
    """)

    print("keyspace created succesfully")

def create_table(session):
    session.execute("""
    CREATE TABLE IF NOT EXISTS spark_streams.poke_stats(
        id UUID PRIMARY KEY,
        poke_name TEXT,
        type TEXT,
        type_2 TEXT,
        ability TEXT,
        ability_2 TEXT,
        hp INT,
        attack INT,    
        defense INT,               
        special_attack INT,
        special_defense INT,
        speed INT);                   
    """)

    print("Table created sucesfully")

def insert_data(session, **kwargs):

    poke_id = kwargs.get('id'),
    poke_name = kwargs.get('poke_name'),
    type1 = kwargs.get('type'),
    type_2=kwargs.get('type_2'),
    ability=kwargs.get('ability'),
    ability_2=kwargs.get('ability_2'),
    hp=kwargs.get('hp'),
    attack=kwargs.get('attack'),    
    defense=kwargs.get('defense'),               
    special_attack=kwargs.get('spatk'),
    special_defense=kwargs.get('spdf'),
    speed=kwargs.get('spd')

    try:
        session.execute("""
        INSERT INTO spark_streams.poke_stats(uuid,poke_name, type, type_2, ability, ability_2, hp,
        attack, defense, special_attack, special_defense, speed)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)           
        """, (poke_id, poke_name, type1, type_2, ability, ability_2, hp, attack, defense, special_attack, special_defense, speed))

        logging.info(f"Data inserted for {poke_name}")

    except Exception as e:
        logging.error(f"could not insert data due to {e}")

def create_spark_connection():
    s_conn = None
#note to self, the spark version needs to match scala version on
    try:
        s_conn = SparkSession.builder \
            .appName('SparkDataStreaming') \
            .config('spark.jars.packages', "com.datastax.spark:spark-cassandra-connector_2.12:3.4.1,"
                                           "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
            .config('spark.cassandra.connection.host', 'localhost') \
            .getOrCreate()

        s_conn.sparkContext.setLogLevel("ERROR")
        logging.info("Spark connection created successfully!")
    except Exception as e:
        logging.error(f"Couldn't create the spark session due to exception {e}")

    return s_conn

def connect_to_kafka(spark_conn):

    spark_df = None
    try:
        spark_df = spark_conn.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'broker:29092') \
            .option('subscribe', 'poke_data') \
            .option('startingOffsets', 'earliest') \
            .load()
        logging.info("kafka dataframe created successfully")
    except Exception as e:
        logging.warning(f"kafka dataframe could not be created because: {e}")

    return spark_df

def create_cassandra_connection():
    try:
        #connecting to the cassandra cluster
        cluster = Cluster(['localhost'])

        cas_session = cluster.connect()

        return cas_session
    except Exception as e:
        logging.error(f"Could not create cassandra connection due to {e}")
        return None

def create_selection_df_from_kafka(spark_df):
    schema = StructType([
        StructField("poke_id", StringType(), False),
        StructField("poke_name", StringType(), False),
        StructField("type", StringType(), False),
        StructField("type2", StringType(), False),
        StructField("ability", StringType(), False),
        StructField("ability2", StringType(), False),
        StructField("hp", StringType(), False),
        StructField("attack", StringType(), False),
        StructField("defense", StringType(), False),
        StructField("special_attack", StringType(), False),
        StructField("special_defense", StringType(), False),
        StructField("speed", StringType(), False)
    ])

    sel = spark_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col('value'), schema).alias('data')).select("data.*")
    print(sel)

    return sel

if __name__ == "__main__":
 # create spark connection
    spark_conn = create_spark_connection()

    if spark_conn is not None:
        # connect to kafka with spark connection
        spark_df = connect_to_kafka(spark_conn)
        selection_df = create_selection_df_from_kafka(spark_df)
        session = create_cassandra_connection()

        if session is not None:
            create_keyspace(session)
            create_table(session)

            logging.info("Streaming is being started...")

            streaming_query = (selection_df.writeStream.format("org.apache.spark.sql.cassandra")
                               .option('checkpointLocation', '/tmp/checkpoint')
                               .option('keyspace', 'spark_streams')
                               .option('table', 'poke_stats')
                               .start())

            streaming_query.awaitTermination()