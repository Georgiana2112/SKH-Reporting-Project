from dash import Output, Input
from typing_extensions import override

from charts.donut_chart import donut_chart
from util import add_condition_to_query


class one_drop_donut_chart(donut_chart):
    @override
    def register_callback(self, id_bar):
        @self._app.callback(
            Output(component_id=self.id, component_property='figure'),
            Input(component_id=self.dropdown_input, component_property='value')
        )
        def callbacks_s_function(val):  # val = optiunile alese din dropdown
            query_per_team = add_condition_to_query(self._query, val, self.column_to_add)
            df = self.get_data(query=query_per_team)
            self.center_value = sum(self.get_data(query=query_per_team)["count"])
            return self.draw_chart(self._name, self._value, self._title, df, self.hole)