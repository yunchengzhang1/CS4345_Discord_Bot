import mysql.connector
from mysql.connector import Error
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from database_func import database_func


test = database_func()
test.users_in_class(3)
# connect to database

# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')
#
#
# bot = commands.Bot(command_prefix='!', help_command=None)
# # @bot.command(name="test")
# # async def test(ctx):
# #     await ctx.send("Edward Testing")
# #
# @bot.command(name="ping")
# async def ping(ctx):
#     await ctx.send("Latency: " +str(round(bot.latency*1000)) +" ms")
#
# bot.run(TOKEN)

