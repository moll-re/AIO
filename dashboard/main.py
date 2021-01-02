import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf8")
#from dash.dependencies import Input, Output

import datetime
import time
import xmltodict

import requests
import emoji

class DashBoard():
    """"""
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
        ])

        @self.app.callback(Output('layout-update','children'), Input('interval-component','n_intervals'))
        def update_layout(n):
            print("REFRESH")
            kids = [
                self.card_header(),
                dbc.CardColumns([
                    *self.cards_lists(),
                    self.card_news(),
                    self.card_xkcd(),
                    self.card_weather()


                ])
            ]
            return kids
            #[card_header, dbc.CardColumns([card_shopping_list,card_placeholder,card_placeholder,card_placeholder,card_placeholder,card_placeholder])]


    def launch_dashboard(self):
        self.app.run_server(host=self.host_ip)#, debug=True)


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
            html_content = [dbc.ListGroupItem(t) for t in l_content]
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


    # def card_bot_stats(self):
    #     return card

    def card_weather(self):
        try:
            body = [html.H4("Wetter", className="card-title")]

            content = self.bot.weather.show_weather([47.3769, 8.5417]) # still zürich
            
            wt = content.pop(0)
            body.append(html.Span(children=[
                html.H6("Jetzt: " + wt["short"]),
                html.P(emoji.emojize(":thermometer: ") + str(wt["temps"][0]) + "°")
            ]))

            days = ["Montag", "Dienstag", "Miitwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
            today = datetime.datetime.today().weekday()

            for i, day in enumerate(content):
                tmp = []
                if i == 0:
                    tmp.append(html.H6("Heute: "+ day["short"]))
                else:
                    tmp.append(html.H6(days[(today + i + 1) % 7] + ": " + day["short"]))
                tmp.append(html.P(emoji.emojize(":thermometer: :fast_down_button: " + str(day["temps"][0]) + "° , :thermometer: :fast_up_button: " + str(day["temps"][1]) + "°")))

                body.append(html.Span(children=tmp))


            card = dbc.Card(
                [dbc.CardBody(body)],
                color="dark",
                inverse=True,
                )
        except:
            card = card = dbc.Card([
                dbc.CardBody([
                    html.H4("Could not load WEATHER", className="card-title"),
                    ])
            ],
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
            card = card = dbc.Card([
                dbc.CardBody([
                    html.H4("Could not load XKCD", className="card-title"),
                    ])
            ],
            color="dark",
            inverse=True,
            )
        return card



if __name__ == "__main__":
    test = DashBoard(host_ip="0.0.0.0")