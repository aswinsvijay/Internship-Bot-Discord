import discord
from discord.ext import commands

class Owner(commands.Cog, name='Owner'):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await commands.is_owner().predicate(ctx)

    @commands.command(aliases=['exts'])
    async def extensions(self, ctx):
        await ctx.send('\n'.join(ext for ext in self.bot.extensions))

    @commands.command()
    async def load(self, ctx, cog):
        self.bot.load_extension(f'cogs.{cog}')

    @commands.command()
    async def unload(self, ctx, cog):
        self.bot.unload_extension(f'cogs.{cog}')

    @commands.command()
    async def reload(self, ctx, cog):
        self.bot.reload_extension(f'cogs.{cog}')

def setup(bot):
    bot.add_cog(Owner(bot))
