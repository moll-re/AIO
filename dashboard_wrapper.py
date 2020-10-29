import dash
from flask import Flask
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets = external_stylesheets)

np.random.seed(101)
random_x = np.linspace(1,5,20)
random_y = np.exp(random_x)


app.layout = html.Div(children = [
    html.H1("Hello wolrd!"),
    dcc.Graph(
    id="scatter",
    figure = {
        "data" : [
            go.Scatter(
            x = random_x,
            y = random_y,
            mode="markers"
            )
        ],
        "layout" : go.Layout(
            title="This is a test",
            xaxis={"title" : "x"},
            yaxis={"title" : "y"}
        )
    }
    ),

    ])


if __name__ == "__main__":
    app.run_server(host="0.0.0.0")
