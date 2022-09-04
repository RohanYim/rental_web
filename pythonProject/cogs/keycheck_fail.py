import discord
from discord.ext import commands


class Keycheck_fail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('admin')
    async def keycheck_fail(self, ctx, bot, key, key_nickname, reason, member: discord.Member = None, *args):
        guild = ctx.guild
        # bot = "Dashe"
        # time = "2021.06.23"
        title = "Your %s key can not be approved!" % bot
        embed = discord.Embed(title=title, url="https://www.tidalmarket.com/",
                              description="To get further support, please click the blue chat icon in the bottom right corner of HR Space website.",
                              color=0x82111f)
        # embed.set_author(name=)
        embed.set_thumbnail(url="https://www.whop.io/assets/whop.png")
        # embed.add_field(name="Bot:", value=bot, inline=False)
        embed.add_field(name="Key:", value=key, inline=False)
        embed.add_field(name="Nickname:", value=key_nickname, inline=False)
        embed.add_field(name="Reason:", value=reason, inline=False)
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
    bot.add_cog(Keycheck_fail(bot))