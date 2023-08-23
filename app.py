##### app.py #####
# Main shiny app
# Zach Andrews

#Import modules
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from shiny import App, ui
import shinyswatch

#Import pages
from home import home
from about import about
from gsax_timeline import gsax_timeline
from on_ice_xg_rates import on_ice_xg
from gsax_leaderboard import gsax_leaderboard
from on_ice_xgfp import on_ice_xgfp
from team_xg_rates import team_xg_rates
from gsax_comparison import gsax_comparison
from game import game
from games import games

# Create app
routes = [
    Mount('/home', app=home),
    Mount('/about', app=about),
    Mount('/gsax-timeline', app=gsax_timeline),
    Mount('/skater-xg-rates', app=on_ice_xg),
    Mount('/gsax-leaderboard', app=gsax_leaderboard),
    Mount('/skater-xg-percentages', app=on_ice_xgfp),
    Mount('/team-xg-rates', app=team_xg_rates),
    Mount('/gsax-comparison',app=gsax_comparison),
    Mount('/games',app=games),
    Mount('/game/{game_id}',app=game)
]

#Run App
app = Starlette(routes=routes)