import plotly.express as px
from dash import Output, Input

from charts.pie_chart import pie_chart
from util import add_condition_to_query


class donut_chart(pie_chart):
    def __init__(self, query, app, name, value, title='', hole = 0, titlu_axa_y='',
                 query_total='', dropdown_input="",color=px.colors.sequential.RdBu,column_to_add=''): #,template=''):
        super().__init__(query,  app, name, value, title=title, query_total=query_total, titlu_axa_y=titlu_axa_y, dropdown_input=dropdown_input,column_to_add=column_to_add)
        self.hole = hole
        self.color = color


    def draw_chart(self, name,value, title, df,hole):
        fig = px.pie(df, values = value, names = name, title=title,hole=hole)
        fig.add_annotation(
            text=f"{self.titlu_name}<br>{self.center_value}",
            x = 0.5,
            y=0.5,
            align = "center",
            showarrow = False
         )
        fig.update_traces(marker={'colors': self.color})
        return fig

    @property
    def id(self):
        return self._id

    # @id.setter
    # def id(self, id):
    #     self._id = id

    def register_callback(self,id):
        @self._app.callback(
            Output(self._id, 'figure'),
            Input(self._id, 'id')  # folosim id ca trigger
        )
        def update_figure(_):
            # query_per_team = add_condition_to_query(self._query, val, self.column_to_add)
            df = self.get_data(query=self._query)
            self.center_value = sum(self.get_data(query=self.query_total)["count"])
            return self.draw_chart(self._name, self._value, self._title, df, self.hole)