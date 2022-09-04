import discord
from discord.ext import commands


class Reset_seller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reset_seller(self, ctx, bot, key, nickname, time, member: discord.Member = None, *args):
        guild = ctx.guild
        # bot = "Dashe"
        # time = "2016-04-07 10:25:09"
        title = "New %s Reset Request!" % bot
        embed = discord.Embed(title=title, url="https://www.tidalmarket.com/",
                              color=0x82111f,
                              description="Please reset and confirm before %s" % time)
        # embed.set_author(name=)
        # embed.set_thumbnail(url="https://www.whop.io/assets/whop.png")
        embed.add_field(name="Key:", value=key, inline=False)
        embed.add_field(name="Nickname:", value=nickname, inline=False)
        embed.add_field(name="Please confirm here after resetting:", value="https://www.tidalmarket.com/", inline=False)
        # embed.add_field(name="Time:", value=time, inline=False)
        # embed.add_field(name="Check order:", value="https://www.tidalmarket.com/", inline=False)
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
    bot.add_cog(Reset_seller(bot))
