import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Client()

bot = commands.Bot(command_prefix='!', help_command=None)
@bot.command(name="test")
async def test(ctx):
    await ctx.send("hello world")

bot.run(TOKEN)
