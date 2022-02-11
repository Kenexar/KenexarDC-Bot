from nextcord.ext import commands, tasks
from nextcord.ext.commands import has_permissions


class MemberCounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.current_user.start()

    @tasks.loop(minutes=5)
    async def current_user(self):
        """ Server Stats are created here, its being triggerd every 10 minutes """

        cur = self.bot.dbBase.cursor()

        for server in self.bot.guilds:
            cur.execute("SELECT channel_id, channel_type FROM serverchannel WHERE server_id=%s" % server.id)
            fetcher = cur.fetchall()

            if fetcher:
                channel_count = []
                user_in_voice = []
                user_online = []

                await self.user_appender(channel_count, fetcher, user_in_voice, server)

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

                for channel in fetcher:
                    if channel[1] in [5, 6]:
                        continue

                    channel_to_edit = server.get_channel(channel[0])
                    await channel_to_edit.edit(name=channel_names[channel[1]] + str(channel_types[channel[1]]))

        cur.close()

    async def check_for_state(self, server, user_online):
        for user in server.members:
            if str(user.status) != "offline" and not user.bot:
                user_online.append(user.id)

    async def user_appender(self, channel_count, fetcher, user_in_voice, server):
        tmp_list = await self.non_valid_channel_listener(fetcher)

        for channel in server.channels:
            if 'voice' in str(channel.type) and channel.id not in tmp_list:
                await self.count_member_in_voice(channel, user_in_voice)
                channel_count.append(channel)

    async def non_valid_channel_listener(self, fetcher):
        tmp_list = []
        for entry in fetcher:
            tmp_list.append(entry[0])
        return tmp_list

    async def count_member_in_voice(self, channel, user_in_voice):
        for member in channel.members:
            user_in_voice.append(member.id)

    @commands.Command
    @has_permissions(administrator=True)
    async def create(self, ctx):
        print(ctx.message.content.split(" "))


def setup(bot):
    bot.add_cog(MemberCounter(bot))
