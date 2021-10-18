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


# a polling feature that Edward is working on
# @bot.command(name="createpoll", aliases=["mkpoll"])
# async def create_poll(ctx, hours: int, question: str, *options):
#     polls = []
#     if len(options) > 10:
#         await ctx.send("You can only supply a maximum of 10 options.")
#
#     else:
#         embed = Embed(title="Poll",
#                       description=question,
#                       colour=ctx.author.colour,
#                       timestamp=datetime.utcnow())
#
#         fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False),
#                   ("Instructions", "React to cast a vote!", False)]
#
#         for name, value, inline in fields:
#             embed.add_field(name=name, value=value, inline=inline)
#
#         message = await ctx.send(embed=embed)
#
#         for emoji in numbers[:len(options)]:
#             await message.add_reaction(emoji)
#
#         polls.append((message.channel.id, message.id))
#
#         bot.scheduler.add_job(self.complete_poll, "date", run_date=datetime.now() + timedelta(seconds=hours),
#                                    args=[message.channel.id, message.id])
#
# bot.run(TOKEN)