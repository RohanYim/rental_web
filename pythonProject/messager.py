import discord
from discord.ext import commands
from setting import *

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))


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
    if member is not None:
        channel = member.dm_channel
        if channel is None:
            channel = await member.create_dm()
        await channel.send(embed=embed)

@client.event
async def on_message(msg):
    channel = client.get_channel(861526864919789568)
    if msg.channel != channel:
        if msg.content != None:
            await channel.send(msg.content)



client.run(DISCORD_BOT_TOKEN)