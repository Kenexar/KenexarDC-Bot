import datetime
from typing import Dict, List

import nextcord
from nextcord import ButtonStyle
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, CommandNotFound
from cogs.etc.config import AUTHORID
from nextcord.ui import View, Button


def is_owner():
    def predicate(ctx): return ctx.message.author.id == AUTHORID
    return commands.check(predicate)


async def send_interaction_msg(message: str, interaction: nextcord.Interaction, tmp=True):
    try:
        await interaction.followup.send(message, ephemeral=tmp)
    except Exception as e:
        print(e)


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
            embed.add_field(name='Create a normal poll, this poll can take up to 7 options',
                            value='`$poll (title) ~Option 1 ~Option 2 ...` -> The `~` is used to Space the options, so please use it carefully',
                            inline=False)

            embed.add_field(name='To create a Yes/No poll',
                            value='`$poll (title)`',
                            inline=False)

            await ctx.send(embed=embed)
            return

        numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

        message_content = ctx.message.content[6:].split('~')
        title = message_content[0]
        options = message_content[1:]

        if len(options) > 9:
            return await ctx.send('You passed to many Options, Please be in a range from 2-9')

        if len(options) < 2:
            return await ctx.send('You\'ve submitted fewer Options as you should, the Poll can\'t be startet. The range is 2-9')

        des = ''
        view = View(timeout=None)

        for i in enumerate(options):
            des += f'{numbers[i[0]]} : {i[1].lstrip()}\n'
            view.add_item(Button(emoji=numbers[i[0]], style=ButtonStyle.blurple, custom_id=f'poll-btn-{i[0]}'))

        embed = nextcord.Embed(title=title,
                               description=des,
                               color=self.bot.embed_st,
                               timestamp=datetime.datetime.now() + datetime.timedelta(days=-2))
        embed.set_footer(text='Deadline ')

        await ctx.send(embed=embed, view=view)


class PollBackend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.current_polls = {}  # {'channel_id': [user_id]}

    @commands.Cog.listener()
    async def on_interaction(self, interaction: nextcord.Interaction):
        c_id = interaction.data.get('custom_id', 'custom_id')

        if 'poll-btn-' not in c_id:
            return

        message: nextcord.Message = interaction.message

        if (message.embeds[0].timestamp - message.created_at).total_seconds() < 0:
            return await send_interaction_msg('This poll has reached it\'s Deadline', interaction)

        if interaction.channel_id not in self.current_polls:
            self.current_polls[interaction.channel_id] = []

        if interaction.user.id in self.current_polls[interaction.channel_id]:
            return await send_interaction_msg('You have already voted.', interaction)

        self.current_polls[interaction.channel_id].append(interaction.user.id)


def setup(bot):
    bot.add_cog(Poll(bot))
    bot.add_cog(PollBackend(bot))
