import os
import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
# load all environment variable
TOKEN = os.getenv('DISCORD_TOKEN')
# get discord token
bot = commands.Bot(command_prefix='!', help_command=None)
# set up bot
bot.remove_command('help')

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f'cogs.{file[:-3]}')
#         load all commands from cog folder

bot.run(TOKEN)
# run bot
