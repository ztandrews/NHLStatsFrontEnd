##### home.py #####
# Home page
# Zach Andrews

# Import modules
from shiny import *
import shinyswatch
import plotly.express as px
from shinywidgets import output_widget, render_widget
import pandas as pd
from configure import base_url

# Create app
home = App(ui.page_fluid(
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
    shinyswatch.theme.darkly(),ui.tags.h4("Stats By Zach"),
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
        )),ui.tags.br(),ui.tags.h5("Welcome to Stats By Zach!"),ui.tags.h6("This is my new website dedicated to making my charts and data easily accessible by the public. This site is still very much in it's beta stages, and will probably change hundreds of times throughout the off-season. This website is being built with Shiny for Python, which is a relatively new framework, so there will be a learning curve for me which could make the development take a good chunk of time. For now, enjoy the sections of the site that are running, and feel free to reach out with any questions! Also, I'll note that the data used on this site is only that of the 2022-23 NHL Playoffs. As the summer goes on, more options will be added to look at previous seasons and playoffs. I just wanted to release the site now to show the public what kind  of charts this site will feature in the future."))), None)