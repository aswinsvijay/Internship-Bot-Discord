import discord
from discord.ext import commands

class CommandsCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def set_channel(self,ctx):
        """
        To set the channel where Zapier sends available internships
        Usage: @InternshipBot set_channel #channel-name
        """
        if len(ctx.message.channel_mentions)==1:
            await ctx.send('Internships list - ' + ctx.message.channel_mentions[0].mention)
            print(type(ctx.message.channel_mentions[0]))
        else:
            await ctx.send('''Please mention 1 channel\n@InternshipBot set_channel #channel-name''')

def setup(bot):
    bot.add_cog(CommandsCog(bot))
