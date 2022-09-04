import discord
from discord.ext import commands


class Reset_buyer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reset_buyer(self, ctx, bot, key, member: discord.Member = None, *args):
        guild = ctx.guild
        # bot = "Dashe"
        # time = "2016-04-07 10:25:09"
        title = "%s key has been reset!" % bot
        embed = discord.Embed(title=title, url="https://www.tidalmarket.com/",
                              color=0x82111f
                              )
        # embed.set_author(name=)
        # embed.set_thumbnail(url="https://www.whop.io/assets/whop.png")
        embed.add_field(name="Key:", value=key, inline=False)
        # embed.add_field(name="Confirm here after resetting:", value="https://www.tidalmarket.com/", inline=False)
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
    bot.add_cog(Reset_buyer(bot))
