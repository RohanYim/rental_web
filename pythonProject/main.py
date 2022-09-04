import discord

from discord.ext import commands


TOKEN = 'ODUyNzUwMTkzMjQ1OTQ1ODg2.YMLXgQ.p2ASKuGMMya9o1jJCXUrMLthrV0'

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

@client.command(name='sendDM')
async def DM(ctx, member: discord.member = None):
    if member is not None:
        channel = member.dm_channel
        if channel is None:
            await member.create_dm()
        await channel.send("test!")


@client.command()
async def IDs(ctx):
    await ctx.send('''371524199801223014李振今\n37010419980414222X林泽峣\n370102199804302526孟嘉珺\n370103199807307011李炳崑\n370105200002025322唐笑薇\n370112199810246850 宋浩然''')

@client.command(name='getlastmessage')
async def client_getlastmessage(ctx):
    """Get the last message of a text channel."""
    server = client.get_guild(594010666554097664)
    channel = client.get_channel(716653710629011466)
    if channel is None:
        await ctx.send('Could not find that channel.')
        return
    # NOTE: get_channel can return a TextChannel, VoiceChannel,
    # or CategoryChannel. You may want to add a check to make sure
    # the ID is for text channels only

    message = await channel.fetch_message(
        channel.last_message_id)
    # NOTE: channel.last_message_id could return None; needs a check
    await ctx.send(
        message.content
    )
    # NOTE: message may need to be trimmed to fit within 2000 chars
client.run(TOKEN)
