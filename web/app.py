from flask import Flask, render_template
import redis, os, re
from urllib import parse
from blaseball_stlats_tlracker import Player, getPlayerStatsByName

def _getScaling():
    scaling = {}

    with open('item_scaling.txt', 'r') as f:
        lines = f.readlines()

        # We add an extra '0' to the start of the list to make item qtys align with indices

        # Hot Dogs
        scaling['hotdogs'] = ['0'] + lines[0].strip().split(',')
        scaling['hotdogs'] = [int(i) for i in scaling['hotdogs']]

        # Sunflower Seeds
        scaling['sunflowerseeds'] = ['0'] + lines[1].strip().split(',')
        scaling['sunflowerseeds'] = [int(i) for i in scaling['sunflowerseeds']]

        # Pickles
        scaling['pickles'] = ['0'] + lines[2].strip().split(',')
        scaling['pickles'] = [int(i) for i in scaling['pickles']]

    return scaling

#############
##| Flask |##
#############
bst_frontend = Flask(__name__)
bst_frontend.config['APPLICATION_ROOT'] = '/app/web'  # Set root of webserver


@bst_frontend.route("/")
def index():

    # Read list of batter names from file
    with open('../common/players_batters.txt') as f:
        batterNames = f.readlines()
        batterNames = [name.strip() for name in batterNames]

    # Read list of pitcher names from file
    with open('../common/players_pitchers.txt') as f:
        pitcherNames = f.readlines()
        pitcherNames = [name.strip() for name in pitcherNames]

    ## TODO: Split into two pages, one for batters and one for pitchers?
    names = batterNames  ## TEMP

    players = getPlayerStatsByName(names, 'batter')


    scaling = _getScaling()
    item_counts = {'hotdogs': 1, 'sunflowerseeds': 1, 'pickles': 1}

    player_base_returns = {}
    for player in players:
        return_hotdogs = scaling['hotdogs'][item_counts['hotdogs']] * player.home_runs
        return_sunflowerseeds = scaling['sunflowerseeds'][item_counts['sunflowerseeds']] * player.hits
        return_pickles = scaling['pickles'][item_counts['pickles']] * player.stolen_bases

        player_base_returns[player.name] = round(return_hotdogs + return_sunflowerseeds + return_pickles)


    # ## HACK: Format player data manually
    # players_formatted = []
    # for player in players:
    #     players_formatted.append(
    #         {
    #             'name': player.name,
    #             'team_location': player.team_location,
    #             'team_nickname': player.team_nickname,
    #             'team_emoji': player.team_emoji,
    #             'hits': int(player.hits),
    #             'home_runs': int(player.home_runs),
    #             'stolen_bases': int(player.stolen_bases),
    #             'multiplier': int(player.multiplier)
    #         }
    #     )

    ## TEST Render HTML
    return render_template(
        "index.html",
        players=players,
        player_base_returns=player_base_returns,  ## TODO: Format decimal numbers properly first
    )


if __name__ == "__main__":
    bst_frontend.run()
