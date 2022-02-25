from typing import Tuple

import nextcord
from nextcord import ButtonStyle
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from nextcord.ui import View, Button
from utils.checker import filler


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(no_pm=True)
    @has_permissions(administrator=True)
    async def ticket(self, ctx):
        pass

    @ticket.command(no_pm=True)
    async def define(self, ctx, channel_id):  # db channeltype 8
        cur = self.bot.dbBase.cursor(buffered=True)

        if ctx.guild.id not in self.bot.server_settings:
            cur.execute("INSERT INTO dcbots.server_settings(server_id, enable_ticket) VALUES (%s, %s)",
                        (ctx.guild.id, 1))

            self.bot.dbBase.commit()
            self.bot.server_settings = await filler(self.bot)

    @ticket.command(no_pm=True)
    async def send(self, ctx: commands.Context):
        if ctx.guild.id not in self.bot.server_settings:
            return await ctx.send('The Server have Currently no Configuration', delete_after=5)

        if not self.bot.server_settings[ctx.guild.id].get('enable_ticket'):
            return await ctx.send('The TicketTool is not enabled!', delete_after=5)

        fetcher = await self.__get_server_channel(ctx)

        if not fetcher:  # somehow lol
            return await ctx.send('No channel for the Tickets defined!', delete_after=5)

        ch = self.bot.get_channel(fetcher[0][0])

        embed, view = await self.__send_ticket_message()
        try:
            await ch.send(embed=embed, view=view)
        except Exception:
            pass

    async def __get_server_channel(self, ctx):
        cur = self.bot.dbBase.cursor(buffered=True)

        cur.execute("SELECT channel_id FROM dcbots.serverchannel WHERE server_id=%s AND channel_type=8",
                    (ctx.guild.id,))
        fetcher = cur.fetchall()

        cur.close()
        return fetcher

    async def __send_ticket_message(self) -> Tuple[nextcord.Embed, View]:
        embed = nextcord.Embed(title='Ticket System',
                               description="Um ein Ticket zu erstellen, drücke bitte auf den Knopf.\n\nDein anliegen kannt du im Ticket auswählen.",
                               timestamp=self.bot.current_timestamp)
        embed.set_footer(text="MrPython - TicketTool")
        view = View()
        view.add_item(Button(style=ButtonStyle.blurple, label='Create Ticket', custom_id='ticket-creation', emoji=':heavy_plus_sign:'))

        return embed, view


def setup(bot):
    bot.add_cog(Ticket(bot))
