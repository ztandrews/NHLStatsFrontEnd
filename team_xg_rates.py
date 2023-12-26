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
        
        if input.strength()=="even":
            if input.y() == "Team":
                df = df[['Team','EV_TOI','EV_xGF/60','EV_xGA/60']].sort_values(by='Team',ascending=asc).round(3)
            elif input.y() == 'xGF/60':
                df = df[['Team','EV_TOI','EV_xGF/60','EV_xGA/60']].sort_values(by='EV_xGF/60',ascending=asc).round(3)
            elif input.y() == 'xGA/60':
                df = df[['Team','EV_TOI','EV_xGF/60','EV_xGA/60']].sort_values(by='EV_xGA/60',ascending=asc).round(3)
            else:
                df = df[['Team','EV_TOI','EV_xGF/60','EV_xGA/60']].sort_values(by=input.y(),ascending=asc).round(3)
        elif input.strength()=="_5v5":
            if input.y() == "Team":
                df = df[['Team','5v5_TOI','5v5_xGF/60','5v5_xGA/60']].sort_values(by='Team',ascending=asc).round(3)
            elif input.y() == 'xGF/60':
                df = df[['Team','5v5_TOI','5v5_xGF/60','5v5_xGA/60']].sort_values(by='5v5_xGF/60',ascending=asc).round(3)
            elif input.y() == 'xGA/60':
                df = df[['Team','5v5_TOI','5v5_xGF/60','5v5_xGA/60']].sort_values(by='5v5_xGA/60',ascending=asc).round(3)
            else:
                df = df[['Team','5v5_TOI','5v5_xGF/60','5v5_xGA/60']].sort_values(by=input.y(),ascending=asc).round(3)
        else:
            if input.y() == "Team":
                df = df[['Team','ALL_TOI','ALL_xGF/60','ALL_xGA/60']].sort_values(by='Team',ascending=asc).round(3)
            elif input.y() == 'xGF/60':
                df = df[['Team','ALL_TOI','ALL_xGF/60','ALL_xGA/60']].sort_values(by='ALL_xGF/60',ascending=asc).round(3)
            elif input.y() == 'xGA/60':
                df = df[['Team','ALL_TOI','ALL_xGF/60','ALL_xGA/60']].sort_values(by='ALL_xGA/60',ascending=asc).round(3)
            else:
                df = df[['Team','ALL_TOI','ALL_xGF/60','ALL_xGA/60']].sort_values(by=input.y(),ascending=asc).round(3)
        return df
    
    @output
    @render_widget
    def my_widget():
        df = pd.read_csv(path)
        if input.strength()=="even":
            title_strength = "Even Strength"
            title_toi = "EV"
            x_col = "EV_xGF/60"
            y_col = "EV_xGA/60"
            x_title = "Even Strength xGF/60"
            y_title = "Even Strength xGA/60"
            color_for_chart = "EV_TOI"
        elif input.strength()=="_5v5":
            title_strength="5v5"
            title_toi="5v5"
            x_col = "5v5_xGF/60"
            y_col = "5v5_xGA/60"
            x_title = "5v5 xGF/60"
            y_title = "5v5 xGA/60"
            color_for_chart="5v5_TOI"
        else:
            title_strength="All Situation"
            title_toi="All"
            x_col = "ALL_xGF/60"
            y_col = "ALL_xGA/60"
            x_title = "All Situation xGF/60"
            y_title = "All Situation xGA/60"
            color_for_chart="ALL_TOI"
        fig = px.scatter(df, x_col, y_col,color=color_for_chart,template="plotly_dark",height=1050,width=1050,text='Team')
        fig.update_traces(textposition='top right',marker=dict(size=10))
        fig.update(layout_xaxis_range = [1.5,3.7])
        fig.update(layout_yaxis_range = [3.7,1.5])
        fig.update_traces(textfont_size=15)
        fig.add_vline(x=df[x_col].mean(), line_width=2, line_dash="dash", line_color="#617296")
        fig.add_hline(y=df[y_col].mean(), line_width=2, line_dash="dash", line_color="#617296")
        fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False,plot_bgcolor="#222222",paper_bgcolor="#222222")
        fig.update_layout(
            title=("Team " +title_strength + " xG Rates<br>"+
            "<i>2023-24 NHL Regular Season</i><br>"),
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
        fig.update_layout(xaxis_title=x_title)
        fig.update_layout(yaxis_title=y_title)
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
        )
        ),ui.row(
        ui.column(3,ui.tags.br(),ui.tags.h2("Team xG Rates"),ui.tags.h5("Strength", class_="app-heading"),ui.input_select("strength", "",{'even':"Even",'_5v5':"5v5",'All':"All Situations"}),ui.input_action_button("btn", "Toggle Table"),ui.div({"id":"main-content"},
            #ui.output_table("table"),
        )),
        ui.column(9,output_widget("my_widget"),#output_widget("it"),
        title="Stats By Zach",
    )))),server)
