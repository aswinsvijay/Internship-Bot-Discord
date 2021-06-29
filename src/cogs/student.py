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
        await ctx.message.add_reaction('🔁')
        internships = await self.bot.db.get_internships(ctx.author.id)
        embed = discord.Embed(title='Available internships')
        async for i in internships:
            embed.add_field(name=i[0], value=i[1], inline=False)
        await ctx.author.send(embed=embed, delete_after=15*60)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if str(payload.emoji) == '🔁' and message.author.id == payload.user_id:
                ctx = await self.bot.get_context(message)
                await ctx.reinvoke()

def setup(bot):
    bot.add_cog(Student(bot))
