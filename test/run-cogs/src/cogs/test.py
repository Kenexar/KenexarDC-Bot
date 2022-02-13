from nextcord.ext import commands
from nextcord.ui import View


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        ch = self.bot.get_channel(939179519955320902)
        view = View()
        async for message in ch.history():
            if not message.components:
                continue

            new_view = view.from_message(message)
            origin_view = view.from_message(message)
            new_view.clear_items()

            await message.edit(view=new_view)
            await message.edit(view=origin_view)



def setup(bot):
    bot.add_cog(Test(bot))
