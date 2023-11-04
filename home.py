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
        )),ui.tags.br(),ui.tags.h5("Welcome to Stats By Zach!"),ui.tags.h6("The 2023-24 NHL regular season is here, and the StatsByZach website is officially up and running for it! As I've state before, this website is still a work in progress, with lots of work to be done in terms of styling and compatibility especially. Along with that, I am focusing on finding a new hosting solution, adding more charts, and some prerformace enhancements as well. Thank you for paying the site a visit, and I do hope you can use my data to better understand the NHL. The website gets updated daily, and I try to make improvements on a regular basis, so please do visit the site often, and feel free to reach out to me on Twitter @StatsByZach for any feedback or suggestions. Enjoy the site, and happy hockey season!"))), None)