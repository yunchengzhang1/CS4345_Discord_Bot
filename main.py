import os
import discord
from dotenv import load_dotenv
from discord.ext import commands


# class customHelpCommand(commands.HelpCommand):
#     def __init__(self):
#         super.__init__()
#
#     async def send_bot_help(self, mapping):
#         for cog in mapping:
#             await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in mapping[cog]]}')
#
#     async def send_cog_help(self,cog):
#         await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in cog.get_commands()]}')
#
#     async def send_command_help(self, command):
#         await self.get_destination().send(command.name)

load_dotenv()
# load all environment variable
TOKEN = os.getenv('DISCORD_TOKEN')
# get discord token
bot = commands.Bot(command_prefix='!', help_command=None)
# set up bot

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f'cogs.{file[:-3]}')
#         load all commands from cog folder

bot.run(TOKEN)
# run bot
