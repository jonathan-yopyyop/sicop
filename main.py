import os
from datetime import datetime

import psycopg2
import pyodbc


def get_cursor():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")
    conn_string = f"host='{host}' dbname='{db}' user='{user}' password='{password}' port='{port}'"
    print(f"Connecting to database: {conn_string}")
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    return cursor


def get_query_results(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()


def get_xirux_cursor():
    xirux_user = os.getenv("MSSQL_XIRUX_USER")
    xirux_password = os.getenv("MSSQL_XIRUX_PASSWORD")
    xirux_host = os.getenv("MSSQL_XIRUX_HOST")
    xirux_port = os.getenv("MSSQL_XIRUX_PORT")
    xirux_db = os.getenv("MSSQL_XIRUX_DB")
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};SERVER="
        + xirux_host
        + ";PORT="
        + xirux_port
        + ";DATABASE="
        + xirux_db
        + ";UID="
        + xirux_user
        + ";PWD="
        + xirux_password
        + ";Encrypt=no",
    )
    cursor = conn.cursor()
    return cursor


def get_results_xirux(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()


def business_units():
    cursor = get_cursor()
    cursor_xirux = get_xirux_cursor()
    query_xirux = "select * from ConTipCen"
    results_xirux = get_results_xirux(cursor_xirux, query_xirux)
    for result in results_xirux:
        query = "SELECT * FROM integration_businessunit"
        results = get_query_results(cursor, query)
        for result in results:
            print(result)
        IdTipCen = result[0]
        Nombre = result[1]
        Nemoni = result[2]
        IdUsuari = result[3]
        Operac = result[4]
        FecMod = result[5]
        query = f"SELECT * FROM integration_businessunit where 'IdTipCen' = '{IdTipCen}'"
        results = get_query_results(cursor, query)
        now = datetime.now()
        if len(results) == 0:
            try:
                query = f"""
                INSERT INTO public.integration_businessunit
                (status, created_at, updated_at, "FecMod", "IdUsuari", "Nemoni", "Nombre", "Operac", "IdTipCen")
                VALUES({True}, '{now}', '{now}', '{FecMod}', '{IdUsuari}', '{Nemoni}', '{Nombre}', '{Operac}', '{IdTipCen}');
                """  # noqa
                cursor.execute(query)
                # print("Inserted")
            except Exception as e:
                print(e)

        else:
            try:
                query = f"""
                UPDATE public.integration_businessunit
                SET updated_at='{now}', "FecMod"='{FecMod}', "IdUsuari"='{IdUsuari}', "Nemoni"='{Nemoni}', "Nombre"='{Nombre}', "Operac"='{Operac}'
                WHERE 'IdTipCen'='{IdTipCen}';
                """  # noqa
                query = f"UPDATE integration_businessunit SET 'Nombre '= '{Nombre}', 'Nemoni' = '{Nemoni}', 'IdUsuari' = '{IdUsuari}', 'Operac' = '{Operac}', 'FecMod' = '{FecMod}' WHERE 'IdTipCen' = '{IdTipCen}'"  # noqa
                cursor.execute(query)
                print("Updated")
            except Exception as e:
                print(e)


business_units()
