from nextcord.ext import commands


class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bj_cards = {
            'hearts': {'ace': '🂱', 2: '🂲', 3: '🂳', 4: '🂴', 5: '🂵', 6: '🂶', 7: '🂷', 8: '🂸', 9: '🂹', 10: '🂺',
                       'jack': '🂻', 'queen': '🂽', 'king': '🂾'},

            'spades': {'ace': '🂡', 2: '🂢', 3: '🂣', 4: '🂤', 5: '🂥', 6: '🂦', 7: '🂧', 8: '🂨', 9: '🂩', 10: '🂪',
                       'jack': '🂫', 'queen': '🂭', 'king': '🂮'},

            'diamonds': {'ace': '🃁', 2: '🃂', 3: '🃃', 4: '🃄', 5: '🃅', 6: '🃆', 7: '🃇', 8: '🃈', 9: '🃉', 10: '🃊',
                         'jack': '🃋', 'queen': '🃍', 'king': '🃎'},

            'clubs': {'ace': '🃑', 2: '🃒', 3: '🃓', 4: '🃔', 5: '🃕', 6: '🃖', 7: '🃗', 8: '🃘', 9: '🃙', 10: '🃚',
                      'jack': '🃛', 'queen': '🃝', 'king': '🃞'},
            'back': '🂠'}

    @commands.command(aliases=['bj'])
    async def blackjack(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Casino(bot))
