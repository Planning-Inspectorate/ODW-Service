# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 13:15:31 2023

@author: JonesZofia
"""

from azure.identity import AzureCliCredential
import struct
import pyodbc 

# input params
server = 'pins-prod-pdac-sql.database.windows.net'
database = 'MiPINS-DEV'
query = 'SELECT top (10) * from Live.dim_appeal_combined;'

# Use the cli credential to get a token after the user has signed in via the Azure CLI 'az login' command.
credential = AzureCliCredential()
databaseToken = credential.get_token('https://database.windows.net/')

# get bytes from token obtained
tokenb = bytes(databaseToken[0], "UTF-8")
exptoken = b'';
for i in tokenb:
 exptoken += bytes({i});
 exptoken += bytes(1);
tokenstruct = struct.pack("=i", len(exptoken)) + exptoken;

# build connection string using acquired token
connString = "Driver={ODBC Driver 17 for SQL Server};SERVER="+server+";DATABASE="+database+""
SQL_COPT_SS_ACCESS_TOKEN = 1256 
conn = pyodbc.connect(connString, attrs_before = {SQL_COPT_SS_ACCESS_TOKEN:tokenstruct});

# sample query
cursor = conn.cursor()
cursor.execute(query)
row = cursor.fetchone()
while row:
    print (str(row[0]) + " " + str(row[1]))
    row = cursor.fetchone()