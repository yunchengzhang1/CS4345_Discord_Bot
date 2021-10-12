import mysql.connector
from mysql.connector import Error
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from database_func import database_func
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')


test = database_func()
bot = commands.Bot(command_prefix='!',help_command=None)
@bot.command(name="addClass")#Create a new class
async def add_class(ctx,arg1,arg2):
    test.add_class(arg1,arg2)
    await ctx.send("Class added with name = {} and {}".format(arg1,arg2))
    
@bot.command(name="getUsersInClass")#Return all users that are in this class
async def getUsersInClass(ctx,arg1):
    await ctx.send("Users in class {}: ".format(test.users_in_class(arg1)))
    
@bot.command(name="addUser") #Add a user to a server
async def addUser(ctx,arg1,arg2,arg3):
    test.add_user(arg1,arg2,arg3)
    await ctx.send("User {} added to server {} on timesize {}".format(arg1,arg2,arg3))
    
@bot.command(name="getUsers") #Print all existing users
async def getUsers(ctx):
    await ctx.send("Current existing users: {}".format(test.print_all_users()))

@bot.command(name="deleteClass")
async def deleteClass(ctx,argg): # Take class_name input as string and then deletes class from table
    test.delete_class(argg)
    await ctx.send("Deleted class: {}".format(argg))
@bot.command(name="getClasses")
async def getClasses(ctx):
    await ctx.send("Current existing classes: {}".format(test.print_all_class()))


bot.run(TOKEN)
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

