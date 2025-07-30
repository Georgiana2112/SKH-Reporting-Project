import uuid

import pandas as pd
from dash import Output, Input, dcc, dash_table, html

from charts.chart import chart
from util import add_condition_to_query


class data_table(chart):

    def __init__(self,query,conexiune,app,x,y,dropdown_input="",title='',column_to_add=""):
        self.__query = query
        self.__conexiune = conexiune
        self.__id_generator_random = str(uuid.uuid4()) #obj clasa pentru random din python
        self.__app = app
        self.id = f"bar{self.__id_generator_random}"
        self.__x = x
        self.__y = y
        self.__title = title
        self.column_to_add = column_to_add
        self.dropdown_input = dropdown_input
        self.register_callback(self.id)

    def layout(self):

        return html.Div(
            style={"font-family" : "verdana, arial, sans-serif","background-color" : "white","padding" : "10px"},
            children =[
                html.Div(
                    style = {"color":'rgb(30, 32, 71)', 'padding':'20px'},
                    children=
                    [
                        self.__title
                    ]
                ),
                dash_table.DataTable(
                id = self.id,
                page_size=10,
                sort_action='none',
                filter_action='none',
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
                data=[],
                columns=[])])

    def draw_chart(self, df):
        return {
           'data' : df.to_dict('records'),
            'columns' : [{'name':col, 'id':col} for col in df.columns]
        }

    def create_pivot_with_totals(self,df,index_col, columns_col):
        pivot_df=pd.pivot_table(
            df,
            index='jira_status',
            columns='priority',
            aggfunc='size',
            fill_value=0,
        )
        pivot_df['Total']=pivot_df.sum(axis=1)

        pivot_df.loc['Total'] = pivot_df.sum(axis=0)

        pivot_df = pivot_df.reset_index().rename(columns={index_col: 'Status'})

        desired_cols = ['Status', 'High', 'Medium', 'Low', 'Total']
        cols_to_keep = [col for col in desired_cols if col in pivot_df.columns]
        pivot_df = pivot_df[cols_to_keep]

        return pivot_df

    def get_data(self,query):
        return pd.read_sql_query(query,con=self.__conexiune,)

    def transform_data(self,df):
        return self.create_pivot_with_totals(df,index_col='jira_status',columns_col='priority')

    def register_callback(self,id_bar):
        @self.__app.callback(
            Output(component_id = self.id, component_property='data'),
            Output(component_id = self.id, component_property='columns'),
            Input(component_id = self.dropdown_input, component_property='value')
        )
        def callbacks_s_function(val_query):
            query_filtered = add_condition_to_query(self.__query, val_query, self.column_to_add)
            df = self.get_data(query_filtered)
            df_pivot=self.transform_data(df)
            config = self.draw_chart(df_pivot)
            return config['data'], config['columns']
