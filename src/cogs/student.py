import discord
from discord.ext import commands

class Student(commands.Cog, name='Students'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def enrol(self, ctx):
        """
        To enrol yourself to this guild
        """
        await self.bot.db.set_student_guild(ctx.author.id, ctx.guild.id)

    @commands.command()
    @commands.cooldown(1, 15*60, commands.BucketType.user)
    async def apply(self, ctx):
        """
        To get internships from enrolled guild in DM
        """
        internships = await self.bot.db.get_internships(ctx.author.id)
        embed = discord.Embed(title='Available internships')
        async for i in internships:
            embed.add_field(name=i[0], value=i[1], inline=False)
        await ctx.author.send(embed=embed, delete_after=15*60)

def setup(bot):
    bot.add_cog(Student(bot))
