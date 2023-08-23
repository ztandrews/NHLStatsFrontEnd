##### team_xg_rates.py #####
# A program to display teams on-ice xG rates
# Zach Andrews

# Import modules
from shiny import *
import shinyswatch
import plotly.graph_objs as go
from shinywidgets import output_widget, register_widget, render_widget, bokeh_dependency
import pandas as pd
import plotly.express as px
from configure import base_url

path = "data/team_xg_rates.csv"

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
        df = df[['Team','EV_TOI','xGF/60','xGA/60']].sort_values(by=input.y(),ascending=asc).round(3)
        return df
    
    @output
    @render_widget
    def my_widget():
        df = pd.read_csv(path)
        fig = px.scatter(df, 'xGF/60', 'xGA/60',color="EV_TOI",template="plotly_dark",height=1050,width=1050,text='Team')
        fig.update_traces(textposition='top right',marker=dict(size=10))
        fig.update(layout_xaxis_range = [1.5,3.7])
        fig.update(layout_yaxis_range = [3.7,1.5])
        fig.update_traces(textfont_size=15)
        fig.add_vline(x=df['xGF/60'].mean(), line_width=2, line_dash="dash", line_color="#617296")
        fig.add_hline(y=df['xGA/60'].mean(), line_width=2, line_dash="dash", line_color="#617296")
        fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False,plot_bgcolor="#222222",paper_bgcolor="#222222")
        fig.update_layout(
            title=("Team Even-Strength xG Rates<br>"+
            "<i>2022-23 NHL Playoffs</i><br>"),
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
        btn = input.btn()
        if btn % 2 == 1:
            tab = ui.output_table("table")
            ui.insert_ui(
                ui.div({"id": "inserted-slider"},ui.tags.h5("Sort Table by", class_="app-heading"),ui.input_select("y","",{"Team":"Team","EV_TOI":"EV_TOI","xGF/60":"xGF/60","xGA/60":"xGA/60"}),
            ui.input_radio_buttons(
        "z", "", {"F": "High to Low", "T": "Low to High"}
    ),ui.output_table("table")),
                selector="#main-content",
                where="beforeEnd",
            )
        elif btn > 0:
            ui.remove_ui("#inserted-slider")

team_xg_rates = App(ui.page_fluid(
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
        ui.column(3,ui.tags.br(),ui.tags.h2("Team Even-Strength xG Rates"),ui.input_action_button("btn", "Toggle Table"),ui.div({"id":"main-content"},
            #ui.output_table("table"),
        )),
        ui.column(9,output_widget("my_widget"),#output_widget("it"),
        title="Stats By Zach",
    )))),server)
