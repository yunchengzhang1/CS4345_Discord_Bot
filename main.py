import os
import discord
import mysql.connector 
from mysql.connector import Error 
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ROOT = os.getenv('ROOT')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
# print(ROOT)
# print(PASSWORD)
# print(HOST)
# print(DATABASE)

# connection_json = { 
#     'user':ROOT, 
#     'password':PASSWORD, 
#     'host':HOST,
#     'database':DATABASE,
#     'raise_on_warnings':True 
# }


def mysql_connect():
    connection = None 
    try: 
        connection = mysql.connector.connect(host=HOST, database=DATABASE, user=ROOT, password=PASSWORD)
        # connection = mysql.connector.connect(*connection_json)
        if connection.is_connected(): 
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def run_discord_bot():
    bot = discord.Client()

    bot = commands.Bot(command_prefix='!austin', help_command=None)
    @bot.command(name="test")
    async def test(ctx):
        await ctx.send("hello world")

    @bot.command(name="server")
    async def test(ctx):
        await ctx.send(ctx.guild.name)
        await ctx.send(ctx.guild.id)

    @bot.event 
    async def on_ready():
        print(f'logged in as {bot.user.name}')
        print(f'connected to guild {discord.guild}')

    bot.run(TOKEN)

if __name__ == '__main__': 
    mysql_connect()
    # run_discord_bot()