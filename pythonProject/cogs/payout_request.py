import discord
from discord.ext import commands


class Payout_request(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('admin')
    async def payout_request(self, ctx, amount, method, member: discord.Member = None, *args):
        guild = ctx.guild
        # bot = "Dashe"
        # time = "2021.06.23"
        title = "We have received your withdrawal request!"
        embed = discord.Embed(title=title, url="https://www.tidalmarket.com/",
                              description="Your withdrawal request will be confirmed in 48 hours.",
                              color=0x82111f)
        # embed.set_author(name=)
        embed.set_thumbnail(url="https://www.whop.io/assets/whop.png")
        # embed.add_field(name="Bot:", value=bot, inline=False)
        embed.add_field(name="Amount:", value=amount, inline=False)
        embed.add_field(name="Method:", value=method, inline=False)
        # embed.add_field(name="Check order:", value="https://www.tidalmarket.com/", inline=False)
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
    bot.add_cog(Payout_request(bot))