import nextcord
from nextcord.ext import commands, tasks
from nextcord.ext.commands import has_permissions

from cogs.etc.config import dbBase


class MemberCounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.current_user.start()

    @tasks.loop(minutes=10)
    async def current_user(self):
        """ here comes the current user count on the server """

        cur = dbBase.cursor()

        for server in self.bot.guilds:
            cur.execute("SELECT channel_id, channel_type FROM serverchannel WHERE server_id=%s" % server.id)
            fetcher = cur.fetchall()

            if fetcher:
                channel_count = []
                member_count = []
                user_online = []

                for channel in server.channels:
                    if 'voice' in str(channel.type):
                        for member in channel.members:
                            member_count.append(member.id)
                        channel_count.append(channel)

                for user in server.members:
                    if str(user.status) != "offline":
                        user_online.append(user.id)

                channel_types = {
                    1: server.member_count,
                    2: len(user_online),
                    3: len(member_count),
                    4: len(channel_count),
                }

                channel_names = {
                    1: '┌ Userzahl: ',
                    2: '├ Online: ',
                    3: '├ User im Voice: ',
                    4: '└ Voicechannel: ',
                }

                for channel in fetcher:
                    channel_to_edit = server.get_channel(channel[0])
                    await channel_to_edit.edit(name=channel_names[channel[1]] + str(channel_types[channel[1]]))

        cur.close()

    @commands.Command
    @has_permissions(administrator=True)
    async def set(self, ctx):
        print(ctx.message.content.split(" "))


def setup(bot):
    bot.add_cog(MemberCounter(bot))
