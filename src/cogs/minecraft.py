import discord
from mcstatus import MinecraftServer
from nextcord.ext import commands


class minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def status(self, ctx):

        message = ctx.message
        emoji = "<a:loading:859832585483845714>"
        user = self.bot.user

        await message.add_reaction(emoji)

        embed = discord.Embed(title="Minecraft Server status")

        embed.add_field(name="IP:  ```Kenexar.eu```", value="--------------------------------------", inline=False)

        embed.add_field(name="Proxy:", value=self.getServerStatus("161.97.113.149:25577"), inline=False)
        embed.add_field(name="Lobby:", value=self.getServerStatus("161.97.113.149:10010"), inline=True)
        embed.add_field(name="Challenge-01:", value=self.getServerStatus("161.97.113.149:10020"), inline=True)
        embed.add_field(name="Survival-01:", value=self.getServerStatus("161.97.113.149:10030"), inline=False)

        embed.color = discord.Color.red()

        if self.getServerStatus("161.97.113.149:25577") == "Online":
            embed.color = discord.Color.brand_green()

        await message.remove_reaction(emoji, user)

        return await ctx.send(embed=embed)

    @staticmethod
    def getServerStatus(ip):
        server = MinecraftServer.lookup(ip)
        try:
            status = server.status()
        except Exception as e:
            status = None

        statusString = "Offline"

        if status is not None:
            statusString = "Online"

        return statusString


def setup(bot):
    bot.add_cog(minecraft(bot))
