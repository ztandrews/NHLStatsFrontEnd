##### gsax_leaderboard.,py #####

# Import modules
from shiny import *
import shinyswatch
import plotly.express as px
from shinywidgets import output_widget, render_widget
import pandas as pd
from configure import base_url

# Paths to data
gsaxt = "data/total_gsax.csv"
data = pd.read_csv(gsaxt)
choices = data['Goalie'].value_counts().keys().sort_values().tolist()
def server(input,output,session):
    @output
    @render_widget
    def my_widget():
        df = pd.read_csv(gsaxt)
        if input.rev()==False:
            df = df.sort_values(by="GSAx",ascending=False)
            df = df[:input.size()]
            df = df.sort_values(by="GSAx",ascending=True)
            preface = "Top"
        else:
            df = df.sort_values(by="GSAx",ascending=True)
            df = df[:input.size()]
            df = df.sort_values(by="GSAx",ascending=False)
            preface = "Bottom"
        df['str'] = df['GSAx'].round(4)
        df['str'] = df['str'].map('{:,.3f}'.format)
        color_discrete_sequence = ['#617296']*len(df)
        fig = px.bar(df, x="GSAx", y="Goalie",text=('str'),height=1050,width=1050,template="plotly_dark",color_discrete_sequence=color_discrete_sequence,hover_name="Goalie",hover_data={"str":False,"Goalie":False})
        fig.update_layout(plot_bgcolor="#222222",paper_bgcolor="#222222")
        fig.update_traces(marker_line_color='#FFFFFF',
               marker_line_width=1.5)
        fig.update_layout(
            title=("GSAx Leaderboard<br>"+
                   preface+" " + str(input.size())+" Goalies <br>"+
            "<i>2022-23 NHL Playoffs</i>"),
            margin=dict(r=20, l=40, b=100, t=90),)
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

    @output
    @render.table
    def table():
        df = pd.read_csv(gsaxt)
        df = df[['Goalie','GSAx']]
        df = df.sort_values(by='GSAx',ascending=False)
        return df

gsax_leaderboard = App(ui.page_fluid(
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
        )),ui.row(
    ui.column(3,ui.tags.br(),ui.tags.h2("GSAx Leaderboard"),
    ui.tags.h5("Leaderboard Size", class_="app-heading"),
    ui.input_slider("size", "", min=1, max=len(choices), value=len(choices)),
    ui.tags.h5("Reverse Leaderboard", class_="app-heading"),
    ui.input_switch("rev", "", False),
    ),
    ui.column(9,output_widget("my_widget")
    )),)),server)