import asyncio

import nextcord
from kenutils.src.core import channel_listener
from mysql.connector import InternalError
from nextcord.ext import commands, tasks
from nextcord.ext.commands import has_permissions


async def check_for_state(server, user_online):
    for user in server.members:
        if str(user.status) != "offline" and not user.bot:
            user_online.append(user.id)


async def server_channel_list_creator(fetcher):
    tmp_list = []
    for entry in fetcher:
        tmp_list.append(entry[0])
    return tmp_list


async def count_member_in_voice(channel, user_in_voice):
    for member in channel.members:
        user_in_voice.append(member.id)


class MemberCounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = await channel_listener(self.bot)
        self.current_user.start()

    @tasks.loop(minutes=5)
    async def current_user(self):
        """ Server Stats are created here, its being triggerd every 10 minutes """

        for server_id, channel in self.channel.items():
            channel_count = []
            user_in_voice = []
            user_online = []

            server = self.bot.get_guild(server_id)
            await self.user_appender(channel_count, channel, user_in_voice, server)

            await check_for_state(server, user_online)

            channel_types = {
                1: server.member_count,
                2: len(user_online),
                3: len(user_in_voice),
                4: len(channel_count),
            }

            channel_names = {
                1: '┌ Userzahl: ',
                2: '├ Online: ',
                3: '├ User im Voice: ',
                4: '└ Voicechannel: ',
            }

            for channel_id in channel:
                channel_to_edit = self.bot.get_channel(channel_id[0])
                await asyncio.sleep(1)

                try:
                    await channel_to_edit.edit(name=channel_names[channel_id[1]] + str(channel_types[channel_id[1]]))
                except Exception as e:
                    self.bot.logger.error(e)

    async def user_appender(self, channel_count, fetcher, user_in_voice, server):
        tmp_list = await server_channel_list_creator(fetcher)

        for channel in server.channels:
            if 'voice' in str(channel.type) and channel.id not in tmp_list:
                await count_member_in_voice(channel, user_in_voice)
                channel_count.append(channel)

    @commands.Command
    @has_permissions(administrator=True)
    async def mccreate(self, ctx: commands.Context, category: str = None):
        """ Member Counter creator

        :param ctx:
        :type ctx:
        :param category:
        :type category:
        :return:
        :rtype:
        """
        if category and category.isdigit():
            cur = self.bot.dbBase.cursor(buffered=True)

            ch: nextcord.CategoryChannel = self.bot.get_channel(int(category))
            if ch.type == nextcord.ChannelType.category:
                if len(ch.voice_channels) <= 4:
                    for i in range(5):
                        if not len(ch.voice_channels) >= 4:
                            await ch.create_voice_channel(name='test ' + str(i))

                if len(ch.voice_channels) >= 4:
                    ch_list = ch.voice_channels[:4]
                    cur.execute(
                        "DELETE FROM dcbots.serverchannel WHERE server_id=%s and not channel_type >= 5",
                        (ctx.guild.id,))
                    self.bot.dbBase.commit()

                    for channel_id in enumerate(ch_list):
                        sql_string = "INSERT INTO dcbots.serverchannel(server_id, channel_id, channel_type) VALUES (%s, %s, %s)"

                        cur.execute(sql_string,
                                    (ctx.guild.id, channel_id[1].id, int(channel_id[0] + 1)))
                    self.bot.dbBase.commit()
                    cur.close()
                    self.channel = await channel_listener(self.bot)
                    return

            try:
                cur.close()
                self.channel = await channel_listener(self.bot)
            except InternalError:
                pass
            except Exception as e:
                self.bot.logger.error(f'Error at poll:129\n{e}')


def setup(bot):
    bot.add_cog(MemberCounter(bot))
