##### on_ice_xg_rates.py #####
# A program to display skaters on-ice xG rates
# Zach Andrews

# Import modules
from shiny import *
import shinyswatch
import plotly.graph_objs as go
from shinywidgets import output_widget, register_widget, render_widget
import pandas as pd
import plotly.express as px
from configure import base_url

path = "data/on_ice_xg.csv"

df = pd.read_csv(path)

def server(input, output, session):
    @output
    @render.table
    def table():
        df = pd.read_csv(path)
        if input.z() == "T":
            asc = True
        else:
            asc = False
        df = df[(df['Team']==input.x())&(df['EV_TOI']>=input.toi())]
        df = df[['Player','EV_TOI','xGF/60','xGA/60']].sort_values(by=input.y(),ascending=asc).round(3)
        return df
    
    @output
    @render_widget
    def my_widget():
        df = pd.read_csv(path)
        team = input.x()
        data = df[(df['Team']==team)&(df['EV_TOI']>=input.toi())]
        fig = px.scatter(data, 'xGF/60', 'xGA/60',color="EV_TOI",template="plotly_dark",height=1050,width=1050,text='Player')
        fig.update_traces(textposition='top right',marker=dict(size=10))
        fig.update(layout_xaxis_range = [.01,6])
        fig.update(layout_yaxis_range = [6,.01])
        fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False,plot_bgcolor="#222222",paper_bgcolor="#222222")
        fig.update_layout(
            title=(team + " Skaters Even-Strength On-Ice xG Rates<br>"+
            "<i>2022-23 NHL Playoffs</i><br>" +
            "<i>Minimum "+ str(input.toi()) +" EV TOI</i>"),
            margin=dict(r=20, l=40, b=100, t=90),
            template='plotly_dark')
        fig.add_annotation(
            text = ("Data: @StatsByZach on Twitter")
            , showarrow=False
            , x = .80
            , y = -.045
            , xref='paper'
            , yref='paper' 
            , xanchor='left'
            , yanchor='bottom'
            , xshift=-1
            , yshift=-5
            , font=dict(size=11, color="white")
            , align="left"
        )
        return fig
    
    @reactive.Effect
    def _():
        val = input.quant()
        ui.update_slider(
            "toi", value=val
        )

    @reactive.Effect
    def _2():
        btn = input.btn()
        if btn % 2 == 1:
            tab = ui.output_table("table")
            ui.insert_ui(
                ui.div({"id": "inserted-slider"},ui.tags.h5("Sort Table by", class_="app-heading"),ui.input_select("y","",{"Player":"Player","EV_TOI":"EV_TOI","xGF/60":"xGF/60","xGA/60":"xGA/60"}),
            ui.input_radio_buttons(
        "z", "", {"F": "High to Low", "T": "Low to High"}
    ),ui.output_table("table")),
                selector="#main-content",
                where="beforeEnd",
            )
        elif btn > 0:
            ui.remove_ui("#inserted-slider")

on_ice_xg = App(ui.page_fluid(
    ui.tags.base(href=base_url),
    ui.tags.div(
         {"style": "width:75%;margin: 0 auto"},
        ui.tags.style(
            """
            h4 {
                margin-top: 1em;font-size:35px;
            }
            h2{
                font-size:25px;
            }
            """
         ),
    shinyswatch.theme.darkly(),
    ui.tags.h4("Stats By Zach"),
    ui.tags.i("A website for hockey analytics"),
    ui.navset_tab(
        ui.nav_control(
             ui.a(
                "Home",
                href="home/"
            ),
        ),
        ui.nav_menu(
            "Skater Charts",
            ui.nav_control(
             ui.a(
                "On-Ice xG Rates",
                href="skater-xg-rates/"
            ),
            ui.a(
                "On-Ice xGF%",
                href="skater-xg-percentages/"
            ),
        ),
        ),
        ui.nav_menu(
            "Goalie Charts",
            ui.nav_control(
             ui.a(
                "GSAx Timeline",
                href="gsax-timeline/"
            ),
             ui.a(
                "GSAx Leaderboard",
                href="gsax-leaderboard/"
            ),
             ui.a(
                "GSAx Comparison",
                href="gsax-comparison/"
            )
        ),
        ),ui.nav_menu(
            "Team Charts",
            ui.nav_control(
             ui.a(
                "Team xG Rates",
                href="team-xg-rates/"
            ),
        ),
        ),ui.nav_control(
             ui.a(
                "Games",
                href="games/"
            ),
        ),ui.nav_control(
             ui.a(
                "About",
                href="about/"
            ),
        )
        ),ui.row(
        ui.column(3,ui.tags.br(),ui.tags.h2("Even-Strength On-Ice xG Rates"),ui.tags.h5("Select a Team", class_="app-heading"),
            ui.input_select("x", "", { "ANA": "Anaheim Ducks",
            "ARI": "Arizona Coyotes",
            "BOS": "Boston Bruins",
            "BUF": "Buffalo Sabres",
            "CGY": "Calgary Flames",
            "CAR": "Carolina Hurricanes",
            "CHI": "Chicago Blackhawks",
            "COL": "Colorado Avalanche",
            "CBJ": "Columbus Blue Jackets",
            "DAL": "Dallas Stars",
            "DET": "Detroit Red Wings",
            "EDM": "Edmonton Oilers",
            "FLA": "Florida Panthers",
            "L.A": "Los Angeles Kings",
            "MIN": "Minnesota Wild",
            "MTL": "Montreal Canadiens",
            "NSH": "Nashville Predators",
            "N.J": "New Jersey Devils",
            "NYI": "New York Islanders",
            "NYR": "New York Rangers",
            "OTT": "Ottawa Senators",
            "PHI": "Philadelphia Flyers",
            "PIT": "Pittsburgh Penguins",
            "S.J": "San Jose Sharks",
            "SEA":"Seattle Kraken",
            "STL": "St. Louis Blues",
            "T.B": "Tampa Bay Lightning",
            "TOR": "Toronto Maple Leafs",
            "VAN": "Vancouver Canucks",
            "VGK": "Vegas Golden Knights",
            "WSH": "Washington Capitals",
            "WPG": "Winnipeg Jets"}),
                                      ui.tags.h5("Minimum EV TOI", class_="app-heading"),
            ui.input_slider("toi", "", min=0, max=round(df['EV_TOI'].max(),0), value=round(df['EV_TOI'].quantile(.25),1)),
            ui.tags.h5("EV TOI Percentile (Among All NHL Skaters)"),
        ui.input_radio_buttons(
        "quant",
        "",
        {
            round(df['EV_TOI'].quantile(.25),1): "Top 75%",
            round(df['EV_TOI'].quantile(.5),1): "Top 50%",
            round(df['EV_TOI'].quantile(.75),1): "Top 25%",
        },
    ), ui.input_action_button("btn", "Toggle Table"),ui.div({"id":"main-content"}),
        #ui.output_table("table")
        ),
        ui.column(9,output_widget("my_widget"),title="Stats By Zach",
    )))),server)
