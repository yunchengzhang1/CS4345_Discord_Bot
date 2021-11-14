from discord.ext import commands, tasks
from discord import Embed
import discord
import discord as d
from discord import channel
from discord import guild
from database_func import database_func
from datetime import datetime
import asyncio
import math


class basic(commands.Cog):
    # this file store basic commands
    def __init__(self, bot):
        self.bot = bot
        self.test = database_func.getInstance()
        self.check_reminders.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot ready")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for member in guild.members:
            if not member.bot:
                self.test.add_user(member.id, member.name)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.test.add_user(member.id, member.name)

    @commands.Cog.listener()
    async def on_member_leave(self,member):
        self.test.delete_user(member.id)

    @commands.command()
    async def dm(self, ctx, user: discord.Member):
        USERID = user.id
        await ctx.send(f"<@{USERID}>")


    @commands.command()
    async def help(self, ctx):
        # display all available commands
        author = ctx.message.author
        embed = Embed(title="Help",
                      colour=ctx.author.colour)

        embed.add_field(name="!ping", value="Pong", inline=False)
        embed.add_field(name="!test", value="Author test", inline=False)
        embed.add_field(name="!announcement title(str) *description(str)", value="Create an announcement", inline=False)
        embed.add_field(name="!create_poll seconds(int) question(string) *options(string)", value="Create a poll",
                        inline=False)
        embed.add_field(name="!reminder date(YYYY-MM-DD-HH:MM in 24 hour clock) *text(str)", value="Make a reminder",
                        inline=False)
        embed.add_field(name="!reminder date(YYYY-MM-DD-HH:MM in 24 hour clock) *text(str)", value="Make a reminder",
                        inline=False)
        embed.add_field(name="!status @[valid ping]", value="Check other's activity", inline=False)
        embed.add_field(name="!status_self", value="Check your time playing all video games", inline=False)

        embed.set_footer(text="* value can be multiple values, other can only accept one value")
        await ctx.send(author, embed=embed)

    @commands.command()
    async def test(self, ctx):
        await ctx.send(ctx.message.author.display_name + " test")
        # await ctx.send(ctx.author.id)



    @commands.command()
    async def announcement(self, ctx, title, *description):
        msg = ' '.join(description)
        embed = Embed(title=title,
                      description=msg,
                      colour=ctx.author.colour,
                      timestamp=datetime.utcnow())
        embed.set_author(name=ctx.author)

        message = await ctx.send(embed=embed)
        await message.pin()

    @announcement.error
    async def announcement_error(self, ctx: commands.Context, error: commands.CommandError):
        # reminder error handling
        if isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permissions to run this command!"
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing a required argument: {error.param}"
        elif isinstance(error, commands.ConversionError):
            message = str(error)
        else:
            message = "Oh no! Something went wrong while running the command!"
        await ctx.send(message, delete_after=10)
        # await ctx.message.delete(delay=5)

    @commands.command()
    async def ping(self, ctx):

        latency = ctx.bot.latency
        # Latency is returned in milliseconds
        latency = latency * 1000
        # Latency is converted to a string
        latency = str(latency)
        # The latency is sent to the user
        await ctx.send(f'Pong! `{latency}ms`')
    #     test latency

    @commands.command()
    async def create_poll(self, ctx, seconds: int, question: str, *options):
        # create a poll
        if len(options) > 10:
            await ctx.send("You can only supply a maximum of 10 options.")

        else:
            numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
                       "6⃣", "7⃣", "8⃣", "9⃣", "🔟")
            # reaction array
            embed = Embed(title="Poll",
                          description=question,
                          colour=ctx.author.colour,
                          timestamp=datetime.utcnow())
            # create a embed
            fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False),
                      ("Instructions", "React to cast a vote!", False)]
            # field prototype
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            # configure and add fields
            poll = await ctx.send(embed=embed)
            # send poll

            for emoji in numbers[:len(options)]:
                await poll.add_reaction(emoji)
            #     add reaction
            await poll.pin()
            # pin polll

            await asyncio.sleep(seconds)
            # sleep for a designated time to wait for result

            message = await self.bot.get_channel(poll.channel.id).fetch_message(poll.id)

            most_voted = max(message.reactions, key=lambda r: r.count)
            # get the most voted reaction

            await message.channel.send(
                f"The results are in and option {most_voted.emoji} was the most popular with {most_voted.count - 1:,} votes!\n Poll is removed from pinned messages")

            await poll.unpin()

    #         conclude the result and unpin the poll

    @create_poll.error
    async def poll_error(self, ctx: commands.Context, error: commands.CommandError):
        # error handling for poll error
        if isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permissions to run this command!"
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing a required argument: {error.param}"
        elif isinstance(error, commands.ConversionError):
            message = str(error)
        else:
            message = "Oh no! Something went wrong while running the command!"

        await ctx.send(message, delete_after=10)
        # await ctx.message.delete(delay=5)

    #
    # @commands.command(name="reminder")
    # async def reminder(self, ctx,date: str, title, *message):
    #     # reminder group feature
    #     try:
    #         reminder = datetime.strptime(date, "%Y-%m-%d-%H:%M")
    #     except Exception as e:
    #         await ctx.send(e)
    #     else:
    #         today = datetime.now()
    #         diff = (reminder - today).total_seconds()
    #         # find the difference in seconds and wait
    #         msg = " ".join(message)
    #         await ctx.send("a reminder is set up for " + date + " for " + title)
    #         await asyncio.sleep(diff)
    #         # reminder sleeping
    #         embed = Embed(title="Reminder "+title,
    #                       description=msg,
    #                       colour=ctx.author.colour,
    #                       timestamp=datetime.utcnow())
    #         embed.set_author(name=ctx.author)
    #         await ctx.send(embed =embed)
    #         # time up

    @commands.command(name="reminder")
    async def reminder(self, ctx,date: str, title, *message):
        # reminder group feature
        try:
            reminder = datetime.strptime(date, "%Y-%m-%d-%H:%M")

        except Exception as e:
            await ctx.send(e)
        else:
            msg = " ".join(message)
            message_sent = await ctx.send("a reminder is set up for " + date + " for " + title)
            # await ctx.send(message_sent.channel.id)
            self.test.add_reminder(message_sent.id,message_sent.channel.id,ctx.author.id, reminder, title,msg)





            # message = await self.bot.get_channel(poll.channel.id).fetch_message(poll.id)




    @reminder.error
    async def reminder_error(self, ctx: commands.Context, error: commands.CommandError):
        # reminder error handling
        if isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permissions to run this command!"
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing a required argument: {error.param}"
        elif isinstance(error, commands.ConversionError):
            message = str(error)
        else:
            message = "Oh no! Something went wrong while running the command!"

        await ctx.send(message, delete_after=10)
        # await ctx.message.delete(delay=5)

    @tasks.loop(seconds=30)
    async def check_reminders(self):
        results = self.test.get_reminders()
    #     return a list of reminders on current time
        if results is None:
            return
        else:
            for reminder in results:
                channelid = reminder[0]
                title = reminder[1]
                description = reminder[2]
                channel = self.bot.get_channel(channelid)
                embed = Embed(
                    title = title,
                    description = description,
                    timestamp=datetime.utcnow()
                )
                await channel.send(embed = embed)


    # @commands.command()
    # async def reminder_self(self, ctx, date: str, *message):
    #     # reminder for self only
    #     try:
    #         reminder = datetime.strptime(date, "%Y-%m-%d-%H:%M")
    #     except Exception as e:
    #         await ctx.author.send(e)
    #     else:
    #         today = datetime.now()
    #         diff = (reminder - today).total_seconds()
    #         # find the difference in seconds and wait
    #         msg = " ".join(message)
    #         await ctx.author.send("a reminder is set up for " + date + " for " + msg)
    #         await asyncio.sleep(diff)
    #         # reminder sleeping
    #         await ctx.author.send("Reminder: " + msg)
    #
    #
    # @reminder_self.error
    # async def reminder_self_error(self, ctx: commands.Context, error: commands.CommandError):
    #     # reminder error handling
    #     if isinstance(error, commands.CommandOnCooldown):
    #         message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
    #     elif isinstance(error, commands.MissingPermissions):
    #         message = "You are missing the required permissions to run this command!"
    #     elif isinstance(error, commands.MissingRequiredArgument):
    #         message = f"Missing a required argument: {error.param}"
    #     elif isinstance(error, commands.ConversionError):
    #         message = str(error)
    #     else:
    #         message = "Oh no! Something went wrong while running the command!"
    #
    #     await ctx.author.send(message, delete_after=10)
    #     # await ctx.message.delete(delay=5)

    
def setup(bot):
    bot.add_cog(basic(bot))
