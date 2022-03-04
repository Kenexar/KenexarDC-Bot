import nextcord
from mcstatus import MinecraftServer
from nextcord.ext import commands


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def MCstatus(self, ctx):
        message = ctx.message
        emoji = "<a:loading:859832585483845714>"
        user = self.bot.user

        await message.add_reaction(emoji)

        embed = nextcord.Embed(title="Minecraft Server status")

        embed.add_field(name="IP:  `Kenexar.eu`", value="--------------------------------------", inline=False)

        embed.add_field(name="Proxy:", value=await self.__get_server_status("161.97.113.149:25577"), inline=False)
        embed.add_field(name="Lobby:", value=await self.__get_server_status("161.97.113.149:10010"), inline=True)
        embed.add_field(name="Challenge-01:", value=await self.__get_server_status("161.97.113.149:10020"), inline=True)
        embed.add_field(name="Survival-01:", value=await self.__get_server_status("161.97.113.149:10030"), inline=False)

        embed.colour = nextcord.Color.red()

        if await self.__get_server_status("161.97.113.149:25577") == "Online":
            embed.colour = nextcord.Color.brand_green()

        await message.remove_reaction(emoji, user)

        return await ctx.send(embed=embed)

    async def __get_server_status(self, ip):
        server = MinecraftServer.lookup(ip)
        try:
            status = server.status()
        except Exception:
            status = None

        status_string = "Offline"

        if status:
            status_string = "Online"

        return status_string


def setup(bot):
    bot.add_cog(Minecraft(bot))
