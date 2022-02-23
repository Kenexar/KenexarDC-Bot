from pprint import pprint

import nextcord
from nextcord.ext import commands, tasks
from nextcord.ext.commands import has_permissions
from utils.channel_listener import channel_listener

# 942103044575871040 1, 942103044575871041 2, 942103044575871042 3, 942103044575871043 4 #


class MemberCounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = await channel_listener(self.bot)
        self.current_user.start()

    @tasks.loop(minutes=10)
    async def current_user(self):
        """ Server Stats are created here, its being triggerd every 10 minutes """

        for server_id, channel in self.channel.items():
            channel_count = []
            user_in_voice = []
            user_online = []

            server = self.bot.get_guild(server_id)
            await self.user_appender(channel_count, channel, user_in_voice, server)

            await self.check_for_state(server, user_online)

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
                channel_to_edit = server.get_channel(channel_id[0])
                await channel_to_edit.edit(name=channel_names[channel_id[1]] + str(channel_types[channel_id[1]]))

    async def check_for_state(self, server, user_online):
        for user in server.members:
            if str(user.status) != "offline" and not user.bot:
                user_online.append(user.id)

    async def user_appender(self, channel_count, fetcher, user_in_voice, server):
        tmp_list = await self.server_channel_list_creator(fetcher)

        for channel in server.channels:
            if 'voice' in str(channel.type) and channel.id not in tmp_list:
                await self.count_member_in_voice(channel, user_in_voice)
                channel_count.append(channel)

    async def server_channel_list_creator(self, fetcher):
        tmp_list = []
        for entry in fetcher:
            tmp_list.append(entry[0])
        return tmp_list

    async def count_member_in_voice(self, channel, user_in_voice):
        for member in channel.members:
            user_in_voice.append(member.id)

    @commands.Command
    @has_permissions(administrator=True)
    async def create(self, ctx: commands.Context, category: str = None):
        """

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
                if len(ch.voice_channels) >= 4:
                    ch_list = ch.voice_channels[:4]
                    cur.execute(
                        "SELECT channel_id FROM dcbots.serverchannel WHERE server_id=%s and not channel_type >= 5",
                        (ctx.guild.id,))

                    fetcher = cur.fetchall()

                    for channel_id in enumerate(ch_list):
                        sql_string = "INSERT INTO dcbots.serverchannel(server_id, channel_id, channel_type) VALUES (%s, %s, %s)"
                        if fetcher:
                            sql_string = "UPDATE dcbots.serverchannel SET channel_id=%s WHERE server_id=%s AND channel_type=%s"
                        cur.execute(sql_string,
                                    (ctx.guild.id, channel_id[1].id, int(channel_id[0] + 1)))
                    self.bot.dbBase.commit()
                    cur.close()
                    return

            try:
                cur.close()
            except Exception:
                pass


def setup(bot):
    bot.add_cog(MemberCounter(bot))
