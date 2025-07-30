import os
import re
from pathlib import Path

import pandas as pd
from dash import html, dcc
from dotenv import load_dotenv
from sqlalchemy import create_engine

from config import QUERIES

load_dotenv(Path('util.env'))


DB_PASSWORD = os.getenv('DB_PASSWORD')
USER = os.getenv('USER')
LOCALHOST = os.getenv('LOCALHOST')
PORT = str(os.getenv('PORT'))
DB_NAME = os.getenv('DB_NAME')

#conectarea la baza de date
db_con = create_engine(f'postgresql+psycopg2://{USER}:{DB_PASSWORD}@{LOCALHOST}:{PORT}/{DB_NAME}')

def build_drop(id,titlu,**kwargs):
    return html.Div(
        children=[
            html.Label(title=titlu),
            dcc.Dropdown(id=id,**kwargs)
        ])

def  build_dual_drop(id,titlu,**kwargs):
    return html.Div(
        children=[
            html.Label(title=titlu),
            dcc.Dropdown(id=id, **kwargs)
        ])

def get_dual_dropdown_options():
    df = pd.read_sql_query(QUERIES["crd_test_requirement_level"], db_con)
    options_dict = {}
    for req_level in df["requirement_level"].unique():
        sub_df = df[df["requirement_level"] == req_level]
        options_dict[req_level] = sub_df["test_level"].unique().tolist()
    return options_dict

def add_condition_to_query(query,lista_de_adaugat_in_query,coloana):
    if lista_de_adaugat_in_query == [] or 'None' in lista_de_adaugat_in_query or lista_de_adaugat_in_query == [None]:
        return query
    conditii = " OR ".join([f'{coloana} = \'{val}\'' for val in lista_de_adaugat_in_query])
    conditie_noua = f"({conditii})"

    query_lower = query.lower()

    has_where = " where " in query_lower

    clauses = ["group by", "order by", "limit", "having"]
    positions = []
    for clause in clauses:
        match = re.search(r'\b' + clause + r'\b', query_lower)
        if match:
            positions.append(match.start())

    insert_pos = min(positions) if positions else len(query)

    if has_where:
        # Adaugam conditia cu AND inainte de insert_pos
        query_nou = query[:insert_pos] + f" AND {conditie_noua}" + query[insert_pos:]
    else:
        # Nu exista WHERE, inseram WHERE inainte de insert_pos
        query_nou = query[:insert_pos] + f" WHERE {conditie_noua}" + query[insert_pos:]

    return query_nou

