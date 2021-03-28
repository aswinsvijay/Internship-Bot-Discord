import discord
from discord.ext import commands
from sqlfunctions import *

class ModeratorCog(commands.Cog, name='InternshipMod'):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('InternshipMod')
    async def set_channel(self,ctx):
        """
        To set the channel where Zapier sends available internships
        Usage: @InternshipBot set_channel #channel-name
        """
        if len(ctx.message.channel_mentions)==1:
            sql_set_channel(ctx.guild.id,ctx.channel.id,ctx.message.channel_mentions[0].id)
            await ctx.send('Internships list - ' + ctx.message.channel_mentions[0].mention)
        else:
            await ctx.send('''Please mention 1 channel\n@InternshipBot set_channel #channel-name''')

    @set_channel.error
    async def set_channel_error(self,ctx,error):
        if isinstance(error,commands.MissingRole):
            await ctx.send('\"InternshipMod\" role required for command.')

def setup(bot):
    bot.add_cog(ModeratorCog(bot))
