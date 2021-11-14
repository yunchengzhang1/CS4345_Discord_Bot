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


class UserActivity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.test = database_func.getInstance()
        self.playtime = {}

    @commands.Cog.listener()
    async def on_ready(self):
        self.collect_play_time.start()
        self.show_play_time.start()
        self.warn_play_time.start()


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

    @commands.command()
    async def status_self(self, ctx):
        msg = ctx.author.name + "\n"
        results_list = self.test.get_user_activities(ctx.author.id)
        # list of tuples where [0] is activity and [1] is time
        for activity in results_list:
            act_time = activity[1]
            act_hour = math.floor(act_time / 3600)
            act_time = act_time % 3600
            act_minute = math.floor(act_time / 60)
            act_seconds = act_time % 60
            msg = msg + activity[0] + " for " + str(act_hour) + " hours " + str(act_minute) + " minutes " + str(
                act_seconds) + " seconds\n"

        await ctx.send(msg)

        # dict = self.playtime[ctx.author.name]
        # playtime = 0
        # streamtime = 0
        # listentime = 0
        # watchtime = 0
        # customtime = 0
        # competetime = 0
        #
        # for key in dict:
        #     activityTime = dict[key]
        #     # get certain activity time
        #     activityHour = math.floor(activityTime / 3600)
        #     # find the hours spend
        #     activityTime = activityTime % 3600
        #     # reduce the time to find minutes
        #     activityMinute = math.floor(activityTime / 60)
        #     # find the minute spend
        #     activityTime = activityTime % 60
        #     activitySecond = activityTime
        #
        #     msg = msg + key + " for " + str(activityHour) + " hours " + str(activityMinute) + " minutes " + str(
        #         activitySecond) + " seconds\n"
        #
        #     if "playing" in key:
        #         playtime = playtime + dict[key]
        #     if "streaming" in key:
        #         streamtime = streamtime + dict[key]
        #     if "watching" in key:
        #         watchtime = watchtime + dict[key]
        #     if "listening" in key:
        #         listentime = listentime + dict[key]
        #     if "competing" in key:
        #         competetime = competetime + dict[key]
        #     if "custom" in key:
        #         customtime = customtime + dict[key]
        #
        # if playtime != 0:
        #     playHour = math.floor(playtime / 3600)
        #     playtime = playtime % 3600
        #     playMinute = math.floor(playtime / 60)
        #     playtime = playtime % 60
        #     playSecond = playtime
        #     msg = msg + "Total play time: " + str(playHour) + " hours " + str(playMinute) + " minutes " + str(
        #         playSecond) + " seconds \n"
        # if streamtime != 0:
        #     streamHour = math.floor(streamtime / 3600)
        #     streamtime = streamtime % 3600
        #     streamMinute = math.floor(streamtime / 60)
        #     streamtime = streamtime % 60
        #     streamSecond = streamtime
        #     msg = msg + "Total stream time: " + str(streamHour) + " hours " + str(streamMinute) + " minutes " + str(
        #         streamSecond) + " seconds \n"
        # if watchtime != 0:
        #     watchHour = math.floor(watchtime / 3600)
        #     watchtime = watchtime % 3600
        #     watchMinute = math.floor(watchtime / 60)
        #     watchtime = watchtime % 60
        #     watchSecond = watchtime
        #     msg = msg + "Total watch time: " + str(watchHour) + " hours " + str(watchMinute) + " minutes " + str(
        #         watchSecond) + " seconds \n"
        # if customtime != 0:
        #     customHour = math.floor(customtime / 3600)
        #     customtime = customtime % 3600
        #     customMinute = math.floor(customtime / 60)
        #     customtime = customtime % 60
        #     customSecond = customtime
        #     msg = msg + "Total custom activity time: " + str(customHour) + " hours " + str(
        #         customMinute) + " minutes " + str(customSecond) + " seconds \n"
        # if competetime != 0:
        #     competeHour = math.floor(competetime / 3600)
        #     competetime = competetime % 3600
        #     competeMinute = math.floor(competetime / 60)
        #     competetime = competetime % 60
        #     competeSecond = competetime
        #     msg = msg + "Total compete time: " + str(competeHour) + " hours " + str(competeMinute) + " minutes " + str(
        #         competeSecond) + " seconds \n"
        # await ctx.send(msg)

    @tasks.loop(seconds=10)
    async def collect_play_time(self):
        for guild in self.bot.guilds:
            # get all servers that bots are in
            for member in guild.members:
                # get all members in a server
                if not member.bot:
                    if member.activity is not None:
                        currActType = str(member.activity.type)
                        if "ActivityType." in currActType:
                            currActType = currActType.replace("ActivityType.", "")
                        currActname = member.activity.name
                        activity = currActType + " " + currActname
                        if self.test.activity_exist(member.id, activity):
                            # if the activity is recorded in db
                            self.test.update_activity(member.id, activity)
                        else:
                            # if not recorded
                            self.test.add_activity(member.id, activity)

                        # get activity with user id and member activity

    # @tasks.loop(seconds= 10)
    # async def collect_play_time(self):
    #     for guild in self.bot.guilds:
    #         # get all servers that bots are in
    #         for member in guild.members:
    #             # get all members in a server
    #             if not member.bot:
    #                 # if user is not a bot
    #                 if member.name not in self.playtime:
    #                     # add user to the dict if not existed
    #                     self.playtime[member.name] = {}
    #
    #                 if member.activity is not None:
    #                     # start playing
    #                     currActType = str(member.activity.type)
    #                     if "ActivityType." in currActType:
    #                         currActType = currActType.replace("ActivityType.", "")
    #                     currActname = member.activity.name
    #                     activity = currActType + " " + currActname
    #                     if member.name in self.playtime:
    #                         # user is in dict
    #                         dict = self.playtime[member.name]
    #                         if activity not in dict:
    #                             dict[activity] = 0
    #                             # starting to play a game
    #                         else:
    #                             dict[activity] += 10
    #                             # continue playing a game
    #                     else:
    #                         self.playtime[member.name] = {activity: 0}
    #                         # user is not in dict, record his activity rarely happens
    #     #         this will check and record user activities every 5 seconds

    @tasks.loop(seconds=60)
    async def warn_play_time(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                # get all members in a server
                if not member.bot:
                    status = self.test.get_playtime_limit_and_warning(member.id)
                    # return status info like playtime limit and is warned
                    result = self.test.sum_user_activities(member.id)
                    # return sum playtime
                    if status[1] == 0 and status[0] < result:
                        #  they have not been warned about play time
                        #  and have exceeded playtime
                        msg = member.name + "\n"
                        try:
                            msg = msg + "You have exceeded your planned play time, please make sure that you are actively doing work\n"
                            await member.send(msg)
                        except:
                            print("cannot send to this user")
                        self.test.is_warned(member.id)



                    # dict = self.playtime[member.name]
                    # activityTime = 0
                    # for key in dict:
                    #     activityTime = dict[key]
                    #     # get certain activity time
                    #     activityHour = math.floor(activityTime / 3600)
                    #     # find the hours spend
                    #     activityTime = activityTime % 3600
                    #     # reduce the time to find minutes
                    #     activityMinute = math.floor(activityTime / 60)
                    #     # find the minute spend
                    #     activityTime = activityTime % 60
                    #     activitySecond = activityTime
                    #
                    #     msg = msg + key + " for " + str(activityHour) + " hours " + str(
                    #         activityMinute) + " minutes " + str(activitySecond) + " seconds\n"
                    #
                    # if activityTime > 3600:
                    #     try:
                    #         if (msg != member.name):
                    #             msg = msg + "You have exceeded your planned play time, please make sure that you are actively doing work\n"
                    #             await member.send(msg)
                    #     except:
                    #         print("cannot send to this user")

    @tasks.loop(hours=12)
    async def show_play_time(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                # get all members in a server
                if not member.bot:
                    msg = member.name + "\n"
                    results_list = self.test.get_user_activities(member.id)
                    # list of tuples where [0] is activity and [1] is time
                    if len(results_list) > 0:
                        for activity in results_list:
                            act_time = activity[1]
                            act_hour = math.floor(act_time / 3600)
                            act_time = act_time % 3600
                            act_minute = math.floor(act_time / 60)
                            act_seconds = act_time % 60
                            msg = msg + activity[0] + " for " + str(act_hour) + " hours " + str(
                                act_minute) + " minutes " + str(
                                act_seconds) + " seconds\n"
                        try:
                            await member.send(msg)
                                # we got some activity recorded
                        except:
                            print("cannot send to this user")


                    # msg = member.name + "\n"
                    # dict = self.playtime[member.name]
                    # playtime = 0
                    # streamtime = 0
                    # listentime = 0
                    # watchtime = 0
                    # customtime = 0
                    # competetime = 0
                    #
                    # for key in dict:
                    #     activityTime = dict[key]
                    #     # get certain activity time
                    #     activityHour = math.floor(activityTime / 3600)
                    #     # find the hours spend
                    #     activityTime = activityTime % 3600
                    #     # reduce the time to find minutes
                    #     activityMinute = math.floor(activityTime / 60)
                    #     # find the minute spend
                    #     activityTime = activityTime % 60
                    #     activitySecond = activityTime
                    #
                    #     msg = msg + key + " for " + str(activityHour) + " hours " + str(
                    #         activityMinute) + " minutes " + str(activitySecond) + " seconds\n"
                    #
                    #     if "playing" in key:
                    #         playtime = playtime + dict[key]
                    #     if "streaming" in key:
                    #         streamtime = streamtime + dict[key]
                    #     if "watching" in key:
                    #         watchtime = watchtime + dict[key]
                    #     if "listening" in key:
                    #         listentime = listentime + dict[key]
                    #     if "competing" in key:
                    #         competetime = competetime + dict[key]
                    #     if "custom" in key:
                    #         customtime = customtime + dict[key]
                    #
                    # if playtime != 0:
                    #     playHour = math.floor(playtime / 3600)
                    #     playtime = playtime % 3600
                    #     playMinute = math.floor(playtime / 60)
                    #     playtime = playtime % 60
                    #     playSecond = playtime
                    #     msg = msg + "Total play time: " + str(playHour) + " hours " + str(
                    #         playMinute) + " minutes " + str(playSecond) + " seconds \n"
                    # if streamtime != 0:
                    #     streamHour = math.floor(streamtime / 3600)
                    #     streamtime = streamtime % 3600
                    #     streamMinute = math.floor(streamtime / 60)
                    #     streamtime = streamtime % 60
                    #     streamSecond = streamtime
                    #     msg = msg + "Total stream time: " + str(streamHour) + " hours " + str(
                    #         streamMinute) + " minutes " + str(streamSecond) + " seconds \n"
                    # if watchtime != 0:
                    #     watchHour = math.floor(watchtime / 3600)
                    #     watchtime = watchtime % 3600
                    #     watchMinute = math.floor(watchtime / 60)
                    #     watchtime = watchtime % 60
                    #     watchSecond = watchtime
                    #     msg = msg + "Total watch time: " + str(watchHour) + " hours " + str(
                    #         watchMinute) + " minutes " + str(watchSecond) + " seconds \n"
                    # if customtime != 0:
                    #     customHour = math.floor(customtime / 3600)
                    #     customtime = customtime % 3600
                    #     customMinute = math.floor(customtime / 60)
                    #     customtime = customtime % 60
                    #     customSecond = customtime
                    #     msg = msg + "Total custom activity time: " + str(customHour) + " hours " + str(
                    #         customMinute) + " minutes " + str(customSecond) + " seconds \n"
                    # if competetime != 0:
                    #     competeHour = math.floor(competetime / 3600)
                    #     competetime = competetime % 3600
                    #     competeMinute = math.floor(competetime / 60)
                    #     competetime = competetime % 60
                    #     competeSecond = competetime
                    #     msg = msg + "Total compete time: " + str(competeHour) + " hours " + str(
                    #         competeMinute) + " minutes " + str(competeSecond) + " seconds \n"
                    # try:
                    #     if (msg != member.name):
                    #         await member.send(msg)
                    #         # we got some activity recorded
                    # except:
                    #     print("cannot send to this user")


def setup(bot):
    bot.add_cog(UserActivity(bot))
