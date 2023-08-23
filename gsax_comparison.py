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
        df['str'] = df['GSAx'].round(4)
        df['str'] = df['str'].map('{:,.3f}'.format)
        color_discrete_sequence = ['#617296']*len(df)
        #df = df[(df['Goalie']=="ILYA SOROKIN")|(df['Goalie']=="ADIN HILL")] 
        if len(list(input.x())) >=5:
            ui.update_selectize("x",choices=list(input.x()),selected=list(input.x()))
        else:
            ui.update_selectize("x",choices=choices,selected=list(input.x()))
        df = df[df['Goalie'].isin(list(input.x()))]
        df = df.sort_values(by='GSAx',ascending=False)
        seq = df['Color'].tolist()
        df = df.sort_values(by='GSAx',ascending=False)
        fig = px.bar(df, x="Goalie", y="GSAx",text=('str'),height=1050,width=750,template="plotly_dark",color='Goalie',color_discrete_sequence=seq,hover_name="Goalie",hover_data={"str":False,"Goalie":False,'Team':True})
        fig.update_layout(plot_bgcolor="#222222",paper_bgcolor="#222222")
        fig.update_traces(marker_line_color='#FFFFFF',
               marker_line_width=1.5)
        fig.update_layout(
            title=(input.y()+"<br>"+
                   "GSAx Comparison<br>"+
            "<i>2022-23 NHL Playoffs</i>"),
            margin=dict(r=20, l=40, b=100, t=90),)
        fig.add_annotation(
            text = ("Data: @StatsByZach on Twitter")
            , showarrow=False
            , x = .75
            , y = -.113
            , xref='paper'
            , yref='paper' 
            , xanchor='left'
            , yanchor='bottom'
            , xshift=-1
            , yshift=-5
            , font=dict(size=11, color="white")
            , align="left"
        )
        fig.update_traces(textfont_size=14)
        return fig

    @output
    @render.table
    def table():
        df = pd.read_csv(gsaxt)
        df = df[['Goalie','GSAx']]
        df = df.sort_values(by='GSAx',ascending=False)
        return df
    


gsax_comparison = App(ui.page_fluid(
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
    ui.column(3,ui.tags.br(),ui.tags.h2("GSAx Comparison"),
    ui.tags.h5("Select Up To 5 Goalies", class_="app-heading"),
    ui.input_selectize("x", "", choices, multiple = True),
    ui.tags.h5("Custom Chart Title (Optional):"),
    ui.input_text("y", "")
    ),
    ui.column(9,output_widget("my_widget")
    )),)),server)