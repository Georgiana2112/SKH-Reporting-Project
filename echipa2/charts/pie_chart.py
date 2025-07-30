import uuid
import pandas as pd
import plotly.express as px
from dash import Output, Input, dcc
from charts.chart import chart
from util import db_con


class pie_chart(chart):
    def __init__(self, query,   app, name, value, dropdown_input="", title='', hole = 0, titlu_axa_y='',
                 query_total='',column_to_add=''): #,template=''):
        self._query = query
        self._id_generator_random = str(uuid.uuid4()) #obj clasa pentru random din python
        self._app = app
        self._id = f"pie{self._id_generator_random}"
        self._name = name
        self._value = value
        self._title = title
        self.hole = 0
        self.query_total = query_total
        self.center_value = ""
        self.column_to_add = column_to_add
        self.titlu_name = titlu_axa_y
        self.dropdown_input = dropdown_input
        self.register_callback(self.id)

    def layout(self):
         #return dcc.Graph(id = self.id, figure = self.__bar_chart)
        return dcc.Graph(id = self.id)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self,id):
        self._id=id

    def draw_chart(self, name,value, title, df,hole):
        return px.pie(df, values = value, names = name, title=title,hole=hole)#,color_discrete_sequence=colors)

    def get_data(self,query=''):
        return pd.read_sql_query(query,con = db_con)


    def register_callback(self, id):
        @self._app.callback(
            Output(component_id=self.id, component_property='figure'),
            Input(component_id=self.id, component_property='id')
        )
        def callbacks_s_function(id):
            df = self.get_data(self._query)
            return self.draw_chart(self._name, self._value, self._title, df, self.hole)