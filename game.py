##### game.,py #####

# Import modules
from shiny import *
import shinyswatch
import plotly.express as px
from shinywidgets import output_widget, render_widget
import pandas as pd
from configure import base_url
import matplotlib.pyplot as plt
from hockey_rink import NHLRink
from matplotlib.lines import Line2D
import numpy as np
import plotly.express as px

# Paths to data
shots = "data/test_shots.csv"
info = "data/game_list.csv"
xg = "data/on_ice_xg_by_game.csv"
#data = pd.read_csv(shots)
def server(input,output,session):
    game_id = session.http_conn.path_params['game_id']
    game_shots = pd.read_csv(shots)
    game_info = pd.read_csv(info)
    xg_df = pd.read_csv(xg)
    @output
    @render.text
    def text():
        #t = session.__dir__()
        #This is how we can get the Game_Id that was passed in. Nice!
        t = session.http_conn.path_params['game_id']
        return t
    
    @output
    @render.text
    def game_info_teams():
        gi = game_info
        gi = gi[gi['Game_Id']==int(game_id)]
        away_team = gi['Away'].tolist()[0]
        home_team = gi['Home'].tolist()[0]
        date = gi['Date'].tolist()[0]
        string = away_team + " @ " + home_team
        return string
    
    @output
    @render.text
    def game_info_date():
        gi = game_info
        gi = gi[gi['Game_Id']==int(game_id)]
        date = gi['Date'].tolist()[0]
        string = date
        return string
    
    @output
    @render.table
    def table():
        df = game_shots
        df = df[df['Game_Id']==int(game_id)]
        df = df[df['Event']=="GOAL"][['p1_name','Event','xG']]
        return df
    
    @reactive.Effect
    def _():
        gi = game_shots
        gi = gi[gi['Game_Id']==int(game_id)]
        max_p = gi['Period'].max()
        if max_p >3:
            choices = ["All",1,2,3,"OT"]
        else:
            choices = ["All",1,2,3]
        ui.update_select(
            "period",
            choices=choices
        )


    @output
    @render.plot
    def a_scatter_plot():
        gi = game_shots
        gi = gi[gi['Game_Id']==int(game_id)]
        if input.strength() == "All":
            gi = gi
            strength_str = "All Situations"
        elif input.strength() =="Even":
            gi = gi[(gi['Strength_Mapped']=="even")]
            strength_str = "Even"
        else:
            gi = gi[(gi['homeSkatersOnIce']==5)&(gi['awaySkatersOnIce']==5)]
            strength_str = "5v5"
        if input.period()=="All":
            gi=gi
            title_p=""
        elif input.period() == "OT":
            gi = gi[gi['Period']>3]
            title_p = "\nPeriod: OT"
        else:
            gi = gi[gi['Period']==int(input.period())]
            title_p = "\nPeriod: " + str(input.period())
        away_team = gi['Away_Team'].tolist()[0]
        home_team = gi['Home_Team'].tolist()[0]
        home_shots = gi[(gi['Ev_Team']==home_team)]
        away_shots = gi[(gi['Ev_Team']==away_team)]
        date = gi["Date"].tolist()[0]
        nhl_rink = NHLRink(rotation=90)
        fig=plt.figure(figsize=(100,100))
        plt.xlim([0,100])
        plt.ylim([-42.5, 42.5])
        rink = NHLRink()
        rink.draw()
        plt.scatter((home_shots['xCordAdjusted']),(home_shots['yCordAdjusted']), (home_shots['xG']*1500) ,c= np.where((home_shots['Event']=="GOAL"),'green',np.where((home_shots['Event']=="SHOT"),'orange','red')),zorder=10,edgecolors='black',linewidth=1)
        plt.scatter((away_shots['xCordAdjusted']*-1),(away_shots['yCordAdjusted']*-1), (away_shots['xG']*1500) ,c= np.where((away_shots['Event']=="GOAL"),'green',np.where((away_shots['Event']=="SHOT"),'orange','red')),zorder=10,edgecolors='black',linewidth=1)         
        fig.patch.set_facecolor('#222222')
        plt.title(away_team+" @ "+home_team+"\n"+date+"\nAll Unblocked Shot Attempts\nStrength: "+strength_str+title_p,color= 'white',size=12)
        plt.text(55,44,home_team+"\n"+str(round(home_shots['xG'].sum(),3))+" xG",color="white",horizontalalignment='center',size=10)
        plt.text(-55,44,away_team+"\n"+str(round(away_shots['xG'].sum(),3))+" xG",color="white",horizontalalignment='center',size=10)
        custom_points = [Line2D([0], [0], marker='o', color='w', label='shot', markerfacecolor='orange', markersize=15),
                Line2D([0], [0], marker='o', color='w', label='miss', markerfacecolor='red', markersize=15),
                Line2D([0], [0], marker='o', color='w', label='goal', markerfacecolor='green', markersize=15)]

        return fig
    
    @output
    @render_widget
    def my_widget():
        gi = game_info
        gi = gi[gi['Game_Id']==int(game_id)]
        away_team = gi['Away'].tolist()[0]
        home_team = gi['Home'].tolist()[0]
        date = gi['Date'].tolist()[0]
        data = xg_df
        data = data[data['Game_Id']==int(game_id)]
        data = data[data['Team']==home_team]
        data['xGF%'] = data['EV_xGF']/(data['EV_xGF']+data['EV_xGA'])*100
        data = data.sort_values(by=['xGF%'])
        data['xGF%_str'] = data['xGF%'].round(4)
        data['xGF%_str']  = data['xGF%_str'] .map('{:,.2f}%'.format)
        fig = px.bar(data, x='xGF%', y='Player',text=('xGF%_str'),
             color='EV_TOI',color_continuous_scale=px.colors.sequential.Oryel,template="plotly_dark",height=850,width=850,
            )
        fig.update_layout(plot_bgcolor="#222222",paper_bgcolor="#222222")
        fig.update_traces(marker_line_color='#FFFFFF',
               marker_line_width=1.5)
        fig.update_layout(
            title=(home_team + " Skaters On-Ice xGF%<br>"+away_team +" @ "+home_team+", "+date+"<br><i>Strength: Even</i><br>"),margin=dict(r=20, l=40, b=100, t=90))
        fig.update_xaxes(range=[0, 100])
        fig.update_xaxes(tickvals=[0,25,50,75,100],ticktext=['0%','25%','50%','75%','100%'])
        fig.add_annotation(
            text = ("Data: @StatsByZach on Twitter")
            , showarrow=False
            , x = .70
            , y = -.06
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
    @render_widget
    def my_widget2():
        gi = game_info
        gi = gi[gi['Game_Id']==int(game_id)]
        away_team = gi['Away'].tolist()[0]
        home_team = gi['Home'].tolist()[0]
        date = gi['Date'].tolist()[0]
        data = xg_df
        data = data[data['Game_Id']==int(game_id)]
        data = data[data['Team']==away_team]
        data['xGF%'] = data['EV_xGF']/(data['EV_xGF']+data['EV_xGA'])*100
        data = data.sort_values(by=['xGF%'])
        data['xGF%_str'] = data['xGF%'].round(4)
        data['xGF%_str']  = data['xGF%_str'] .map('{:,.2f}%'.format)
        fig = px.bar(data, x='xGF%', y='Player',text=('xGF%_str'),
             color='EV_TOI',color_continuous_scale=px.colors.sequential.Oryel,template="plotly_dark",height=850,width=850,
            )
        fig.update_layout(plot_bgcolor="#222222",paper_bgcolor="#222222")
        fig.update_traces(marker_line_color='#FFFFFF',
               marker_line_width=1.5)
        fig.update_layout(
            title=(away_team + " Skaters On-Ice xGF%<br>"+away_team +" @ "+home_team+", "+date+"<br><i>Strength: Even</i><br>"),margin=dict(r=20, l=40, b=100, t=90))
        fig.update_xaxes(range=[0, 100])
        fig.update_xaxes(tickvals=[0,25,50,75,100],ticktext=['0%','25%','50%','75%','100%'])
        fig.add_annotation(
            text = ("Data: @StatsByZach on Twitter")
            , showarrow=False
            , x = .70
            , y = -.06
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
game = App(ui.page_fluid(
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
    ui.column(12,ui.tags.br(),ui.tags.h2(ui.output_text("game_info_teams")),ui.tags.h2(ui.output_text("game_info_date")),ui.tags.h5("Shot Map"),ui.tags.h5("Select strength"),ui.input_select("strength", "", ["All",'Even','5v5']),ui.tags.h5("Select period"),ui.input_select("period", "",["All",1,2,3] ),
              ui.output_plot("a_scatter_plot"),ui.tags.br()
    )),ui.row(ui.tags.h5("Even-Strength xGF%'s"),ui.column(6,output_widget("my_widget2")),ui.column(6,output_widget("my_widget"))))),server)