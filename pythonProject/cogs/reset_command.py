import discord
from discord.ext import commands
import os

from cogs.reset.autoreset import reset_mekaio, reset_stellar, reset_kodai, reset_koi


class Reset_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reset_command(self, ctx, bot, key, nickname, seller_id, member: discord.Member = None, *args):
        guild = ctx.guild
        # bot = "Dashe"
        # time = "2016-04-07 10:25:09"
        if bot == 'Velox':
            os.system(r"python cogs\\reset\\velox_reset.py %s" % seller_id)
        if bot == 'Balko':
            os.system(r"python cogs\\reset\\balko_reset.py %s" % seller_id)
        if bot == 'Mekaio':
            result = reset_mekaio()
            if 'key' in result and result['key']['value']['isActive'] == True:
                title = "%s auto-reset has completed!" % bot
                reason = ''
            elif 'key' in result and result['key']['value']['isActive'] == False:
                title = "%s auto-reset failed!" % bot
                reason = "Key is not activated on any ip addresses."
            else:
                title = "%s auto-reset failed!" % bot
                reason = result
        if bot == 'Stellar':
            result = reset_stellar()
            if 'message' in result and result['message'] == 'Successfully reset license!':
                title = "%s auto-reset has completed!" % bot
                reason = ''
            elif 'message' in result and result['message'] == 'License not found.':
                title = "%s auto-reset failed!" % bot
                reason = 'License not found. Please update your information and reset manually!'
            else:
                title = "%s auto-reset failed!" % bot
                reason = result
        if bot == 'Kodai':
            result = reset_kodai()
            if 'success' in result and result['success'] == True:
                title = "%s auto-reset has completed!" % bot
                reason = ''
            elif 'success' in result and result['success'] == False:
                title = "%s auto-reset failed!" % bot
                reason = 'Kodai dashboard has a 30 mins rate limit, please try again later manually!'
            else:
                title = "%s auto-reset failed!" % bot
                reason = result
        if bot == 'Koi':
            result = reset_koi()
            if result == 'OK':
                title = "%s auto-reset has completed!" % bot
                reason = ''
            else:
                title = "%s auto-reset failed!" % bot
                reason = result

        embed = discord.Embed(title=title, url="https://www.tidalmarket.com/",
                              color=0x82111f, description=reason)
        # embed.set_author(name=)
        # embed.set_thumbnail(url="https://www.whop.io/assets/whop.png")
        # embed.add_field(name="Time:", value=time, inline=False)
        embed.add_field(name="Key:", value=key, inline=False)
        embed.add_field(name="Nickname:", value=nickname, inline=False)
        # embed.add_field(name="Time:", value=time, inline=False)
        embed.add_field(name="Check order:", value="https://www.tidalmarket.com/", inline=False)
        embed.set_footer(text="HR Space", icon_url="https://www.whop.io/assets/whop.png")

        # embed.add_field(value="欢迎来到HR Space!")
        if member is not None:
            channel = member.dm_channel
            if channel is None:
                channel = await member.create_dm()
            await channel.send(embed=embed)
        else:
            await ctx.send("None!")


def setup(bot):
    bot.add_cog(Reset_command(bot))
