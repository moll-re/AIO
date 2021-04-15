import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf8")
#from dash.dependencies import Input, Output

import datetime
import time
import xmltodict

import requests

from . import helpers

class DashBoard():
    """"""
    # added by the launcher, we have self.modules (dict)

    def __init__(self, host_ip, prst):
        ## pre-sets
        
        self.inter_margin = "1em"
        self.persistence = prst
        self.host_ip = host_ip
        ex_css = [dbc.themes.BOOTSTRAP]
        self.app = dash.Dash(__name__, external_stylesheets=ex_css)
        self.app.layout = html.Div([
            html.Div(id = 'layout-update', className = "content", style={"padding":self.inter_margin},),
            dcc.Interval(
                id='interval-component',
                interval=3600*1000, # in milliseconds
                n_intervals=0
                )
        ]#,style={'background-image':'url("static/background.jpg")'}
        )

        @self.app.callback(Output('layout-update','children'), Input('interval-component','n_intervals'))
        def update_layout(n):
            self.set_stats()
            kids = [
                self.card_header(),
                dbc.CardColumns([
                    # self.card_weather(),
                    *self.cards_lists(),
                    self.card_bot_stats(),
                    self.card_news(),
                    self.card_xkcd(),
                    self.card_sensor_stats(),
                ])
            ]
            return kids


    def start(self):
        self.app.run_server(host=self.host_ip, port=80)#, debug=True)


    def card_header(self):
        today = datetime.date.today().strftime("%A, der %d. %B %Y")
        card = dbc.Card(
            [   dbc.CardImg(src="static/header.jpg", top=True, bottom=False,
                title="Header", alt='Header image'),
                dbc.CardBody([html.H3(today, className="card-title")]),
            ],
            color="dark",
            style = {"width" : "100%", "margin-bottom":self.inter_margin},
            inverse=True,
            )
        return card
    

    def cards_lists(self):
        ret = []
        for l in self.persistence["global"]["lists"].keys():
            l_content = self.persistence["global"]["lists"][l]
            html_content = [html.A(t, href="#", className="list-group-item bg-dark list-group-item-action text-light") for t in l_content]
            card = dbc.Card(
                [   
                    dbc.CardBody([
                        html.H4("Liste '" + l + "':", className="card-title"),
                        dbc.ListGroup(html_content, flush=True, style={"color":"black"})
                    ]),
                ],
                color="dark",
                inverse=True,
                )
            ret.append(card)
        return ret


    def card_bot_stats(self):
        if not self.stat_graph:
            self.set_stats()

        card = dbc.Card(
                [   
                    dbc.CardBody([
                        html.H4("Chat-Metriken", className="card-title"),
                        dcc.Graph(figure=self.stat_graph, config={'displayModeBar': False})
                    ]),
                ],
                color="dark",
                inverse=True,
                )
        return card

    def card_sensor_stats(self):
        fig = go.Figure()
        sensors = self.persistence["clock"]["sensors"]
        time = sensors["time"]
        time = time - time[0] # rescale
        for sensor in sensors.keys():
            if sensor != "time":
                fig.add_trace(go.Scatter(x=time, y=sensors[sensor], mode="lines", text=sensor, line=dict(width=4)))
            
        fig.layout.update(
        #     xaxis = {
        #         'showgrid': False, # thin lines in the background
        #         'zeroline': False, # thick line at x=0
        #         'visible': False,  # numbers below
        #     }, # the same for yaxis
        #     yaxis = {
        #         'showgrid': False, # thin lines in the background
        #         'zeroline': False, # thick line at x=0
        #         'visible': False,  # numbers below
        #     }, # the same for yaxis

            showlegend=False,
        #     margin=dict(l=0, r=0, t=0, b=0),
        #     paper_bgcolor='rgba(0,0,0,0)',
        #     plot_bgcolor='rgba(0,0,0,0)',
            )

        card = dbc.Card(
                [   
                    dbc.CardBody([
                        html.H4("Sensor-Metriken", className="card-title"),
                        dcc.Graph(figure=fig, config={'displayModeBar': False})
                    ]),
                ],
                color="dark",
                inverse=True,
                )
        return card


    def card_weather(self):
        def weather_item(name, overview, temps):
            if len(temps) == 2:
                temp = "🌡(❄): " + str(temps[0]) + "°  ➡  🌡(🔥): " + str(temps[1]) + "°"
            else:
                temp = "🌡: " + str(temps[0]) + "°"
            temp_line = html.P(temp, className="mb-1")

            it = html.A([
                html.Div([
                    html.H5(name, className="mb-1"),
                    html.Span(categories[overview], className="badge badge-primary badge-pill")
                    ],
                    className="d-flex w-100 justify-content-between"),
                temp_line,
                ],
                href="#", className="list-group-item bg-dark list-group-item-action text-light"
            )

            return it

        days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        categories = {"Clouds": "☁", "Rain": "🌧", "Thunderstorm": "🌩", "Drizzle": ":droplet:", "Snow": "❄", "Clear": "☀", "Mist": "🌫", "Smoke": "Smoke", "Haze": "Haze", "Dust": "Dust", "Fog": "Fog", "Sand": "Sand", "Dust": "Dust", "Ash": "Ash", "Squall": "Squall", "Tornado": "Tornado",}
        today = datetime.datetime.today().weekday()

        body = []
        
        try:
            bot = self.modules["bot"]
            content = bot.api_weather.show_weather([47.3769, 8.5417]) # still zürich
            
            wt = content.pop(0)
            body.append(weather_item("Jetzt", wt["short"], wt["temps"]))

            for i, day in enumerate(content):
                tmp = []
                if i == 0:
                    day_name = "Heute"
                else:
                    day_name = days[(today + i) % 7]

                body.append(weather_item(day_name, day["short"], day["temps"]))
            body = dbc.ListGroup(body, flush=True, style={"color":"black"})


        except:
            body.append(html.H6("Konnte nicht geladen werden"))

        card = dbc.Card(
            [dbc.CardBody([
                html.H4("Wetter", className="card-title"),
                body])],
            color="dark",
            inverse=True,
            )
        return card


    def card_news(self):
        try:
            card = dbc.Card([
                dbc.CardBody([html.Iframe(src="https://nzz.ch", style={"border":"none", "min-height":"30em", "width":"100%"})])
            ],
            color="dark",
            inverse=True,
            )
        except:
            card = card = dbc.Card([
                dbc.CardBody([
                    html.H4("Could not load NEWS", className="card-title"),
                    ])
            ],
            color="dark",
            inverse=True,
            )
        return card
    

    def card_xkcd(self):
        try:
            xml = requests.get("https://xkcd.com/atom.xml").content
            feed = xmltodict.parse(xml)
            title = feed["feed"]["entry"][0]["title"]
            img = feed["feed"]["entry"][0]["summary"]["#text"]
            i1 = img.find('"') +1
            i2 = img.find('"', i1+1)
            i3 = img.find('"', i2+1) + 1
            i4 = img.find('"', i3+1)
            img_src = img[i1:i2]
            img_alt = img[i3:i4]
            card = dbc.Card([
                dbc.CardBody([
                    html.H4(title, className="card-title"),
                    html.Img(src=img_src, style={"width":"100%"}),
                    html.P(img_alt)
                    ])
            ],
            color="dark",
            inverse=True,
            )
        except:
            card = dbc.Card([
                dbc.CardBody([
                    html.H4("Could not load XKCD", className="card-title"),
                    ])
            ],
            color="dark",
            inverse=True,
            )
        return card


    ######### helper:
    def set_stats(self):
        xs, ys = helpers.clean_axis(self.persistence["bot"]["send_activity"]["hour"], self.persistence["bot"]["send_activity"]["count"])
        xr, yr = helpers.clean_axis(self.persistence["bot"]["receive_activity"]["hour"], self.persistence["bot"]["receive_activity"]["count"])
        xe, ye = helpers.clean_axis(self.persistence["bot"]["execute_activity"]["hour"], self.persistence["bot"]["execute_activity"]["count"])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xr, y=yr, mode="lines", text="Gelesen", line=dict(width=4)))
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", text="Gesendet", line=dict(width=4)))
        fig.add_trace(go.Scatter(x=xe, y=ye, mode="lines", text="Ausgeführt", line=dict(width=4)))
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.layout.update(
            xaxis = {
                'showgrid': False, # thin lines in the background
                'zeroline': False, # thick line at x=0
                'visible': False,  # numbers below
            }, # the same for yaxis
            yaxis = {
                'showgrid': False, # thin lines in the background
                'zeroline': False, # thick line at x=0
                'visible': False,  # numbers below
            }, # the same for yaxis

            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            )
        
        self.stat_graph = fig
