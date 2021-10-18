import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)
bot = commands.Bot(command_prefix='!', help_command=None)


for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(TOKEN)



# bot.run(TOKEN)