##### games.,py #####

# Import modules
from shiny import *
import shinyswatch
import plotly.express as px
from shinywidgets import output_widget, render_widget
import pandas as pd
from configure import base_url
import math
import datetime


# Paths to data
gsaxt = "data/game_list.csv"
data = pd.read_csv(gsaxt)
data = data[['Home','Away','Game_Id','Date','Link']]
game_dates = ['All']
game_dates_temp = data['Date'].value_counts().keys().tolist()
game_dates_temp=game_dates_temp[::-1]
dates = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in game_dates_temp]
dates.sort()
sorteddates = [datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates]
sorteddates = sorteddates[::-1]
game_dates.extend(sorteddates)
print(game_dates)
default=game_dates[1]
def server(input,output,session):
    @output
    @render.text
    def text():
        t= 'Vi'
        return t
    
    @output
    @render.table
    def table():
        df = pd.read_csv(gsaxt)
        df = df[['Home','Away','Date','Link']]
        if input.team() =="All":
            df = df
        else:
            df = df[(df['Home']==input.team())|(df['Away']==input.team())]
        if input.date() == "All":
            df = df
        else:
            df = df[df['Date']==input.date()]
        #return df.style.set_table_attributes('escape=False class="dataframe shiny-table table w-auto"').hide_index()
        return df.style.set_table_attributes(
                    'class="dataframe shiny-table table w-auto"'
                ).set_properties(**{'border': '1.3px #222222'},).hide_index().set_table_styles(
                    [dict(selector="th", props=[("text-align", "right"),('font-size','25px')]),
                     dict(selector="tr", props=[('font-size','21px')]),]
                )

games = App(ui.page_fluid(
    ui.tags.base(href=base_url), 
    ui.tags.div(
         {"style": "width:75%;margin: 0 auto;max-width: 1500px;"},
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
        )),ui.row(
    ui.column(5,ui.tags.br(),ui.tags.h2("Games"),ui.input_select(
        "team",
        "Filter by Team:",
        {
            "All":"All",
            "ANA": "Anaheim Ducks",
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
            "WPG": "Winnipeg Jets"
        },
    ),
    ui.input_select(
        "date",
        "Filter by Date:",
        game_dates,
        selected=default
    ),ui.output_table("table"),
    )),)),server)