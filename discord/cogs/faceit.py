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


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.faceit_colors = {
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

        self.logger = None

    @commands.group(no_pm=True)
    async def get(self, ctx):
        pass

    @get.command(no_pm=True)
    async def player(self, ctx, player: str):
        fetched_player: dict = await self.bot.faceit.get_players(player_name=player)

        if not isinstance(fetched_player, dict):
            await self.logger.send(f'<@{self.bot.authorid}> Faceit API return code {fetched_player}')
            return await ctx.send('Spieler nicht gefunden, oder der Service ist momentan nicht Verfügbar')

        player_csgo: dict = fetched_player['games'].get('csgo', 'No information Provided...')
        embed = nextcord.Embed(color=self.faceit_colors.get(fetched_player['games']['csgo']['skill_level']),
                               timestamp=self.bot.current_timestamp)

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

    @commands.Cog.listener()
    async def on_interaction(self, interaction: nextcord.Interaction):
        reaction_id = interaction.data['custom_id']
        if reaction_id == 'csgo':
            username = interaction.message.embeds[0].to_dict()['author']['name']
            user = await self.bot.faceit.get_players(player_name=username)
            stats = await self.bot.faceit.get_player_stats(player_id=user['player_id'])

            embed = nextcord.Embed(timestamp=self.bot.current_timestamp,
                                   color=self.faceit_colors[user['games']['csgo']['skill_level']])

            embed.set_author(name=user['nickname'],
                             icon_url=user['avatar'],
                             url=user['faceit_url'].format(lang=user['country']))

            value_string = ''

            for k, v in stats.items():
                value_string += f'{k}: `{v}`\n'

            embed.add_field(name='Player Info',
                            value=f'Rank: `{user["games"]["csgo"]["skill_level"]}`\n'
                                  f'IG Name: `{user["games"]["csgo"]["game_player_name"]}`')

            embed.add_field(name='Player Stats',
                            value=value_string,
                            inline=False)

            await interaction.edit_original_message(embed=embed)


class FaceitRankVerification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        cur = self.bot.dbBase.cursor()
        cur.execute("SELECT server_id, channel_id from dcbots.serverchannel where channel_type=7;")
        for channel in cur.fetchall():
            ch = self.bot.get_channel(channel[1])
            embed = nextcord.Embed(title='Faceit rang Vergabe',
                                   description=f'Bitte achte darauf, dass wenn du unten auf den Knopf drückst, \ndass dein Dc Name mit deinen Faceit nick übereinstimmt!',
                                   color=self.bot.embed_st,
                                   timestamp=self.bot.current_timestamp)

            view = View()
            view.add_item(Button(style=ButtonStyle.blurple, label='Synchronize', custom_id='faceit-sync'))
            await ch.send(embed=embed, view=view)
        cur.close()

    @commands.Command
    @has_permissions(administrator=True)
    async def faceit_verify(self, ctx: commands.Context):
        channel = ctx.channel.id
        cur = self.bot.dbBase.cursor()

        cur.execute("SELECT count(*) FROM dcbots.serverchannel WHERE channel_id=%s", (channel,))
        fetcher = cur.fetchall()

        sql_string = 'INSERT INTO dcbots.serverchannel(server_id, channel_id, channel_type) VALUES (%s, %s, %s)'
        sql_params = (ctx.guild.id, channel, 7)
        if fetcher:
            sql_string = 'UPDATE dcbots.serverchannel SET channel_id=%s WHERE server_id=%s'
            sql_params = (channel, ctx.guild.id)

        cur.execute(sql_string, sql_params)
        self.bot.dbBase.commit()
        cur.close()
        await ctx.send(f'Channel <#{ctx.channel.id}> setted as faceit verify channel!')


    #### on_interaction() -- for da home

def setup(bot):
    bot.add_cog(Test(bot))
    bot.add_cog(FaceitRankVerification(bot))