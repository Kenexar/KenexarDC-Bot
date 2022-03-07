import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, CommandNotFound
from cogs.etc.config import AUTHORID


def is_owner():
    def predicate(ctx): return ctx.message.author.id == AUTHORID
    return commands.check(predicate)


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CheckFailure):
            return await ctx.send('You have no permission to do that')

        if isinstance(err, CommandNotFound):
            return await ctx.send('Command not found')

        raise err

    @commands.group(no_pm=True)
    @has_permissions(administrator=True)
    async def poll(self, ctx):
        if len(ctx.message.content.split()) == 1:
            embed = nextcord.Embed(title='Create a Poll help',
                                   color=self.bot.embed_st,
                                   timestamp=self.bot.current_timestamp())
            embed.add_field(name='To create a Normal poll',
                            value='`$poll create (title)` -> This will start the poll wizard, you can interuppt it anytime with exit',
                            inline=False)

            embed.add_field(name='To create a Yes/No poll',
                            value='`$poll yes (title) (option 1) (option 2)`',
                            inline=False)

            await ctx.send(embed=embed)

    @poll.command(no_pm=True)
    async def create(self, ctx: commands.Context):
        message = ctx.message.content.split()
        title = message[2:]

        embed = nextcord.Embed(title=title,
                               color=self.bot.embed_st,
                               timestamp=self.bot.current_timestamp())

        await ctx.send('Please send your first Option after this message, you have 60 Seconds')

        def check(m): return m.channel == ctx.channel and m.author == ctx.author

        try:
            msg = self.bot.wait_for('message', check=check, timeout=60)
        except Exception:
            return await ctx.send('Your time runned out')


def setup(bot):
    bot.add_cog(Poll(bot))
