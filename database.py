import pymysql
import sys
import boto3
import os

ENDPOINT=""
PORT=3306
USER="dipadmin_sa"
REGION="us-east-1b"
DBNAME="metadata"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
PASSWORD="yi7g*dZa.3FHP6*"


def db_connection():
    try:
        conn = pymysql.connect(host=ENDPOINT, user=USER, passwd=PASSWORD, port=PORT, database=DBNAME)
        cur = conn.cursor()
        return cur
    except Exception as e:
        return "Database connection failed due to {}".format(e)


"""
        Functions get_customer_details and get_region_customers
        are temporary until list of OEX customers are given
"""


def get_customer_details():
    oex = ['OEE', 'ORT', 'OEJ', 'OEK', 'OEP', 'OEZ', 'OEZ-TW', 'OEZ', 'OAA']
    return oex
    '''
    cur = db_connection()
    try:
        cur.execute("""SELECT * from metadata.company_details""")
        query_results = cur.fetchall()
        return query_results
    except Exception as e:
        return e
    '''


def get_region_customers():
    customers = ['BOE', 'Bosch_Braga', 'Global_Foundries', 'TMMK_Kentucky', 'Other']
    return customers
    '''
    cur = db_connection()
    where_clause = ''
    if region is not None:
        where_clause = f"WHERE Region='{region}'"
    try:
        cur.execute(f"SELECT Company_Name FROM metadata.company_details {where_clause}")
        query_results = cur.fetchall()
        return query_results
    except Exception as e:
        return e
    '''

'''def get_region_name(key: int):
    cur = db_connection()
    try:
        cur.execute(f"SELECT Region FROM metadata.company_details WHERE Company_Key={key}")
        query_results = cur.fetchall()
        return query_results
    except Exception as e:
        return e

def get_company_name(key: int):
    cur = db_connection()
    try:
        cur.execute(f"SELECT Company_Name FROM metadata.company_details WHERE Company_Key={key}")
        query_results = cur.fetchall()
        return query_results
    except Exception as e:
        return e
'''