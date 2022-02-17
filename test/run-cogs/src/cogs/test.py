from datetime import datetime, timedelta

import nextcord
from nextcord import Interaction
from nextcord.ext import commands


# from pydispatch import dispatcher


def event_handler(self, sender):
    print('signal sender', sender)


# dispatcher.connect(event_handler, signal='signal', sender=dispatcher.Any)
testingServer = 762815486823891014


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('ready')
        # dispatcher.send(signal='moo', sender='me')

    @commands.Cog.listener()
    async def on_command_error(self, ctx: nextcord.ext.commands.Context, error: nextcord.ext.commands.CommandError):
        print(ctx, error.args)
        ch = self.bot.get_channel(self.bot.log_channel)
        message = f""" 
{error}
<@{self.bot.authorid}>
               """
        await ch.send(message)

    @commands.group(no_pm=True)
    async def admin(self, ctx):
        if ctx.invoked_subcommand is None:
            print('inside')

    @commands.Command
    async def throwexception(self, ctx):
        await ctx.send(embed=nextcord.Embed(title='test', timestamp=datetime.now() + timedelta(days=2)))

    @nextcord.slash_command(name='moretesting', description='only testing some stuff', guild_ids=[testingServer])
    async def moretesting(self, interaction: Interaction):
        return await interaction.response.send_message('tes')

    @nextcord.slash_command(name='testin', description='only testing some stuff', guild_ids=[testingServer])
    async def testin(self, interaction: Interaction, timeout=None):
        return await interaction.response.send_message('tes')

    # @testin.subcommand(name='testout', description='subcommand?')
    # async def testout(self, interaction: Interaction, payload):
    #     print(payload)
    #     await interaction.response.send_message('test')
    #     return interaction.response.is_done()
    #
    # @testin.subcommand(name='testinside', description='subcommand? nr.2')
    # async def testinside(self, interaction: Interaction, payload, options):
    #     print(payload, options)
    #
    #     return await interaction.send('test')

    @admin.command(no_pm=True)
    async def testing(self, ctx):
        return await ctx.send(ctx.message.content.split()[1:])

    @commands.Command
    async def get_avatar(self, ctx: commands.Context, member: nextcord.Member):
        print(member.avatar.url)


def setup(bot):
    bot.add_cog(Test(bot))
