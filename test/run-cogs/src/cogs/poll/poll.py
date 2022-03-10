import datetime
from typing import Dict, List

import nextcord
from nextcord.ext import tasks
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


numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']


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

        message_content = ctx.message.content[6:].split('~')
        title = message_content[0]
        options = message_content[1:]

        if not options:
            options += ['yes', 'no']

        if len(options) > 9:
            return await ctx.send('You passed to many Options, Please be in a range from 2-9')

        if len(options) < 2:
            return await ctx.send('You\'ve submitted fewer Options as you should, the Poll can\'t be startet. The range is 2-9')

        des = ''
        view = View(timeout=None)  # (24*60*60)*2

        for i in enumerate(options):
            des += f'{numbers[i[0]]} : {i[1].strip()} - `Votes: 0`\n'
            view.add_item(Button(emoji=numbers[i[0]], style=ButtonStyle.blurple, custom_id=f'poll-btn-{i[0]}'))

        embed = nextcord.Embed(title=title,
                               description=des,
                               color=self.bot.embed_st,
                               timestamp=datetime.datetime.now() + datetime.timedelta(minutes=1))
        embed.set_footer(text='Deadline ')

        await ctx.send(embed=embed, view=view)


class PollBackend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.current_polls = {}  # {message_id: {'message_id', message_id, 'user': [user_id], 'votes': {'1': 1, '2': 2}}}

        self.poll_cleaner.start()

    @tasks.loop(seconds=90)
    async def poll_cleaner(self):
        tmp = []
        for i, v in self.current_polls.items():
            ch: nextcord.TextChannel = self.bot.get_channel(v['channel_id'])
            msg: nextcord.Message = await ch.fetch_message(i)
            if msg:
                embed = msg.embeds[0]
                embed_timestamp = datetime.datetime.timestamp(embed.timestamp)
                current = datetime.datetime.timestamp(datetime.datetime.now())

                if embed_timestamp > current:
                    continue

                embed.title = f'{embed.title} - Ended'
                await msg.edit(embed=embed, view=View().clear_items())
            tmp.append(i)

        for i in tmp:
            self.current_polls.pop(i)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: nextcord.Interaction):
        c_id = interaction.data.get('custom_id', 'custom_id')

        if 'poll-btn-' not in c_id:
            return

        message: nextcord.Message = interaction.message

        embed_timestamp = datetime.datetime.timestamp(message.embeds[0].timestamp)
        current = datetime.datetime.timestamp(datetime.datetime.now())

        if embed_timestamp < current:
            return await send_interaction_msg('This poll has reached it\'s Deadline', interaction)

        content = message.embeds[0].description.split('\n')

        if message.id not in self.current_polls:
            self.current_polls[message.id] = {'channel_id': message.channel.id, 'user': [], 'votes': {str(i): 0 for i in range(len(content))}}

        if interaction.user.id in self.current_polls[message.id]['user']:
            return await send_interaction_msg('You have already voted.', interaction)

        self.current_polls[message.id]['user'].append(interaction.user.id)
        content_reassemble = []
        self.current_polls[message.id]['votes'][c_id[-1:]] += 1

        for cc in enumerate(content):
            cd = cc[1][6:cc[1].rfind('`Votes:')]
            # Re-Assemble the broken up string, it could be done better but at my position, I dont wanna do that now, mabye I do it, when I clean up the code :)
            content_reassemble.append(f'{numbers[cc[0]]} : {cd}`Votes: {self.current_polls[message.id]["votes"][str(cc[0])]}`\n')

        embed = nextcord.Embed(title=message.embeds[0].title,
                               description=''.join(content_reassemble),
                               color=self.bot.embed_st,
                               timestamp=message.embeds[0].timestamp)

        embed.set_footer(text='Deadline ')
        await interaction.message.edit(embed=embed)


def setup(bot):
    bot.add_cog(Poll(bot))
    bot.add_cog(PollBackend(bot))
