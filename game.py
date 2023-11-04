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
from scipy.interpolate import interp1d
import plotly.graph_objects as go
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
        #This is how it woks. Neat! Woooo!
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
            strength_str = "All"
        elif input.strength() =="Even":
            gi = gi[(gi['Strength_Mapped']=="even")]
            strength_str = "EV"
        else:
            gi = gi[(gi['homeSkatersOnIce']==5)&(gi['awaySkatersOnIce']==5)]
            strength_str = "5v5"
        if input.period()=="All":
            gi=gi
            title_p=""
        elif input.period() == "OT":
            gi = gi[gi['Period']>3]
            title_p = " OT"
        else:
            gi = gi[gi['Period']==int(input.period())]
            title_p = " Period "+str(input.period())
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
        #plt.title(away_team+" @ "+home_team+"\n"+date+"\nAll Unblocked Shot Attempts\nStrength: "+strength_str+title_p,color= 'white',size=12)
        plt.title(away_team+" @ "+home_team+" - "+date+'\n'+strength_str+title_p+" Unblocked Shot Attempts",color="white")
        plt.text(55,44,home_team+"\n"+str(round(home_shots['xG'].sum(),3))+" xG",color="white",horizontalalignment='center',size=12)
        plt.text(-55,44,away_team+"\n"+str(round(away_shots['xG'].sum(),3))+" xG",color="white",horizontalalignment='center',size=12)
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
        if input.strength_for_bars()=="even":
            xgf = "EV_xGF"
            xga = "EV_xGA"
            xgfp = "EV_xGF%"
            toi = "EV_TOI"
            title = "EV"
            x_title = "Even Strength xGF%"
        elif input.strength_for_bars()=="_5v5":
            xgf = "5v5_xGF"
            xga = "5v5_xGA"
            toi = "5v5_TOI"
            title = "5v5"
            x_title = "5v5 xGF%"
        else:
            xgf = "ALL_xGF"
            xga = "ALL_xGA"
            toi = "ALL_TOI"
            title = "All"
            x_title = "All Situation xGF%"
        data['xGF%'] = data[xgf]/(data[xgf]+data[xga])*100
        data = data.sort_values(by=['xGF%'])
        data = data[data['xGF%']>0]
        data['xGF%_str'] = data['xGF%'].round(4)
        data['xGF%_str']  = data['xGF%_str'] .map('{:,.2f}%'.format)
        fig = px.bar(data, x='xGF%', y='Player',text=('xGF%_str'),
             color=toi,color_continuous_scale=px.colors.sequential.Oryel,template="plotly_dark",height=750,width=750,
            )
        fig.update_layout(plot_bgcolor="#222222",paper_bgcolor="#222222")
        fig.update_traces(marker_line_color='#FFFFFF',
               marker_line_width=1.5)
        fig.update_layout(
            title=(home_team + " Skaters "+ title + " On-Ice xGF%<br>"+away_team +" @ "+home_team+"<br>"+date),margin=dict(r=20, l=40, b=100, t=90))
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
        fig.update_layout(xaxis_title=x_title)
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
        if input.strength_for_bars()=="even":
            xgf = "EV_xGF"
            xga = "EV_xGA"
            xgfp = "EV_xGF%"
            toi = "EV_TOI"
            title = "EV"
            x_title = "Even Strength xGF%"
        elif input.strength_for_bars()=="_5v5":
            xgf = "5v5_xGF"
            xga = "5v5_xGA"
            toi = "5v5_TOI"
            title = "5v5"
            x_title = "5v5 xGF%"
        else:
            xgf = "ALL_xGF"
            xga = "ALL_xGA"
            toi = "ALL_TOI"
            title = "All"
            x_title = "All Situation xGF%"
        data['xGF%'] = data[xgf]/(data[xgf]+data[xga])*100
        data = data.sort_values(by=['xGF%'])
        data = data[data['xGF%']>0]
        data['xGF%_str'] = data['xGF%'].round(4)
        data['xGF%_str']  = data['xGF%_str'] .map('{:,.2f}%'.format)
        fig = px.bar(data, x='xGF%', y='Player',text=('xGF%_str'),
             color=toi,color_continuous_scale=px.colors.sequential.Oryel,template="plotly_dark",height=750,width=750,
            )
        fig.update_layout(plot_bgcolor="#222222",paper_bgcolor="#222222")
        fig.update_traces(marker_line_color='#FFFFFF',
               marker_line_width=1.5)
        fig.update_layout(
             title=(away_team + " Skaters "+ title + " On-Ice xGF%<br>"+away_team +" @ "+home_team+"<br>"+date),margin=dict(r=20, l=40, b=100, t=90))
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
        fig.update_layout(xaxis_title=x_title)
        return fig
    
    @output
    @render_widget
    def my_widget3():
        gi = game_shots
        gi = gi[gi['Game_Id']==int(game_id)]
        if input.strength() == "All":
            gi = gi
            strength_str = "All Situations"
        elif input.strength() =="Even":
            gi = gi[(gi['Strength_Mapped']=="even")]
            strength_str = "Even Strength"
        else:
            gi = gi[(gi['homeSkatersOnIce']==5)&(gi['awaySkatersOnIce']==5)]
            strength_str = "5v5"
        if input.period()=="All":
            gi=gi
            title_p=""
        elif input.period() == "OT":
            gi = gi[gi['Period']>3]
            title_p = " OT"
        else:
            gi = gi[gi['Period']==int(input.period())]
            title_p = " Period "+str(input.period())
        away_team = gi['Away_Team'].tolist()[0]
        home_team = gi['Home_Team'].tolist()[0]
        date = gi["Date"].tolist()[0]
        gi = gi.reset_index()
        gi['xCordAdjusted'] = np.where(gi['isHomeTeam']==0,gi['xCordAdjusted']*-1,gi['xCordAdjusted'])
        gi['yCordAdjusted'] = np.where(gi['isHomeTeam']==0,gi['yCordAdjusted']*-1,gi['yCordAdjusted'])
        home_shots = gi[(gi['Ev_Team']==home_team)]
        away_shots = gi[(gi['Ev_Team']==away_team)]
        home_xg = round(home_shots['xG'].sum(),3)
        away_xg = round(away_shots['xG'].sum(),3)
        gi = gi.rename(columns={"p1_name":"Shooter"})
        fig = px.scatter(gi,'xCordAdjusted','yCordAdjusted',size='xG',color="Event",color_discrete_map={'MISS':"#ff7575",'GOAL':"#81ff75",'SHOT':"#ffd375"},hover_data=['Shooter','xG','Event','Period','goalieAgainst'])
        fig.add_shape(type="rect",
            x0=-100, y0=-45, x1=100, y1=45,
            line=dict(
                color="#222222",
                width=2,
            ),
            fillcolor="#222222",
        )
        fig.add_shape(type="line",
                    x0=100, 
                    y0=-17, 
                    x1=100, 
                    y1=17,line=dict(color="#FFFFFF",width=5))
        fig.add_shape(type="line",
                    x0=-70, 
                    y0=45, 
                    x1=70, 
                    y1=45,line=dict(color="#FFFFFF",width=5))

        fig.add_shape(type="circle",
            xref="x", yref="y",
            x0=-40, y0=10, x1=-100, y1=-45,
            line=dict(color="#FFFFFF",width=5),
        )
        fig.add_shape(type="circle",
            xref="x", yref="y",
            x0=40, y0=-10, x1=100, y1=45,
            line=dict(color="#FFFFFF",width=5)),

        fig.add_shape(type="circle",
            xref="x", yref="y",
            x0=-40, y0=-10, x1=-100, y1=45,
            line=dict(color="#FFFFFF",width=5)),

        fig.add_shape(type="circle",
            xref="x", yref="y",
            x0=40, y0=10, x1=100, y1=-45,
            line=dict(color="#FFFFFF",width=5)),

        fig.add_shape(type="rect",
            x0=-99.5, y0=-18, x1=-30, y1=18,
            line=dict(
                color="#222222",
                width=2,
            ),
            fillcolor="#222222",
        )

        fig.add_shape(type="rect",
            x0=-70, y0=-44.5, x1=-30, y1=44.5,
            line=dict(
                color="#222222",
                width=2,
            ),
            fillcolor="#222222",
        )

        fig.add_shape(type="rect",
            x0=99.5, y0=-18, x1=30, y1=18,
            line=dict(
                color="#222222",
                width=2,
            ),
            fillcolor="#222222",
        )

        fig.add_shape(type="rect",
            x0=70, y0=-44.5, x1=30, y1=44.5,
            line=dict(
                color="#222222",
                width=2,
            ),
            fillcolor="#222222",
        )



        fig.add_shape(type="line",
                    x0=-70, 
                    y0=-45, 
                    x1=70, 
                    y1=-45,line=dict(color="#FFFFFF",width=5))
        fig.add_shape(type="line",
                    x0=-100, 
                    y0=-17, 
                    x1=-100, 
                    y1=17,line=dict(color="#FFFFFF",width=5))
        fig.add_shape(type="line",
                    x0=0, 
                    y0=-44.9, 
                    x1=0, 
                    y1=44.9,line=dict(color="#c76969",width=5))
        fig.add_shape(type="line",
                    x0=89, 
                    y0=-38.1, 
                    x1=89, 
                    y1=38.1,line=dict(color="#c76969",width=4))
        fig.add_shape(type="line",
                    x0=25, 
                    y0=-44.7, 
                    x1=25, 
                    y1=44.7,line=dict(color="#6987c7",width=5))
        fig.add_shape(type="line",
                    x0=-25, 
                    y0=-44.7, 
                    x1=-25, 
                    y1=44.7,line=dict(color="#6987c7",width=5))

        fig.add_shape(type="circle",
            xref="x", yref="y",
            x0=-15, y0=-15, x1=15, y1=15,
            line=dict(color="#6998c7",width=4),
        )
        fig.add_shape(type="circle",
            xref="x", yref="y",
            x0=53, y0=7, x1=83, y1=37,
            line=dict(color="#c76969",width=4),
        )
        fig.add_shape(type="circle",
            xref="x", yref="y",
            x0=-53, y0=7, x1=-83, y1=37,
            line=dict(color="#c76969",width=4),
        )
        fig.add_shape(type="circle",
            xref="x", yref="y",
            x0=-53, y0=-7, x1=-83, y1=-37,
            line=dict(color="#c76969",width=4),
        )
        fig.add_shape(type="circle",
            xref="x", yref="y",
            x0=53, y0=-7, x1=83, y1=-37,
            line=dict(color="#c76969",width=4),
        )
        fig.add_shape(type="line",
                    x0=-89, 
                    y0=-38.1, 
                    x1=-89, 
                    y1=38.1,line=dict(color="#c76969",width=4))
        fig.add_shape(type="line",
                    x0=-89, 
                    y0=-3, 
                    x1=-89, 
                    y1=3,line=dict(color="#FFFFFF",width=5))
        fig.add_shape(type="line",
                    x0=89, 
                    y0=-3, 
                    x1=89, 
                    y1=3,line=dict(color="#FFFFFF",width=5))

        fig.update_layout(xaxis=dict(showgrid=False,zeroline=False,visible= False),
                    yaxis=dict(showgrid=False,zeroline=False,visible= False),
                        width=1400,height=630
        )
        fig.update_layout(plot_bgcolor='#222222',
                                        paper_bgcolor='#222222',)
        fig.update_layout(title_text=away_team+' @ '+ home_team +' - '+ date +' <br>All Unblocked Shot Attempts - '+strength_str + title_p, title_x=0.5)
        fig.update_layout(
            font_color="white",)
        # Create custom shapes for the points
        shots_list = home_shots['level_0'].to_list()
        for s in shots_list:
            xc=home_shots.loc[home_shots['level_0']==s]['xCordAdjusted'].tolist()[0]
            yc=home_shots.loc[home_shots['level_0']==s]['yCordAdjusted'].tolist()[0]
            xg = home_shots.loc[home_shots['level_0']==s]['xG'].tolist()[0]
            t = home_shots.loc[home_shots['level_0']==s]['Event'].tolist()[0]
            if t=="MISS":
                c = "#fa5f5f"
            elif t=='SHOT':
                c="#fad85f"
            else:
                c="#8dfa5f"
            if xg < .03:
                mul = 25
            elif xg >=.03 and xg < .07:
                mul = 23
            elif xg >= .07 and xg < .11:
                mul = 20
            elif xg >= .11 and xg < .15:
                mul = 17
            else:
                mul = 7
            fig.add_shape(
                type='circle',
                x0=xc - xg*mul,
                y0=yc - xg*mul,
                x1=xc + xg*mul,
                y1=yc + xg*mul,
                fillcolor=c,
                opacity=1,
                line=dict(color="#FFFFFF",width=1)
            )
        # Create custom shapes for the points
        shots_list = away_shots['level_0'].to_list()
        for s in shots_list:
            xc=away_shots.loc[away_shots['level_0']==s]['xCordAdjusted'].tolist()[0]
            yc=away_shots.loc[away_shots['level_0']==s]['yCordAdjusted'].tolist()[0]
            xg = away_shots.loc[away_shots['level_0']==s]['xG'].tolist()[0]
            t = away_shots.loc[away_shots['level_0']==s]['Event'].tolist()[0]
            if t=="MISS":
                c = "#fa5f5f"
            elif t=='SHOT':
                c="#fad85f"
            else:
                c="#8dfa5f"
            if xg < .03:
                mul = 25
            elif xg >=.03 and xg < .07:
                mul = 23
            elif xg >= .07 and xg < .11:
                mul = 20
            elif xg >= .11 and xg < .15:
                mul = 17
            else:
                mul = 7
            fig.add_shape(
                type='circle',
                x0=xc - xg*mul,
                y0=yc - xg*mul,
                x1=xc + xg*mul,
                y1=yc + xg*mul,
                fillcolor=c,
                opacity=1,
                line=dict(color="#FFFFFF",width=1)
            )
        fig.add_annotation(
            text = ("Data: @StatsByZach on Twitter")
            , showarrow=False
            , x = .79
            , y = -.03
            , xref='paper'
            , yref='paper' 
            , xanchor='left'
            , yanchor='bottom'
            , xshift=-1
            , yshift=-5
            , font=dict(size=11, color="white")
            , align="left"
        )
        fig.add_annotation(
            text = (home_team + "<br>"+str(home_xg)+" xG")
            , showarrow=False
            , x = .80
            , y = 1.02
            , xref='paper'
            , yref='paper' 
            , xanchor='left'
            , yanchor='bottom'
            , xshift=-1
            , yshift=-5
            , font=dict(size=15, color="white")
            , align="center"
        )
        fig.add_annotation(
            text = (away_team+"<br>"+str(away_xg)+" xG")
            , showarrow=False
            , x = .13
            , y = 1.02
            , xref='paper'
            , yref='paper' 
            , xanchor='left'
            , yanchor='bottom'
            , xshift=-1
            , yshift=-5
            , font=dict(size=15, color="white")
            , align="center"
        )
        
        return fig
    @output
    @render_widget
    def xg_chart():
        game = game_shots
        game = game[game['Game_Id']==int(game_id)]
        away = game['Away_Team'].tolist()[0]
        home = game['Home_Team'].tolist()[0]
        f = game[game['Ev_Team']==home]
        s = game[game['Ev_Team']==away]
        date = game['Date'].tolist()[0]
        f['cxG'] = f['xG'].cumsum()
        s['cxG'] = s['xG'].cumsum()
        fa = f['gameSeconds'].tolist()
        if max(game['gameSeconds'].tolist()) > 3600:
            max_seconds = max(game['gameSeconds'].tolist())+1
        else:
            max_seconds=3600
        fa.append(max_seconds)
        fa.insert(0,0)
        fx = f['cxG'].tolist()
        fx.insert(0,0)
        fx.append(fx[-1])
        sa = s['gameSeconds'].tolist()
        sa.append(max_seconds)
        sa.insert(0,0)
        sx = s['cxG'].tolist()
        sx.insert(0,0)
        sx.append(sx[-1])
        import numpy as np
        from scipy.interpolate import interp1d
        import plotly.graph_objects as go

        # Define colors at the top
        TEAM1_COLOR = '#EBEBD3'
        TEAM2_COLOR = '#F95738'
        FILL_COLOR_TEAM1 = '#EBEBD3'  # Corresponding fill color for Team 1
        FILL_COLOR_TEAM2 = '#F95738'  # Corresponding fill color for Team 2

        # Create a new time array with 1-second intervals
        full_time = np.arange(0, max_seconds, 1)  # 60 minutes with 1-second intervals

        # Interpolate both teams' data to this new time array
        f_interp = interp1d(fa, fx, kind='linear', bounds_error=False, fill_value=(fx[0], fx[-1]))
        s_interp = interp1d(sa, sx, kind='linear', bounds_error=False, fill_value=(sx[0], sx[-1]))

        fx_full = f_interp(full_time)
        sx_full = s_interp(full_time)

        fig = go.Figure()

        # Find intersections
        intersections = np.where(np.diff(np.sign(fx_full - sx_full)))[0]

        # Initialize starting index
        start = 0

        # Loop through intersections and plot segments
        for idx in intersections:
            if fx_full[idx] > sx_full[idx]:
                fillcolor = FILL_COLOR_TEAM1
            else:
                fillcolor = FILL_COLOR_TEAM2

            fig.add_trace(go.Scatter(x=full_time[start:idx+2], y=fx_full[start:idx+2], mode='lines', line=dict(color=TEAM1_COLOR), showlegend=False))
            fig.add_trace(go.Scatter(x=full_time[start:idx+2], y=sx_full[start:idx+2], mode='lines', line=dict(color=TEAM2_COLOR),
                                    fill='tonexty', fillcolor=fillcolor, showlegend=False))
            start = idx + 1

        # Handle the last segment
        if fx_full[start] > sx_full[start]:
            fillcolor = FILL_COLOR_TEAM1
        else:
            fillcolor = FILL_COLOR_TEAM2

        fig.add_trace(go.Scatter(x=full_time[start:], y=fx_full[start:], mode='lines', line=dict(color=TEAM1_COLOR), showlegend=False))
        fig.add_trace(go.Scatter(x=full_time[start:], y=sx_full[start:], mode='lines', line=dict(color=TEAM2_COLOR),
                                fill='tonexty', fillcolor=fillcolor, showlegend=False))

        # Update layout for axis labels, theme, and figure dimensions
        fig.update_layout(
            title="Cumulative xG<br>"+away+  " @ " + home +" - " + date + "<br>Strength: All situations",
            xaxis_title="Time",
            xaxis_showgrid=False,  # Hide x-axis grid lines
            yaxis_title="xG",
            yaxis_showgrid=False,  # Hide y-axis grid lines
            template="plotly_dark",
            width=1400,
            height=700,
            plot_bgcolor="#222222",  # Set plot background color
            paper_bgcolor="#222222",
            xaxis_range=[0, 3600], 
            yaxis_range=[0, 5.5],
        )

        # Add legend entries
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color=TEAM1_COLOR), name=home))
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color=TEAM2_COLOR), name=away))
        if max_seconds==3600:
            fig.update_layout(
                xaxis_range=[0, 3600],
                xaxis=dict(
                    tickvals=[0,1200,2400,3600],  # positions of tick marks
                    ticktext=["0","20","40","60"]  # text to display at those positions
                )
            )
        else:
            fig.update_layout(
                xaxis_range=[0, max_seconds], 
                xaxis=dict(
                    tickvals=[0,1200,2400,3600,4800],  # positions of tick marks
                    ticktext=["0","20","40","60","80"]  # text to display at those positions
                )
            )
        fig.update_layout(hovermode=False)
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
              )),ui.row(ui.column(1),ui.column(11,output_widget("my_widget3"),output_widget("xg_chart"),ui.tags.br()),
    ),ui.row(ui.tags.h5("On-Ice xGF%'s"),ui.tags.h5("Strength", class_="app-heading"),ui.input_select("strength_for_bars", "",{'even':"Even",'_5v5':"5v5",'All':"All Situations"})),ui.row(ui.column(6,output_widget("my_widget2")),ui.column(6,output_widget("my_widget"))))),server)