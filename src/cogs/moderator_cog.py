import discord
from discord.ext import commands
from utils import sql

class ModeratorCog(commands.Cog, name='InternshipMod'):
    """
    Contains commands that can be used by users with 'InternshipMod' role in the guild
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('InternshipMod')
    async def set_channel(self, ctx, channel: discord.TextChannel):
        """
        To set the channel where Zapier sends available internships
        """
        await sql.set_internship_channel(ctx.guild.id, channel.id)
        await ctx.send('Internships list - ' + channel.mention)

    @set_channel.error
    async def set_channel_error(self, ctx, error):
        """
        Error handler for set_channel command
        """
        if isinstance(error, commands.MissingRole):
            await ctx.send('\"InternshipMod\" role required for command.')
        else:
            await ctx.send_help(ctx.command)

def setup(bot):
    bot.add_cog(ModeratorCog(bot))
