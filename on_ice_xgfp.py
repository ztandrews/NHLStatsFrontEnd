##### gsax_leaderboard.,py #####

# Import modules
from shiny import *
import shinyswatch
import plotly.express as px
from shinywidgets import output_widget, render_widget
import pandas as pd
from configure import base_url

# Paths to data
onice = "data/on_ice_xg.csv"
df = pd.read_csv(onice)
def server(input,output,session): 
    @output
    @render.table
    def table():
        df = pd.read_csv(onice)
        if input.z() == "T":
            asc = True
        else:
            asc = False
        
        if input.strength()=="even":
            df = df[(df['Team']==input.x())&(df['EV_TOI']>=input.toi())]
            if input.y() == "xGF%":
                df = df[['Player','EV_TOI','EV_xGF%']].sort_values(by='EV_xGF%',ascending=asc).round(3)
            elif input.y() == 'TOI':
                df = df[['Player','EV_TOI','EV_xGF%']].sort_values(by='EV_TOI',ascending=asc).round(3)
            else:
                df = df[['Player','EV_TOI','EV_xGF%']].sort_values(by=input.y(),ascending=asc).round(3)
        elif input.strength()=="_5v5":
            df = df[(df['Team']==input.x())&(df['5v5_TOI']>=input.toi())]
            if input.y() == "xGF%":
                df = df[['Player','5v5_TOI','5v5_xGF%']].sort_values(by='5v5_xGF%',ascending=asc).round(3)
            elif input.y() == 'TOI':
                df = df[['Player','5v5_TOI','5v5_xGF%']].sort_values(by='5v5_TOI',ascending=asc).round(3)
            else:
                df = df[['Player','5v5_TOI','5v5_xGF%']].sort_values(by=input.y(),ascending=asc).round(3)
        else:
            df = df[(df['Team']==input.x())&(df['ALL_TOI']>=input.toi())]
            if input.y() == "xGF%":
                df = df[['Player','ALL_TOI','ALL_xGF%']].sort_values(by='ALL_xGF%',ascending=asc).round(3)
            elif input.y() == 'TOI':
                df = df[['Player','ALL_TOI','ALL_xGF%']].sort_values(by='ALL_TOI',ascending=asc).round(3)
            else:
                df = df[['Player','ALL_TOI','ALL_xGF%']].sort_values(by=input.y(),ascending=asc).round(3)
        return df
    
    @output
    @render_widget
    def my_widget():
        df = pd.read_csv(onice)
        team = input.x()
        if input.strength()=="even":
            title_strength = "Even Strength"
            title_toi = "EV"
            x_col = "EV_xGF%"
            x_title = "Even Strength xGF%"
            color_for_chart = "EV_TOI"
            data = df[(df['Team']==team)&(df['EV_TOI']>=input.toi())]
        elif input.strength()=="_5v5":
            title_strength="5v5"
            title_toi="5v5"
            x_col = "5v5_xGF%"
            x_title = "5v5 xGF%"
            color_for_chart="5v5_TOI"
            data = df[(df['Team']==team)&(df['5v5_TOI']>=input.toi())]
        else:
            title_strength="All Situation"
            title_toi="All"
            x_col = "ALL_xGF%"
            x_title = "All Situation xGF%"
            color_for_chart="ALL_TOI"
            data = df[(df['Team']==team)&(df['ALL_TOI']>=input.toi())]
        data = data.sort_values(by=x_col,ascending=True)
        data['str'] = data[x_col].round(4)
        data['str'] = data['str'].map('{:,.2f}%'.format)
        color_discrete_sequence = ['#617296']*len(data)
        fig = px.bar(data, x=x_col, y="Player",text=('str'),height=1050,width=1050,template="plotly_dark",color=color_for_chart,color_continuous_scale=["#ffffff","#195293"])
        fig.update_layout(plot_bgcolor="#222222",paper_bgcolor="#222222")
        fig.update_traces(marker_line_color='#FFFFFF',
               marker_line_width=1.5)
        fig.update_layout(
            title=(input.x()+ " Skaters "+ title_strength +" On-Ice xGF%<br>"+
            "<i>2023-24 NHL Regular Season</i><br>"+
            "<i>Minimum " + str(input.toi()) + " " + title_toi + " TOI</i>"),
            margin=dict(r=20, l=40, b=100, t=90),)
        fig.update_xaxes(range=[0, 100])
        fig.update_xaxes(tickvals=[0,25,50,75,100],ticktext=['0%','25%','50%','75%','100%'])
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
        fig.update_layout(xaxis_title=x_title)
        return fig
    
    @reactive.Effect
    def _():
        val = input.quant()

        if input.strength()=="even":
            calc = "EV_TOI"
        elif input.strength()=="_5v5":
            calc = "5v5_TOI"
        else:
            calc = "ALL_TOI"

        if val == "_25":
           q= round(df[calc].quantile(.25),1)
        elif val == "_50":
            q= round(df[calc].quantile(.5),1)
        elif val == "_75":
            q=round(df[calc].quantile(.75),1)
        else:
            q=0
        ui.update_slider(
            "toi", value=q
        )
    
    @reactive.Effect
    def _2():
        btn = input.btn()
        if btn % 2 == 1:
            tab = ui.output_table("table")
            ui.insert_ui(
                ui.div({"id": "inserted-slider"},ui.tags.h5("Sort Table by", class_="app-heading"),ui.input_select("y","",{"Player":"Player","TOI":"TOI","xGF%":"xGF%",}),
            ui.input_radio_buttons(
        "z", "", {"F": "High to Low", "T": "Low to High"}
    ),ui.output_table("table")),
                selector="#main-content",
                where="beforeEnd",
            )
        elif btn > 0:
            ui.remove_ui("#inserted-slider")

on_ice_xgfp = App(ui.page_fluid(
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
        ),
        ui.nav_menu(
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
        ),
        ui.nav_control(
             ui.a(
                "About",
                href="about/"
            ),
        )),ui.row(
            ui.column(3,ui.tags.br(),ui.tags.h2("On-Ice xGF%"),ui.tags.h5("Team", class_="app-heading"),
            ui.input_select("x", "", {"ANA": "Anaheim Ducks",
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
            "WPG": "Winnipeg Jets"}),ui.tags.h5("Strength", class_="app-heading"),ui.input_select("strength", "",{'even':"Even",'_5v5':"5v5",'All':"All Strengths"}),
                                      ui.tags.h5("Minimum TOI", class_="app-heading"),
            ui.input_slider("toi", "", min=0, max=round(df['ALL_TOI'].max(),0),  value=round(df['EV_TOI'].quantile(.25),1)),ui.tags.h5("TOI Percentile (among all NHL skaters)", class_="app-heading"),ui.input_radio_buttons(
        "quant",
        "",
        {
            "_25": "Top 75%",
            "_50": "Top 50%",
            "_75": "Top 25%",
        },
    ),ui.input_action_button("btn", "Toggle Table"),ui.div({"id":"main-content"}),),
    ui.column(9,output_widget("my_widget")
    )),)),server)