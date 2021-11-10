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
        self.show_play_time.start()
        self.test = database_func()
        self.playtime = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print("HELLO")
        while True:
            for guild in self.bot.guilds:
                for member in guild.members:
                    # get all members in a server
                    if not member.bot:
                        # if user is not a bot
                        if member.name not in self.playtime:
                            # add user to the dict if not existed
                            self.playtime[member.name] = {}

                        if member.activity is not None:
                            # start playing
                            currActType = str(member.activity.type)
                            if "ActivityType." in currActType:
                                currActType = currActType.replace("ActivityType.", "")
                            currActname = member.activity.name
                            activity = currActType + " " + currActname
                            if member.name in self.playtime:
                                # user is in dict
                                dict = self.playtime[member.name]
                                if activity not in dict:
                                    dict[activity] = 0
                                    # starting to play a game
                                else:
                                    dict[activity] += 5
                                    # continue playing a game
                            else:
                                self.playtime[member.name] = {activity: 0}
                                # user is not in dict, record his activity rarely happens

            await asyncio.sleep(5)

    #         this will check and record user activities every 5 seconds

    @commands.command()
    async def dm(self, ctx, user: discord.Member, *message):
        msg = " ".join(message)
        embed = discord.Embed(title=msg)
        await user.send(embed=embed)

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
        await ctx.send(ctx.message.author.display_name + "  test")

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
    async def status(self, ctx, member: discord.Member):
        # https://discordpy.readthedocs.io/en/stable/intents.html
        # https://stackoverflow.com/questions/67149879/how-to-get-user-activity-in-discord-py
        if member.activity is None:
            await ctx.send(member.display_name + " is not doing anything now")
        else:
            type = str(member.activity.type)
            if "ActivityType." in type:
                type = type.replace("ActivityType.", "")
                if "custom" not in type:
                    await ctx.send(member.name + " is " + type + " " + member.activity.name)
                else:
                    await ctx.send(member.name + " is doing " + member.activity.name)

        return

    @commands.command()
    async def status_self(self, ctx):
        msg = ctx.author.name + "\n"
        dict = self.playtime[ctx.author.name]
        playtime = 0
        streamtime = 0
        listentime = 0
        watchtime = 0
        customtime = 0
        competetime = 0

        for key in dict:
            activityTime = dict[key]
            # get certain activity time
            activityHour = math.floor(activityTime / 3600)
            # find the hours spend
            activityTime = activityTime % 3600
            # reduce the time to find minutes
            activityMinute = math.floor(activityTime / 60)
            # find the minute spend
            activityTime = activityTime % 60
            activitySecond = activityTime

            msg = msg + key + " for " + str(activityHour) + " hours " + str(activityMinute) + " minutes " + str(
                activitySecond) + " seconds\n"

            if "playing" in key:
                playtime = playtime + dict[key]
            if "streaming" in key:
                streamtime = streamtime + dict[key]
            if "watching" in key:
                watchtime = watchtime + dict[key]
            if "listening" in key:
                listentime = listentime + dict[key]
            if "competing" in key:
                competetime = competetime + dict[key]
            if "custom" in key:
                customtime = customtime + dict[key]

        if playtime != 0:
            playHour = math.floor(playtime / 3600)
            playtime = playtime % 3600
            playMinute = math.floor(playtime / 60)
            playtime = playtime % 60
            playSecond = playtime
            msg = msg + "Total play time: " + str(playHour) + " hours " + str(playMinute) + " minutes " + str(
                playSecond) + " seconds \n"
        if streamtime != 0:
            streamHour = math.floor(streamtime / 3600)
            streamtime = streamtime % 3600
            streamMinute = math.floor(streamtime / 60)
            streamtime = streamtime % 60
            streamSecond = streamtime
            msg = msg + "Total stream time: " + str(streamHour) + " hours " + str(streamMinute) + " minutes " + str(
                streamSecond) + " seconds \n"
        if watchtime != 0:
            watchHour = math.floor(watchtime / 3600)
            watchtime = watchtime % 3600
            watchMinute = math.floor(watchtime / 60)
            watchtime = watchtime % 60
            watchSecond = watchtime
            msg = msg + "Total watch time: " + str(watchHour) + " hours " + str(watchMinute) + " minutes " + str(
                watchSecond) + " seconds \n"
        if customtime != 0:
            customHour = math.floor(customtime / 3600)
            customtime = customtime % 3600
            customMinute = math.floor(customtime / 60)
            customtime = customtime % 60
            customSecond = customtime
            msg = msg + "Total custom activity time: " + str(customHour) + " hours " + str(
                customMinute) + " minutes " + str(customSecond) + " seconds \n"
        if competetime != 0:
            competeHour = math.floor(competetime / 3600)
            competetime = competetime % 3600
            competeMinute = math.floor(competetime / 60)
            competetime = competetime % 60
            competeSecond = competetime
            msg = msg + "Total compete time: " + str(competeHour) + " hours " + str(competeMinute) + " minutes " + str(
                competeSecond) + " seconds \n"
        await ctx.send(msg)

    @tasks.loop(hours=12)
    async def show_play_time(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                # get all members in a server
                if not member.bot:
                    msg = member.name + "\n"
                    dict = self.playtime[member.name]
                    playtime = 0
                    streamtime = 0
                    listentime = 0
                    watchtime = 0
                    customtime = 0
                    competetime = 0

                    for key in dict:
                        activityTime = dict[key]
                        # get certain activity time
                        activityHour = math.floor(activityTime / 3600)
                        # find the hours spend
                        activityTime = activityTime % 3600
                        # reduce the time to find minutes
                        activityMinute = math.floor(activityTime / 60)
                        # find the minute spend
                        activityTime = activityTime % 60
                        activitySecond = activityTime

                        msg = msg + key + " for " + str(activityHour) + " hours " + str(
                            activityMinute) + " minutes " + str(activitySecond) + " seconds\n"

                        if "playing" in key:
                            playtime = playtime + dict[key]
                        if "streaming" in key:
                            streamtime = streamtime + dict[key]
                        if "watching" in key:
                            watchtime = watchtime + dict[key]
                        if "listening" in key:
                            listentime = listentime + dict[key]
                        if "competing" in key:
                            competetime = competetime + dict[key]
                        if "custom" in key:
                            customtime = customtime + dict[key]

                    if playtime != 0:
                        playHour = math.floor(playtime / 3600)
                        playtime = playtime % 3600
                        playMinute = math.floor(playtime / 60)
                        playtime = playtime % 60
                        playSecond = playtime
                        msg = msg + "Total play time: " + str(playHour) + " hours " + str(
                            playMinute) + " minutes " + str(playSecond) + " seconds \n"
                    if streamtime != 0:
                        streamHour = math.floor(streamtime / 3600)
                        streamtime = streamtime % 3600
                        streamMinute = math.floor(streamtime / 60)
                        streamtime = streamtime % 60
                        streamSecond = streamtime
                        msg = msg + "Total stream time: " + str(streamHour) + " hours " + str(
                            streamMinute) + " minutes " + str(streamSecond) + " seconds \n"
                    if watchtime != 0:
                        watchHour = math.floor(watchtime / 3600)
                        watchtime = watchtime % 3600
                        watchMinute = math.floor(watchtime / 60)
                        watchtime = watchtime % 60
                        watchSecond = watchtime
                        msg = msg + "Total watch time: " + str(watchHour) + " hours " + str(
                            watchMinute) + " minutes " + str(watchSecond) + " seconds \n"
                    if customtime != 0:
                        customHour = math.floor(customtime / 3600)
                        customtime = customtime % 3600
                        customMinute = math.floor(customtime / 60)
                        customtime = customtime % 60
                        customSecond = customtime
                        msg = msg + "Total custom activity time: " + str(customHour) + " hours " + str(
                            customMinute) + " minutes " + str(customSecond) + " seconds \n"
                    if competetime != 0:
                        competeHour = math.floor(competetime / 3600)
                        competetime = competetime % 3600
                        competeMinute = math.floor(competetime / 60)
                        competetime = competetime % 60
                        competeSecond = competetime
                        msg = msg + "Total compete time: " + str(competeHour) + " hours " + str(
                            competeMinute) + " minutes " + str(competeSecond) + " seconds \n"
                    try:
                        if(msg != member.name):
                            await member.send(msg)
                            # we got some activity recorded
                    except:
                        print("cannot send to this user")

    @status.error
    async def status_error(self, ctx: commands.Context, error: commands.CommandError):
        # error handling for status error
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

    @commands.command(name="addClass")  # Create a new class
    @commands.has_permissions(manage_roles=True)
    async def add_class(self, ctx, class_name: str, server_name: str):
        self.test.add_class(class_name, server_name)
        guild = ctx.guild
        if ctx.author.guild_permissions.manage_channels:
            role = await guild.create_role(name = class_name,colour=discord.Colour(0xff0000))
            authour = ctx.message.author
            await authour.add_roles(role)
            newChannel = await guild.create_text_channel(name = '{}'.format(class_name),)
            member = guild.default_role
            await newChannel.set_permissions(member, view_channel = False)
            await newChannel.set_permissions(role, view_channel = True, send_messages=True)
            message = await ctx.send(f'Class `{class_name}` has been created! \nReact below to join.')
            reaction = await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

    
     
    
    @commands.command(name="getUsersInClass")  # Return all users that are in this class
    async def getUsersInClass(self, ctx, class_id):
        await ctx.send("Users in class {}: ".format(self.test.users_in_class(class_id)))

    @commands.command(name="addUser")  # Add a user to a server
    async def addUser(self, ctx, user_name, server_name, timezone):
        self.test.add_user(user_name, server_name, timezone)
        await ctx.send("User {} added to server {} on timezone {}".format(user_name, server_name, timezone))

    @commands.command(name="getUsers")  # Print all existing users
    async def getUsers(self, ctx):
        await ctx.send("Current existing users: {}".format(self.test.print_all_users()))

    @commands.command(name="deleteClass")
    async def deleteClass(self, ctx, class_name, channel: d.TextChannel):  # Take class_name input as string and then deletes class from table
        self.test.delete_class(class_name)
        role_object = discord.utils.get(ctx.message.guild.roles, name=class_name)
        await ctx.send("Deleted class: {}".format(class_name))
        await role_object.delete()
        mbed = d.Embed(
            tile = 'Success',
            description = "{} has been successfully deleted.".format(class_name)
        )
        if ctx.author.guild_permissions.manage_channels:
            await ctx.send(embed=mbed)
            await channel.delete()

    @commands.command(name="getClasses")
    async def getClasses(self, ctx):
        await ctx.send("Current existing classes: {}".format(self.test.print_all_class()))

    @commands.command(name="reminder")
    async def reminder(self, ctx, date: str, *message):
        # reminder group feature
        try:
            reminder = datetime.strptime(date, "%Y-%m-%d-%H:%M")
        except Exception as e:
            await ctx.send(e)
        else:
            today = datetime.now()
            diff = (reminder - today).total_seconds()
            # find the difference in seconds and wait
            msg = " ".join(message)
            await ctx.send("a reminder is set up for " + date + " for " + msg)
            await asyncio.sleep(diff)
            # reminder sleeping
            await ctx.send("Reminder: " + msg)
            # time up

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

    @commands.command()
    async def reminder_self(self, ctx, date: str, *message):
        # reminder for self only
        try:
            reminder = datetime.strptime(date, "%Y-%m-%d-%H:%M")
        except Exception as e:
            await ctx.author.send(e)
        else:
            today = datetime.now()
            diff = (reminder - today).total_seconds()
            # find the difference in seconds and wait
            msg = " ".join(message)
            await ctx.author.send("a reminder is set up for " + date + " for " + msg)
            await asyncio.sleep(diff)
            # reminder sleeping
            await ctx.author.send("Reminder: " + msg)
            
    @commands.command()
    async def add_task(self,ctx, title, difficulty, deadline, class_name):
        format_deadline = '%Y-%m-%d-%H:%M'
        try:
            user_id = ctx.message.author.id
            user_id = int(user_id/100000000)
            title = title
            difficulty = int(difficulty)
            deadline = datetime.strptime(deadline,format_deadline)
            

        except Exception as e:
            await ctx.send(e)
        else:     
            self.test.add_task(user_id,title,difficulty,deadline,class_name)
            await ctx.send("Task added")
    @add_task.error
    async def add_task_error(self,ctx: commands.context, error: commands.CommandError):
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
    
    
    
    @commands.command(name="deleteClass")
    async def deleteClass(self, ctx, class_name, channel: d.TextChannel):  # Take class_name input as string and then deletes class from table
        self.test.delete_class(class_name)
        role_object = discord.utils.get(ctx.message.guild.roles, name=class_name)
        await ctx.send("Deleted class: {}".format(class_name))
        await role_object.delete()
        mbed = d.Embed(
            tile = 'Success',
            description = "{} has been successfully deleted.".format(class_name)
        )
        if ctx.author.guild_permissions.manage_channels:
            await ctx.send(embed=mbed)
            await channel.delete()
    @commands.command()
    async def delete_task(self,ctx,task_name):
        self.test.delete_task(task_name)
        await ctx.send("Task deleted")
    
    @tasks.loop(minutes=1)
    async def remove_expired_tasks(self):
        self.test.remove_expired_tasks()

    
    @delete_task.error
    async def delete_task_error(self,ctx: commands.context, error: commands.CommandError):
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
        
    
    @commands.command()
    async def taskm(self,ctx):
        user_id = int(ctx.message.author.id/100000000)
        x = self.test.get_tasks_month(user_id)
        tasks_as_user = [a for a in x if a[1] == user_id]
        await ctx.send("There are {} tasks due in the next month".format(len(tasks_as_user)))
        for i in x:
            if i[1] == user_id:
                s = "{} is due on {} with difficulty {} and for class {}".format(i[2],i[4],i[3],i[5])
                await ctx.send(s)
        #await ctx.send("List of tasks due the next thirty days: {}".format(self.test.get_tasks_month(int(ctx.message.author.id)/100000000)))
    
    @commands.command()
    async def taskw(self,ctx):
        user_id = int(ctx.message.author.id/100000000)
        x = self.test.get_tasks_week(user_id)
        tasks_as_user = [a for a in x if a[1] == user_id]
        await ctx.send("There are {} tasks due in the next week".format(len(tasks_as_user)))
        for i in x:
            if i[1] == user_id:
                s = "{} is due on {} with difficulty {} and for class {}".format(i[2],i[4],i[3],i[5])
                await ctx.send(s)
        #await ctx.send("List of tasks due the next thirty days: {}".format(self.test.get_tasks_month(int(ctx.message.author.id)/100000000)))
              
    @reminder_self.error
    async def reminder_self_error(self, ctx: commands.Context, error: commands.CommandError):
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

        await ctx.author.send(message, delete_after=10)
        # await ctx.message.delete(delay=5)

    
def setup(bot):
    bot.add_cog(basic(bot))
