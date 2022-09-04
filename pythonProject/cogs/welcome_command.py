import discord
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def welcome(self, ctx, member: discord.Member = None, *args):
        guild = ctx.guild

        embed = discord.Embed(title="Welcome to HR Space", url="https://www.tidalmarket.com/",
                              description="To get further support, please click the blue chat icon in the bottom right corner of HR Space website.",
                              color=discord.Colour.purple())
        # embed.set_author(name=)
        embed.set_thumbnail(url="https://www.whop.io/assets/whop.png")
        embed.add_field(name="Start to rent:", value="https://www.tidalmarket.com/", inline=False)
        embed.add_field(name="To be a seller:", value="https://www.tidalmarket.com/", inline=False)
        embed.add_field(name="Guide and Document:", value="https://www.tidalmarket.com/", inline=False)
        embed.set_footer(text="Made by HR Space", icon_url="https://www.whop.io/assets/whop.png")

        # embed.add_field(value="欢迎来到HR Space!")

        if member is not None:
            channel = member.dm_channel
            if channel is None:
                channel = await member.create_dm()
            await channel.send(embed=embed)
        else:
            await ctx.send("None!")


def setup(bot):
    bot.add_cog(Welcome(bot))