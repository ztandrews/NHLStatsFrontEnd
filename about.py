##### about.py #####
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
about = App(ui.page_fluid(
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
                href="kater-xg-percentages/"
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
        )),ui.tags.br(),ui.tags.h2("About"),ui.tags.h6("This section of the site is under construction. Eventually, this will have some general explinations on my xG model, the charts I make, and a glossary. I'll hopefully have this finished in the very near future!"),
        ui.tags.h5("Coming Soon"),("This site, as mentioned in it's very early stages. I wanted to use this section to highlight features that will be added soon to the site:"),ui.tags.ul(ui.tags.li("Data from all seasons dating back to 2007"),
        ui.tags.li("Ability to see stats from more strengths (5v5, All Situation, 5v5, 5v4, 5v3, etc.)"),
        ui.tags.li("More stat options for each chart (Corsi, Fenwick, etc.)"),
        ui.tags.li("Mobile friendly UI"),
        ui.tags.li("Glossary to help explain stats"),
        ui.tags.li("Article section primarily to do write ups about my xG model")),ui.tags.h6("These features have no set date to be released, but I think it'll be a long process that could stretch throughout the whole season. I try to work on the site as much as I can, so hopefully with that I can roll out these features fast."))), None)