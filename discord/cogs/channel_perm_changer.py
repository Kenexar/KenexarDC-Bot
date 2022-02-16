from nextcord.ext import commands


#todo:
# Changeable channel sizes
# Channel Name
# Channel Current owner, Change owner, Claim owner
# Channel Info
#


class ChannelPermChanger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.changeable_perm_list = [
            'size',
            'owner',
            'claim-owner',
            'set-owner',
            'name',
            'info'
        ]

    @commands.command(name='channel')
    async def _channel(self, ctx, attr=None, *args: str):
        # Maybe subcommands?
        return await ctx.send('...Maintenance...')
        if attr not in self.changeable_perm_list:
            return await ctx.send('Command Attribut ist nicht Valide')

        try:
            member = ctx.author
            channel = ctx.author.voice.channel
        except AttributeError:
            return await ctx.send('Du must für diese aktion in einen Voice channel sein')

        if attr == 'size':
            if not len(args) == 1:
                return await ctx.send(
                    f'Du hast für diesen Befehl zu viele/zu wenig argumente angegeben, \nBeispiel: {self.bot.prefix}channel size 5')

            if not args[0].isdigit():
                return await ctx.send('Das angegebene argument ist keine Zahl !')


def setup(bot):
    bot.add_cog(ChannelPermChanger(bot))
