from sqlite3 import Cursor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
from scipy.stats import pearsonr
import sqlalchemy as sa
from sqlalchemy import create_engine
import pyodbc
import os

server = os.getenv('http://unstructured-data-server.database.windows.net')
database = os.getenv('unstructured-data')
username = os.getenv('project-admin')
password = os.getenv('password22$')
port = os.getenv('1433')

connection_string = ('Driver={ODBC Driver 17 for SQL Server};Server=tcp:unstructured-data-server.database.windows.net,1433;Database=unstructured-data;Uid=project-admin;Pwd={password22$};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')

connection = pyodbc.connect(connection_string)

cursor = connection.cursor()

data = pd.read_sql('SELECT * FROM steam_source_data', connection)
print(data)