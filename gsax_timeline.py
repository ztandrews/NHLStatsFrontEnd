##### gsax_timeline.py #####
# A program to visualize goalies GSAx throughout a season
# Zach Andrews

# Import modules
from shiny import *
import shinyswatch
import plotly.express as px
from shinywidgets import output_widget, render_widget
import pandas as pd
from configure import base_url

# Paths to data
gsaxd = "data/gsax_by_date.csv"
gsaxt = "data/total_gsax.csv"

# App
data = pd.read_csv(gsaxd)
choices = data['Goalie'].value_counts().keys().sort_values().tolist()
def server(input,output,session):
    @output
    @render_widget
    def my_widget():
        df = pd.read_csv(gsaxd)
        goalies = list(input.x())
        df = df[df['Goalie'].isin(goalies)]
        key = df[['Goalie','Team','Color']]
        a = df.groupby("Goalie").count()
        a = a.reset_index()
        l = a['Goalie'].tolist()
        seq = []
        for x in l:
            cmap = key[key['Goalie']==x]['Color'].tolist()[0]
            seq.append(str(cmap))
        df = df.sort_values(by=['Goalie','Date'])
        fig = px.line(df, x=input.y(), y="GSAx",color="Goalie",template="plotly_dark",color_discrete_sequence=seq,height=1050,width=1050)
        fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False,plot_bgcolor="#222222",paper_bgcolor="#222222")
        fig.update_traces(line=dict(width=5))
        fig.update_layout(
            title=("GSAx by "+input.y()+"<br>"+
            "<i>2023-24 NHL Regular Season</i>"),
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

    @output
    @render.table
    def table():
        df = pd.read_csv(gsaxt)
        if input.z() == "T":
            asc = True
        else:
            asc = False
        df = df[['Goalie','GSAx']]
        df = df[df['Goalie'].isin(list(input.x()))].sort_values(by=input.b(),ascending=asc)
        return df
    
    @reactive.Effect
    def _2():
        btn = input.btn()
        if btn % 2 == 1:
            tab = ui.output_table("table")
            ui.insert_ui(
                ui.div({"id": "inserted-slider"},ui.tags.h5("Sort Table by", class_="app-heading"),ui.input_select("b","",{"Goalie":"Goalie","GSAx":"GSAx"}),
            ui.input_radio_buttons(
        "z", "", {"F": "High to Low", "T": "Low to High"}
    ),ui.output_table("table")),
                selector="#main-content",
                where="beforeEnd",
            )
        elif btn > 0:
            ui.remove_ui("#inserted-slider")
gsax_timeline = App(ui.page_fluid(
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
    ui.column(3,ui.tags.br(),ui.tags.h2("GSAx Timeline Charts"),ui.tags.h5("Select a Goalie", class_="app-heading"),ui.input_selectize("x", "", choices, multiple = True),
              ui.tags.h5("X-Axis", class_="app-heading"), ui.input_radio_buttons(
        "y",
        "",
        {
            "Date":"Date",
            "Appearance Number": "Appearance Number",
        },
    ),ui.input_action_button("btn", "Toggle Table"),ui.div({"id":"main-content"}),
    #ui.tags.h5("Selected Goalies", class_="app-heading"),
    #ui.output_table("table")
    ),
    ui.column(9,output_widget("my_widget"))),)),server)