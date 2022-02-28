import random
from typing import Tuple

import nextcord
from nextcord import TextChannel, CategoryChannel, ChannelType
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
    async def define(self, ctx: commands.Context, channel_id: str):  # db channel type 8
        """ When a Channel is getting a Category, it will try to use it as the default Ticket category, otherwise when
        it is a Channel id, it will be used as the Default ticket message channel where users can create tickets.

        When the user defines a category id, the bot will NOT automatically set the tickets setting to true,
        it must be a channel id for the message.

        The Database builds up from the Category bind 0 to 25 (It is the max count of buttons that a view can have)
        the default bind is here 0 for the initial category, the decision inside the ticket to wich topic it belongs
        can be defined later in the process of creation, the command $ticket bind (category id) (category bind id)

        :param ctx: Context object that comes from discords webhook
        :type ctx: nextcord.Context
        :param channel_id: The channel/category id to process
        :type channel_id:
        :return:
        :rtype:
        """
        cur = self.bot.dbBase.cursor(buffered=True)

        if not channel_id.isdigit():
            return await ctx.send('Channel/Category id is not valid!')

        ch: TextChannel or CategoryChannel = self.bot.get_channel(int(channel_id))

        if ch.type == ChannelType.category:
            try:
                await self.__define_init_category(channel_id, ctx, cur)
                cur.close()
                return await ctx.send(f'Setted <#{channel_id}> as Initial Category', delete_after=10)
            except Exception as e:
                self.bot.logger.error(e)
                cur.close()
                return await ctx.send('Can\'t define Channel/Category, please try again or contact the Maintainer',
                                      delete_after=10)

        elif ch.type == ChannelType.text:
            try:
                ch, embed, view = await self.__create_tickets_option(channel_id, ctx, cur)
                cur.close()
                await ch.send(embed=embed, view=view)
                return await ctx.send(f'Setted <#{channel_id}> as Ticket creation channel', delete_after=10)

            except Exception as e:
                cur.close()
                self.bot.logger.error(e)
                return await ctx.send('Cant\'t define Channel/Category, please try again or contact the Maintainer',
                                      delete_after=10)

        else:
            return await ctx.send('Given id is not an Category/Text channel!', delete_after=5)

    async def __define_init_category(self, channel_id, ctx, cur):
        cur.execute("SELECT category_id FROM dcbots.tickets_serverchannel WHERE server_id=%s AND category_bind=0",
                    (ctx.guild.id,))
        fetcher = cur.fetchall()
        sql_string = "INSERT INTO dcbots.tickets_serverchannel (category_id, server_id, category_bind) VALUES (%s, %s, 0)"
        if fetcher:
            sql_string = "UPDATE dcbots.tickets_serverchannel SET category_id=%s WHERE server_id=%s"
        cur.execute(sql_string, (int(channel_id), ctx.guild.id))
        self.bot.dbBase.commit()

    async def __create_tickets_option(self, channel_id, ctx, cur):
        if ctx.guild.id not in self.bot.server_settings:
            cur.execute("INSERT INTO dcbots.server_settings(server_id, enable_ticket) VALUES (%s, %s)",
                        (ctx.guild.id, 1))

            self.bot.dbBase.commit()
            self.bot.server_settings = await filler(self.bot)
        cur.execute("SELECT channel_id FROM dcbots.serverchannel WHERE server_id=%s AND channel_type=8",
                    (ctx.guild.id,))
        fetcher = cur.fetchone()

        await self.__create_db_entry(channel_id, ctx, cur, fetcher)

        embed, view = await self.__send_ticket_message()
        ch = self.bot.get_channel(int(channel_id))
        return ch, embed, view

    async def __create_db_entry(self, channel_id, ctx, cur, fetcher):
        sql_string = "INSERT INTO dcbots.serverchannel(channel_id, server_id, channel_type) VALUES (%s, %s, %s)"

        if fetcher:
            sql_string = "UPDATE dcbots.serverchannel SET channel_id=%s WHERE server_id=%s and channel_type=%s"

        cur.execute(sql_string, (int(channel_id), ctx.guild.id, 8))
        self.bot.dbBase.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        cur = self.bot.dbBase.cursor(buffered=True)
        cur.execute("SELECT channel_id FROM dcbots.serverchannel WHERE channel_type=8")

        fetcher = cur.fetchall()
        cur.close()
        embed, view = await self.__create_ticket_message()

        for entry in fetcher:
            ch = self.bot.get_channel(entry[0])
            await ch.send(embed=embed, view=view)

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

        embed, view = await self.__create_ticket_message()

        await ch.send(embed=embed, view=view)

    async def __get_server_channel(self, ctx):
        cur = self.bot.dbBase.cursor(buffered=True)

        cur.execute("SELECT channel_id FROM dcbots.serverchannel WHERE server_id=%s AND channel_type=8",
                    (ctx.guild.id,))
        fetcher = cur.fetchall()

        cur.close()
        return fetcher

    async def __create_ticket_message(self) -> Tuple[nextcord.Embed, View]:
        embed = nextcord.Embed(title='Ticket System',
                               description="Um ein Ticket zu erstellen, drücke bitte auf den Knopf.\n\nDein anliegen kannt du im Ticket auswählen.",
                               color=self.bot.embed_st,
                               timestamp=self.bot.current_timestamp)

        embed.set_footer(text="MrPython - TicketTool")
        view = View(timeout=None)
        view.add_item(Button(style=ButtonStyle.blurple, label='Create Ticket', custom_id='ticket-creation', emoji='➕'))

        return embed, view


class TicketBackend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bot.current_ticket_list = {}

    async def __define_init_category(self, channel_id, ctx, cur):
        cur.execute("SELECT category_id FROM dcbots.tickets_serverchannel WHERE server_id=%s AND category_bind=0",
                    (ctx.guild.id,))
        fetcher = cur.fetchall()
        sql_string = "INSERT INTO dcbots.tickets_serverchannel (category_id, server_id, category_bind) VALUES (%s, %s, 0)"
        if fetcher:
            sql_string = "UPDATE dcbots.tickets_serverchannel SET category_id=%s WHERE server_id=%s"

        cur.execute(sql_string, (int(channel_id), ctx.guild.id))
        self.bot.dbBase.commit()

    @commands.Cog.listener()
    async def on_interaction(self, interaction: nextcord.Interaction):
        i_id = interaction.data.get('custom_id', 'custom_id')
        cur = self.bot.dbBase.cursor()

        if i_id == 'ticket-creation':
            cur.execute("SELECT category_id FROM dcbots.tickets_serverchannel WHERE server_id=%s AND category_bind=%s",
                        (interaction.guild.id, 0))

            fetcher = cur.fetchall()
            guild: nextcord.Guild = interaction.guild

            if fetcher:
                category: nextcord.CategoryChannel = self.bot.get_channel(fetcher[0][0])
                ch = await guild.create_text_channel(name=f"Ticket-{random.randint(0, 65535)}", category=category)
            else:
                ch = await guild.create_text_channel(name=f"Ticket-{random.randint(0, 65535)}")

            await ch.set_permissions(interaction.user, view_channel=True, send_messages=True, read_messages=True)

            cur.execute("SELECT category_bind, button_emoji, button_label FROM dcbots.ticket_button_options WHERE server_id=%s", (guild.id,))
            fetcher = cur.fetchall()

            view = TicketBaseView()
            for btn in fetcher:
                view.add_item(Button(label=f'{btn[0]}: {btn[2]}', emoji=str(btn[1]), style=ButtonStyle.blurple))

            await ch.send("Message", view=view)


class TicketBaseView(View):
    @nextcord.ui.button(label='Rename', emoji='📝', style=ButtonStyle.blurple, row=4)
    async def rename(self, button: Button, interaction: nextcord.Interaction):
        button.disabled = True
        button.style = ButtonStyle.gray
        await interaction.response.edit_message(view=self)

    @nextcord.ui.button(label='Close', emoji='🔒', custom_id='close-ticket', style=ButtonStyle.danger, row=4)
    async def close(self, button: Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(view=TicketDeleteView())


class TicketDeleteView(View):
    @nextcord.ui.button(label='Delete it', style=ButtonStyle.danger)
    async def delete_it(self, button: Button, interaction: nextcord.Interaction):
        ch: nextcord.TextChannel = interaction.channel

        m = await ch.send('Ticket will be closed...')
        await m.add_reaction('<:monaloadingdark:915863386196181014>')

        await ch.edit(sync_permissions=True)
        await ch.send(f'{interaction.user.mention} closed the ticket')
        await ch.send(embed=nextcord.Embed(title='`Team Controls`'), view=TicketEndView())

    @nextcord.ui.button(label='Cancel', style=ButtonStyle.blurple)
    async def cancel(self, button: Button, interaction: nextcord.Interaction):
        await interaction.response.delete_original_message()


class TicketEndView(View):
    @nextcord.ui.button(label='Delete', emoji='🗑️', style=ButtonStyle.danger)
    async def delete_it(self, button: Button, interaction: nextcord.Interaction):
        ch: nextcord.TextChannel = interaction.channel

        m = await ch.send('Ticket will be deleted...')
        await m.add_reaction('<:monaloadingdark:915863386196181014>')

        await ch.delete()

    @nextcord.ui.button(label='Re-Open', emoji='🔓', style=ButtonStyle.blurple)
    async def cancel(self, button: Button, interaction: nextcord.Interaction):
        await interaction.response.delete_original_message()

    @nextcord.ui.button(label='Archive and Delete', emoji='🗒️', style=ButtonStyle.blurple)
    async def cancel(self, button: Button, interaction: nextcord.Interaction):
        await interaction.channel.delete()


def setup(bot):
    bot.add_cog(Ticket(bot))
    bot.add_cog(TicketBackend(bot))
