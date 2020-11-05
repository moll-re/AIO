import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
#from dash.dependencies import Input, Output

import datetime
ex_css = [dbc.themes.BOOTSTRAP, "static/test.css"]
app = dash.Dash(__name__, external_stylesheets=ex_css)

card_main = dbc.Card(
    [
        dbc.CardImg(src="/assets/ball_of_sun.jpg", top=True, bottom=False,
                    title="Image by Kevin Dinkel", alt='Learn Dash Bootstrap Card Component'),
        dbc.CardBody(
            [
                html.H4("Learn Dash with Charming Data", className="card-title"),
                html.H6("Lesson 1:", className="card-subtitle"),
                html.P(
                    "Choose the year you would like to see on the bubble chart.",
                    className="card-text",
                ),

                dbc.Button("Still not live I guess?", color="primary"),
                # dbc.CardLink("GirlsWhoCode", href="https://girlswhocode.com/", target="_blank"),
            ]
        ),
    ],
    color="dark",   # https://bootswatch.com/default/ for more card colors
    inverse=True,   # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)

card_question = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Question 1", className="card-title"),
            html.P("What was India's life expectancy in 1952?", className="card-text"),
            dbc.ListGroup(
                [
                    dbc.ListGroupItem("A. 55 years"),
                    dbc.ListGroupItem("B. 37 years"),
                    dbc.ListGroupItem("C. 49 years"),
                ], flush=True)
        ]),
    ], color="warning",
)





today = datetime.date.today().strftime("%d.%m.%Y")
tag = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"][datetime.datetime.today().weekday()]

string_header = tag + ", der " + today


app.layout = html.Div([
    html.Header(children = [
        html.H1(string_header)
    ]),
    html.Div(
        className = "content",
        style = {"padding-top" : "32em"},
        children = [
            dbc.Row([dbc.Col(card_main, width=3),
                     dbc.Col(card_question, width=3)], justify="around"),  # justify="start", "center", "end", "between", "around"

            # dbc.CardGroup([card_main, card_question, card_graph])   # attaches cards with equal width and height columns
            # dbc.CardDeck([card_main, card_question, card_graph])    # same as CardGroup but with gutter in between cards

            # dbc.CardColumns([                        # Cards organised into Masonry-like columns
            #         card_main,
            #         card_question,
            #         card_graph,
            #         card_question,
            #         card_question,
            # ])
    ])
])




if __name__ == "__main__":
    app.run_server(host="0.0.0.0")
