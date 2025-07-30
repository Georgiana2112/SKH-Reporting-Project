import plotly.express as px
from dash import Output, Input
from typing_extensions import override

from charts.donut_chart import donut_chart
from util import add_condition_to_query


class two_dropdown_donut_chart(donut_chart):
    def __init__(self, query, app, name, value, hole=0.4 ,title='' , titlu_axa_y='',
                 query_total='', dropdown_input = "",dropdown_input2 = "",column_to_add='',column_to_add2=''): #,template=''):
        self.dropdown_input2 = dropdown_input2
        self.column_to_add2 = column_to_add2
        super().__init__(query,  app, name, value, title=title, query_total=query_total,
                         hole=hole,titlu_axa_y=titlu_axa_y, dropdown_input=dropdown_input,column_to_add=column_to_add)

    @override
    def register_callback(self, id_bar):
        @self._app.callback(
            Output(component_id = self.id, component_property='figure'),
            [Input(component_id = self.dropdown_input, component_property='value'),
            Input(component_id = self.dropdown_input2, component_property='value')]

        )
        def callbacks_s_function(val1,val2):  # val = optiunile alese din dropdown
            query_first_add = add_condition_to_query(self._query, [val1], self.column_to_add)
            query_second_add = add_condition_to_query(query_first_add, [val2], self.column_to_add2)
            df = self.get_data(query = query_second_add)
            try:
                self.center_value = sum(self.get_data(query=query_second_add)["count"])
            except:
                return

            return self.draw_chart(self._name, self._value, self._title,  df, self.hole)