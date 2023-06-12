######################################################
# Credit: from discox https://github.com/v1rbox/discox
# Original author: @imindMan, discord: imindMan#8536
# For more information about me: https://github.com/imindMan
# LICENSE: under AGPL v3.0
# Project name: slashcox, repo link: https://github.com/imindMan/slashcox
# Description: discox, but support slashing commands
#
#
#
#              ███         ████████            ████████          ███        ███
#             ███       ███                 ███        ███        ███      ███
#            ███       ███                 ███          ███        ███    ███
#           ███       ███                 ███            ███        ███  ███
#          ███       ███                 ███              ███        ██████
#         ███       ███                 ███                ███        ████
#        ███        ███                 ███                ███        ████
#       ███         ███                 ███                ███       ██████
#      ███           ███                 ███              ███       ███  ███
#     ███             ███                 ███            ███       ███    ███
#    ███               ███                 ███          ███       ███      ███
#   ███                   █████████           ██████████         ███        ███
#
#
# Discox is a general-purpose, free and open-source, multi-functionality and Virbox community's bot written in Python.
#
#
# It's kinda a very cool bot. But anyway, as a discox developer myself, I find that discox needs slashing commands.
# Drillenissen - the developers' leader of that project said "it limits the freedom", so anyway to satisfy my own interest.
# I'll make another alternative Discox called "Slashcox" (xsnowstorm came up with this name, his discord account: xsnowstorm#4883)
#
# This bot is very easy to setup. If you are a discox developer (or contributor of discox project), you'll know how to contribute to this
# immediately, because it's exactly the same as discox, except for the .env file, a little bit different (read the wiki for more details).
#
# Although its core is a clone of discox but support slashing commands, this "slashcox" will also have some of my interesting commands
# and utilities. Also, because it's slashing so it has some "new more modern vibe" comparing to its father discox.
#
# Hope you enjoy!
#                                           - imindMan
#

######################################################


#### IMPORT SOME NECESSARY LIBRARIES ###
import discord

from .base import Client, Tree
from .config import Config


def main():
    ### IMPORTANT VARIABLES ###
    config = Config()

    client = Client(intents=discord.Intents.default())
    tree = Tree(client)
    client.init_tree(tree)

    client.run(config.token)


if __name__ == "__main__":
    main()
