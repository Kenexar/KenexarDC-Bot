from nextcord.ext import commands
import nextcord
from nextcord.ext.commands import has_permissions
from nextcord.ui import Modal, TextInput
import random


async def send_interaction_msg(message: str, interaction: nextcord.Interaction, tmp=True):
    """ Sends this pop-up message for special users only """
    try:
        await interaction.followup.send(message, ephemeral=tmp)
    except Exception as e:
        print(e)


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.cursed_list = {
            'test': 't̴e̶s̸t̶',
            'ludwig': 'L̸u̸d̶w̸i̷g̵',
            'historyv': 'h̸i̴s̶t̸o̵r̶y̵v̶',
            'till': 'T̸i̸l̶l̵',
            'lakker': 'l̴a̷k̴k̶e̶r̷',
            'twitch': 'T̷w̸i̷t̷c̷h̵',
            'burak': 'b̸u̵r̸a̸k̵',
            'yeet': 'y̶e̶e̶t̷',
        }

        self.verify_user = {}

    @commands.group()
    @has_permissions(administrator=True)
    async def verify(self, ctx):
        pass

    @verify.command()
    async def send(self, ctx):
        pass

    @commands.Cog.listener()
    async def on_interaction(self, inter: nextcord.Interaction):
        c_id = inter.data.get('custom_id')

        if c_id == 'verify':
            modal = Modal(title='Verification', custom_id='verify-modal')
            choice = random.choice(list(self.cursed_list.keys()))
            word = self.cursed_list.get(choice, "test")

            self.verify_user[inter.user.id] = choice

            modal.add_item(TextInput(label=f'{word} - Captcha', custom_id='Tests'))
            await inter.response.send_modal(modal)
            return

        if c_id == 'verify-modal':
            comp = inter.data.get('components')
            value = comp[0]['components'][0]['value']
            compare = self.verify_user[inter.user.id]

            if not value.lower() == compare.lower():
                await send_interaction_msg('Du hast die Verifikation leider nicht Geschafft. Probier es noch einmal.',
                                           inter)
                return

            await send_interaction_msg(
                'Du hast die Verifikation erfolgreich bestanden, in kürze solltest du deine Rolle bekommen.', inter)


def setup(bot):
    bot.add_cog(Verify(bot))
