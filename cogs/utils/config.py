import discord
from discord.ext.commands import Bot
from discord.ext import commands
import datetime
import time
import random
import configparser



def settings(section):
        config = configparser.ConfigParser()
        config.read_file(open('cogs/utils/config.ini'))
        dict1 = {}
        options = config.options(section)
        for option in options:
            try:
                dict1[option] = config.get(section, option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

