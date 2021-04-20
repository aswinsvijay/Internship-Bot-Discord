import discord
from discord.ext import commands
from sqlfunctions import *

class StudentCog(commands.Cog, name='Students'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def enrol(self, ctx):
        """
        To enrol yourself to this guild
        """
        await set_student_guild(ctx.author.id, ctx.guild.id)

    @commands.command()
    async def apply(self, ctx):
        """
        To get internships from enrolled guild in DM
        """
        await ctx.message.add_reaction('🔁')
        internships = await get_internships(ctx.author.id)
        embed = discord.Embed(title='Available internships')
        async for i in internships:
            embed.add_field(name=i[0], value=i[1], inline=False)
        await ctx.author.send(embed=embed, delete_after=15*60)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user != self.bot.user:
            message = reaction.message
            if reaction.emoji == '🔁' and message.author == user:
                await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(StudentCog(bot))
