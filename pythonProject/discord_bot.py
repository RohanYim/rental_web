import discord
from discord.ext import commands
import os
import json
from setting import *
from discord_webhook import DiscordWebhook

intents = discord.Intents.default()
intents.members = True
# TOKEN = 'ODUyNzUwMTkzMjQ1OTQ1ODg2.YMLXgQ.p2ASKuGMMya9o1jJCXUrMLthrV0'
# COMMAND_PREFIX = "!"

client = commands.Bot(command_prefix="!", intents=intents)


# class Myclient(discord.Client):
#     async def on_ready(self):
#         print('Logged on as {0}!'.format(self.user))
#
#     async def on_message(self, message):
#         print("message from {0.author}:{0.content}".format(message))
#         # if message.author.bot:
#         #     return
#         #
#         # if message.content[0] == COMMAND_PREFIX:
#         #     await message.channel.send("Hello from test2!")
#         #
#         # if message.content == "!ping":
#         #     await message.channel.send("pong!")
#
# # client = Myclient()
# @commands.command()
# async def ping(ctx):
#     await ctx.send("pong!")
# client.add_command(ping)
@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))

# @client.event
# async def on_message(msg):
#     channel = client.get_channel(861526864919789568)
#     if msg.channel != channel:
#         if msg.content != None:
#             await channel.send(msg.content)


@client.event
async def on_member_join(member: discord.Member):
    embed = discord.Embed(title="Welcome to HR Space!", url="https://www.tidalmarket.com/",
                          description="To get further support, please click the blue chat icon in the bottom right corner of HR Space website.",
                          color=discord.Colour.purple())
    # embed.set_author(name=)
    embed.set_thumbnail(url="https://www.whop.io/assets/whop.png")
    embed.add_field(name="Start to rent:", value="https://www.tidalmarket.com/", inline=False)
    embed.add_field(name="To be a seller:", value="https://www.tidalmarket.com/", inline=False)
    embed.add_field(name="Guide and Document:", value="https://www.tidalmarket.com/", inline=False)
    embed.set_footer(text="Made by HR Space", icon_url="https://www.whop.io/assets/whop.png")




    # with open("embed.json", "r") as file:
    #     embeds_json = json.load(file)
    #     embeds_dict = embeds_json[0]
    # embed = discord.Embed.from_dict(embeds_dict)

    if member is not None:
        channel = member.dm_channel
        if channel is None:
            channel = await member.create_dm()

        await channel.send(embed=embed)



for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
            client.load_extension(f'cogs.{filename[:-3]}')





# print(DISCORD_BOT_TOKEN)
client.run('ODUyNzUwMTkzMjQ1OTQ1ODg2.YMLXgQ.MIGuBIEBoo8K_Tpvi8JsC4AONCc')
