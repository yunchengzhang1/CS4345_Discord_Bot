import discord
from discord.ext import commands


class basic(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def testED (self, ctx):
        await ctx.send("Edward test")


    # @commands.command()
    # async def ping(ctx):
    #     await ctx.send("Latency: " + str(round(self.bot.latency * 1000)) + " ms")




def setup(client):
    client.add_cog(basic(client))