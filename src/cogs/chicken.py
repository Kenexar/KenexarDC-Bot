from nextcord.ext import commands


class Chicken(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def chicken(self, ctx, *args):
        def chicken_to_minichicken(code: str) -> str:
            res = []
            code = code.lower()
            for l in code.split("\n"):
                res.append(str(l.count("chicken")))
            return " ".join(res)

        def minichicken_to_chicken(code: str) -> str:
            res = []
            for n in code.split():
                res.append(" ".join("chicken" for _ in range(int(n))))
            return "\n".join(res)


def setup(bot):
    bot.add_cog(Chicken(bot))
