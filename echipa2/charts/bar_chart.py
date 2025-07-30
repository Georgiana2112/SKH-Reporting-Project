import uuid
import pandas as pd
import plotly.express as px
from dash import Output, Input, dcc
from charts.chart import chart

class bar_chart(chart):

    def __init__(self,query,conexiune,app,x,y,title=''): #titlu_axa_y='',titlu_axa_x='',template=''):
        self.__query = query
        self.__conexiune = conexiune
        self.__id_generator_random = str(uuid.uuid4()) #obj clasa pentru random din python
        self.__app = app
        self.id = f"bar{self.__id_generator_random}"
        self.__x = x
        self.__y = y
        self.__title = title
        self.register_callback(self.id)

    def layout(self):
         #return dcc.Graph(id = self.id, figure = self.__bar_chart)
        return dcc.Graph(id = self.id)

    def draw_chart(self, x,y, title, df):
        return px.bar(df, x=x, y=y, title=title)

    def get_data(self):
        return pd.read_sql_query(self.__query,con=self.__conexiune)

    def register_callback(self, id_bar):
        @self.__app.callback(
            Output(component_id = self.id, component_property='figure'),
            Input(component_id = self.id, component_property='id')
        )
        def callbacks_s_function(id_bar):
            df = self.get_data()
            return self.draw_chart(self.__x, self.__y, self.__title, df)