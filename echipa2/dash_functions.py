
import pandas as pd
from dash import html, Output, Input

from charts.one_drop_donut_chart import one_drop_donut_chart

from charts.two_dropdown_donut_chart import two_dropdown_donut_chart
from config import QUERIES
from charts.data_table import data_table

from util import db_con, build_drop, get_dual_dropdown_options  # , build_dual_drop

def callbacks(dash):
    @dash.callback(
        [Output(component_id = "team_drop", component_property='options'),
         Output(component_id = "team_drop", component_property='value')],
        [Input(component_id = "team_drop", component_property='id')]
    )
    def dropdown_team_select(my_dropdown):
        options = pd.read_sql_query(QUERIES["teams"],db_con)["agile_team"]
        value = options
        return options, value

    @dash.callback(
        Output("test_level_drop", "options"),
        Input("requirement_level_drop", "value")
    )
    def update_test_level(selected_req_level):
        options_dict = get_dual_dropdown_options()
        return [{'label': i, 'value': i} for i in options_dict.get(selected_req_level, [])]


def layout(dash):
    #DataFrame pentru selectarea echipei
    date_echipe = pd.read_sql_query(QUERIES["teams"],db_con)["agile_team"]
    all_options = [{'label': i, 'value': i} for i in date_echipe]

    date_echipe = pd.read_sql_query(QUERIES["teams"],db_con)["agile_team"]
    all_options = [{'label': i, 'value': i} for i in date_echipe]

    date_echipe = pd.read_sql_query(QUERIES["teams"],db_con)["agile_team"]
    all_options = [{'label': i, 'value': i} for i in date_echipe]

    dual_options_dict = get_dual_dropdown_options()

    #definire chart-uri
    priority_by_problem_report_pie =one_drop_donut_chart(QUERIES["count_priority-type_problem_report"],
                                                 dash,"priority","count", title="Open PRs by Priority",
                                                hole=0.4, titlu_axa_y="PRs", query_total= QUERIES["count_all_elements"],
                                                dropdown_input="team_drop",column_to_add='agile_team')
    severity_count_donut = one_drop_donut_chart(QUERIES["count_severity"], dash, "severity", "count",
                                       hole=0.4, titlu_axa_y="PRs", query_total= QUERIES["count_all_elements"],
                                       title="Open PRs by Severity", dropdown_input="team_drop",
                                       column_to_add='agile_team')
    jira_count_donut = one_drop_donut_chart(QUERIES["count_jira_status"],  dash,
                                   "jira_status", "count", hole=0.4, titlu_axa_y="PRs",
                                   query_total=QUERIES["count_all_elements"], title="Problem Reports by Status",
                                   dropdown_input="team_drop",column_to_add='agile_team')

    open_prs_table = data_table(QUERIES["count_open_prs"], db_con, dash, x="", y="",
                                title="Open PRs by Priority and Status",dropdown_input="team_drop",column_to_add='agile_team')
    feature_status_report_donut = one_drop_donut_chart(QUERIES["count_feature_status"],
                                         dash, "status_group", "count", title="Feature Status",
                                        hole=0.4, titlu_axa_y="Features", query_total=QUERIES["count_all_elements"],
                                        dropdown_input="team_drop",column_to_add='agile_team')


    donut_syrd_requirements_status = two_dropdown_donut_chart(QUERIES["syrd_requirement_status"],
                                              dash, "syrd_state", "count", title="SyRD Requirements Status",
                                              hole=0.4, titlu_axa_y="SyRD", query_total=QUERIES["total_syrd_requirement"],
                                              dropdown_input="requirement_level",dropdown_input2="test_level",
                                                              column_to_add="requirement_level",column_to_add2="test_level")
    CRD_count_Implementations = two_dropdown_donut_chart(QUERIES["crd_implemented_requirements"], dash, "implementation_status",
                                            "count", hole=0.4, titlu_axa_y="PRs",
                                            query_total=QUERIES["count_all_implemententions"],
                                            title="CRD Requirements Implemented in Software",dropdown_input="requirement_level",
                                                         dropdown_input2="test_level",column_to_add="requirement_level",
                                                         column_to_add2="test_level")
    sys_sw_testcases = two_dropdown_donut_chart(QUERIES["sys_sw_testcases"], dash, "test_case_status",
                                            "count", hole=0.4, titlu_axa_y="PRs",
                                            query_total=QUERIES["sys_sw_testcases"],
                                            title="Sys+Sw Requirements with Test Cases",dropdown_input="requirement_level",
                                                dropdown_input2="test_level",column_to_add="requirement_level",
                                                column_to_add2="test_level")



    return html.Div(
            style={ 'background-color': 'rgb(255, 250, 240)'},
            children =[
                html.Div(
                    style={'padding-left' : '20%', 'padding-right' : '20%', 'padding-top' : '20px'},

                    children=[
                        build_drop("team_drop", "Alege echipa dorita", options=[all_options]+[
                        {'label': i , 'value': i,} for i in date_echipe],
                        value = [all_options],
                        multi = True)
                    ]
                ),

                html.Div(
                    style={'display': 'grid', 'gridTemplateColumns': 'repeat(2,1fr)',
                           'gridTemplateRows': 'repeat(2,400px)',
                           'gap': '30px', 'padding': '30px'},
                    children=[
                        priority_by_problem_report_pie.layout(),
                        severity_count_donut.layout(),
                        jira_count_donut.layout(),
                        open_prs_table.layout(),
                        feature_status_report_donut.layout(),
                        html.Div(),

                        html.Div([
                            build_drop("requirement_level", "Selectează requirement_level",
                                       options=[{'label': i, 'value': i} for i in dual_options_dict.keys()],
                                       value=None)
                        ]),
                        html.Div([
                            build_drop("test_level", "Selectează test_level",
                                       options=[{'label': i, 'value': i} for i in
                                                dual_options_dict[list(dual_options_dict.keys())[0]]],
                                       value=None)
                        ]),
                        # html.Div(),
                        CRD_count_Implementations.layout(),
                        donut_syrd_requirements_status.layout(),
                        sys_sw_testcases.layout()
                    ]
                )
    ])

