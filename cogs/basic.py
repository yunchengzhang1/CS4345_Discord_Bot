from discord.ext import commands
from discord import Embed
from database_func import database_func
from datetime import datetime
import asyncio

class basic(commands.Cog):
    # this file store basic commands
    def __init__(self, bot):
        self.bot = bot
        self.test = database_func()


    @commands.command()
    async def test(self, ctx):
        await ctx.send("Edward test")
    #     test

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
            embed = Embed(title="Poll",
                          description=question,
                          colour=ctx.author.colour,
                          timestamp=datetime.utcnow())
            # create a embed
            fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False),
                      ("Instructions", "React to cast a vote!", False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            # configure and add fields
            message = await ctx.send(embed=embed)
            # send message

            for emoji in numbers[:len(options)]:
                await message.add_reaction(emoji)
            #     add reaction

            await asyncio.sleep(seconds)
            # sleep for a designated time to wait for result

            message = await self.bot.get_channel(message.channel.id).fetch_message(message.id)

            most_voted = max(message.reactions, key=lambda r: r.count)

            await message.channel.send(
                f"The results are in and option {most_voted.emoji} was the most popular with {most_voted.count - 1:,} votes!")
    #         conclude the result

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

    @commands.command(name="addClass")  # Create a new class
    async def add_class(self, ctx, class_name: str, server_name: str):
        self.test.add_class(class_name, server_name)
        await ctx.send("Class added with name " + class_name + "classname "+ server_name)

    @commands.command(name="getUsersInClass")  # Return all users that are in this class
    async def getUsersInClass(self,ctx, class_id):
        await ctx.send("Users in class {}: ".format(self.test.users_in_class(class_id)))

    @commands.command(name="addUser")  # Add a user to a server
    async def addUser(self, ctx, user_name, server_name, timezone):
        self.test.add_user(user_name, server_name, timezone)
        await ctx.send("User {} added to server {} on timezone {}".format(user_name, server_name, timezone))

    @commands.command(name="getUsers")  # Print all existing users
    async def getUsers(self, ctx):
        await ctx.send("Current existing users: {}".format(self.test.print_all_users()))

    @commands.command(name="deleteClass")
    async def deleteClass(self, ctx, class_name):  # Take class_name input as string and then deletes class from table
        self.test.delete_class(class_name)
        await ctx.send("Deleted class: {}".format(class_name))

    @commands.command(name="getClasses")
    async def getClasses(self, ctx):
        await ctx.send("Current existing classes: {}".format(self.test.print_all_class()))

    @commands.command(name="reminder")
    async def reminder(self, ctx, date: str, *message):
        # reminder feature
        reminder = datetime.strptime(date, "%Y-%m-%d-%H:%M")
        today = datetime.now()
        diff = (reminder - today).total_seconds()
        # find the difference in seconds and wait
        msg = " ".join(message)
        await ctx.send("a reminder is set up for " + date + " for " + msg)
        await asyncio.sleep(diff)
        # reminder sleeping
        await ctx.send("Reminder: " + msg)
    #     time up

    @reminder.error
    async def example_error(self, ctx: commands.Context, error: commands.CommandError):
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


def setup(bot):
    bot.add_cog(basic(bot))
