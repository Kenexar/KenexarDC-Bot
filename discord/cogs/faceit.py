import nextcord
from nextcord import ButtonStyle
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from nextcord.ui import Button, Item
from nextcord.ui import View


class ViewTimeOuter(View):
    def __init__(self, ctx, embed):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.embed = embed

    async def on_timeout(self): return

    async def on_error(self, error: Exception, item: Item, interaction: nextcord.Interaction): return


class Faceit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.logger = None

        self.bot.faceit_colors = {
            1: 0xffffff,
            2: 0x77ff00,
            3: 0x77ff00,
            4: 0xffe100,
            5: 0xffe100,
            6: 0xffe100,
            7: 0xffe100,
            8: 0xe30000,
            9: 0xe30000,
            10: 0xe30000,
        }

    @commands.group(no_pm=True)
    async def faceit(self, ctx):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger = self.bot.get_channel(self.bot.log_channel)

    @faceit.command(no_pm=True)
    async def player(self, ctx, player: str):
        fetched_player: dict = await self.bot.faceit.get_players(player_name=player)

        if not isinstance(fetched_player, dict):
            self.bot.logger.error(f'FaceitAPI: ret code: {fetched_player}')
            await self.logger.send(f'<@{self.bot.authorid}> Faceit API return code {fetched_player}')
            return await ctx.send('Spieler nicht gefunden, oder der Service ist momentan nicht Verfügbar')

        player_csgo: dict = fetched_player['games'].get('csgo', 'No information Provided...')
        embed = nextcord.Embed(color=self.bot.faceit_colors.get(fetched_player['games']['csgo']['skill_level']),
                               timestamp=self.bot.current_timestamp())

        embed.set_author(name=fetched_player['nickname'],
                         url=fetched_player['faceit_url'].format(lang=fetched_player['country']),
                         icon_url=fetched_player['avatar'])

        embed.add_field(name='Information',
                        value=f'Region: `{player_csgo["region"]}`\n'
                              f'Rank: `{player_csgo["skill_level"]}`\n'
                              f'Faceit elo: `{player_csgo["faceit_elo"]}`\n'
                              f'IG Name: `{player_csgo["game_player_name"]}`\n'
                              f'[Profile]({fetched_player["faceit_url"].format(lang=fetched_player["country"])})',
                        inline=False)

        view = ViewTimeOuter(ctx, embed)
        view.add_item(Button(label='CS:GO Stats', style=ButtonStyle.blurple, custom_id=f'csgo'))

        return await ctx.send(embed=embed, view=view)


class FaceitRankVerification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        cur = self.bot.dbBase.cursor()
        cur.execute("SELECT server_id, channel_id from dcbots.serverchannel where channel_type=7;")
        for channel in cur.fetchall():
            ch, embed, view = await self.send_faceit_verify_message(channel)
            await ch.send(embed=embed, view=view)
        cur.close()

    async def send_faceit_verify_message(self, channel):
        ch: nextcord.TextChannel = self.bot.get_channel(channel[1])
        await ch.purge()
        embed = nextcord.Embed(title='Faceit rang Vergabe',
                               description=f'Bitte achte darauf, dass wenn du unten auf den Knopf drückst, \ndass dein Dc Name mit deinen Faceit nick übereinstimmt!\n\nSollte sich dein Rang in laufe der Zeit ändern, drück einfach nochmal drauf',
                               color=self.bot.embed_st,
                               timestamp=self.bot.current_timestamp())
        view = View()
        view.add_item(Button(style=ButtonStyle.blurple, label='Synchronize', custom_id='faceit-sync'))
        return ch, embed, view

    @commands.Command
    @has_permissions(administrator=True)
    async def faceit_verify(self, ctx: commands.Context):
        channel = ctx.channel.id
        cur = self.bot.dbBase.cursor()

        cur.execute("SELECT count(*) FROM dcbots.serverchannel WHERE channel_id=%s", (channel,))
        fetcher = cur.fetchall()

        sql_string = 'INSERT INTO dcbots.serverchannel(server_id, channel_id, channel_type) VALUES (%s, %s, %s)'
        sql_params = (ctx.guild.id, channel, 7)
        if fetcher[0][0]:
            sql_string = 'UPDATE dcbots.serverchannel SET channel_id=%s WHERE server_id=%s'
            sql_params = (channel, ctx.guild.id)

        cur.execute(sql_string, sql_params)
        self.bot.dbBase.commit()
        cur.close()
        await ctx.send(f'Channel <#{ctx.channel.id}> setted as faceit verify channel!')
        ch, embed, view = await self.send_faceit_verify_message((0, ctx.channel.id))
        await ctx.send(embed=embed, view=view)


def setup(bot):
    bot.add_cog(Faceit(bot))
    bot.add_cog(FaceitRankVerification(bot))
