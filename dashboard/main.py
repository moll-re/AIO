import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import locale
locale.setlocale(locale.LC_TIME, "de_DE")
#from dash.dependencies import Input, Output

import datetime


class DashBoard():
    """"""
    def __init__(self, host_ip):
        ## pre-sets
        self.today = datetime.date.today().strftime("%A, der %d. %B %Y")
        self.inter_margin = "1em"

        ex_css = [dbc.themes.BOOTSTRAP]
        self.app = dash.Dash(__name__, external_stylesheets=ex_css)
        
        self.set_layout()
        self.app.run_server(host=host_ip)
        

    def set_layout(self):

        card_placeholder = dbc.Card(
            [
                #dbc.CardImg(src="/assets/ball_of_sun.jpg", top=True, bottom=False,
                #            title="Image by Kevin Dinkel", alt='Learn Dash Bootstrap Card Component'),
                dbc.CardBody(
                    [
                        html.H4("Learn Dash with Charming Data", className="card-title"),
                        html.H6("Lesson 1:", className="card-subtitle"),
                        html.P(
                            "Choose the year you would like to see on the bubble chart. Test this is a very long text that should hopefully have a line break.",
                            className="card-text",
                        ),
                        html.P(
                            "Choose the year you would like to see on the bubble chart.",
                            className="card-text",
                        ),
                        html.P(
                            "Choose the year you would like to see on the bubble chart.",
                            className="card-text",
                        ),
                        html.P(
                            "Choose the year you would like to see on the bubble chart.",
                            className="card-text",
                        ),

                        dbc.Button("Still not live I guess?", color="primary"),
                        dbc.CardLink("GirlsWhoCode", href="https://girlswhocode.com/", target="_blank"),
                    ]
                ),
            ],
            color="dark",   # https://bootswatch.com/default/ for more card colors
            inverse=True,   # change color of text (black or white)
            outline=False,  # True = remove the block colors from the background and header
        )

        card_weather = dbc.Card(

        )

        card_bot_stats = dbc.Card(

        )


        card_header = dbc.Card(
            [   dbc.CardImg(src="static/header.jpg", top=True, bottom=False,
                title="Header", alt='Header image'),
                dbc.CardBody([html.H4(self.today, className="card-title")]),
            ],
            color="dark",
            style = {"width" : "100%", "margin-bottom":self.inter_margin},
            inverse=True,
        )

        card_shopping_list = dbc.Card(
            [
                dbc.CardBody([
                    html.H4("Shopping list:", className="card-title"),
                    # html.P("What was India's life expectancy in 1952?", className="card-text"),
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItem("test"),
                            dbc.ListGroupItem("B. 37 years"),
                            dbc.ListGroupItem("C. 49 years"),
                        ], flush=False)
                ]),
            ],
            color="dark",
            style = {"width" : "100%", "margin-bottom":self.inter_margin},
            inverse=True,
        )


        self.app.layout = html.Div([
            html.Div(
                className = "content",
                style={"padding":self.inter_margin},
                children = [
                    # dbc.Row([dbc.Col(card_main, width=3),
                    #         dbc.Col(card_question, width=3)], justify="around"),  # justify="start", "center", "end", "between", "around"
                    card_header,
                    dbc.CardColumns([
                        card_shopping_list,
                        card_placeholder,
                        card_placeholder,
                        card_placeholder,
                        card_placeholder,
                        card_placeholder,
                    ]),
                    
                ])
        ])




if __name__ == "__main__":
    test = DashBoard(host_ip="0.0.0.0")
    
