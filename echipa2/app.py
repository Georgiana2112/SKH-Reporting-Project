from flask import Flask
from dash import Dash
import dash_functions

app = Flask(__name__)

dash = Dash(__name__,server = app, url_base_pathname="/")


dash.layout = dash_functions.layout(dash)
dash_functions.callbacks(dash)

if __name__ == '__main__':
    app.run(debug=True)