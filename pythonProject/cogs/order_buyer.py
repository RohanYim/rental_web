import discord
from discord.ext import commands
import os


class Order_buyer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('admin')
    async def order_buyer(self, ctx, bot, start_time, end_time, buyer_id, member: discord.Member = None, *args):
        guild = ctx.guild
        # bot = "Dashe"
        # time = "2021.06.23"
        title = "New %s rental!" % bot
        os.system(r"python cogs\\role\\add_role.py %s %s" % (bot, buyer_id))
        embed = discord.Embed(title=title, url="https://www.tidalmarket.com/",
                              description="To get further support, please click the blue chat icon in the bottom right corner of HR Space website.",
                              color=0x82111f)
        # embed.set_author(name=)
        embed.set_thumbnail(url="https://www.whop.io/assets/whop.png")
        embed.add_field(name="Bot:", value=bot, inline=False)
        embed.add_field(name="Start Time:", value=start_time, inline=False)
        embed.add_field(name="End Time:", value=end_time, inline=False)
        embed.add_field(name="Check order:", value="https://www.tidalmarket.com/", inline=False)
        embed.set_footer(text="Thanks for using HR Space", icon_url="https://www.whop.io/assets/whop.png")

        # embed.add_field(value="欢迎来到HR Space!")

        if member is not None:
            channel = member.dm_channel
            if channel is None:
                channel = await member.create_dm()
            await channel.send(embed=embed)
        else:
            await ctx.send("None!")


def setup(bot):
    bot.add_cog(Order_buyer(bot))