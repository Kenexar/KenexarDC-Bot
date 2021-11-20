import json

from datetime import datetime

from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound

from cogs.etc.config import ESCAPE, cur, DBESSENT
from cogs.etc.embeds import user_info


# todo:
#   get, del, add, clear
#       getUser
#       getVehicleTrunk
#       delUser
#       delVehicles
#       delWeapon
#       clearWeapons
#       clearInventory
#       clearVehicleTrunk
#       clearUserMoney
#       addUserMoney


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Ready at {datetime.now().strftime("%H:%M:%S")}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx,
                               error):  # Function doing intense computing!
        if isinstance(error, CommandNotFound):
            return await ctx.send("Command/API not found.")
        raise error

    @staticmethod
    def parser(rounds, toParse, option) -> list or None:
        """ This is a small self written Argparser

        This Function parse given Arguments for administration

        :param rounds: Insert the max number of words for the return
        :param toParse: Gives the Arg to Parse
        :param option: Insert option for parsing


        :return: list
        """

        return_list = []

        if ESCAPE + toParse in option:
            for i in range(rounds):
                return_list.append(i)
            return return_list
        return None

    @commands.Command
    async def get(self, ctx, *args):
        cur.execute(DBESSENT)

        options = [
            f'{ESCAPE}user', f'{ESCAPE}u',
            f'{ESCAPE}vehicletrunk', f'{ESCAPE}vh', 'Null']

        cur.execute(
            "SELECT identifier, `accounts`, `group`, inventory, job, job_grade, loadout, firstname, lastname, phone_number FROM users WHERE identifier='3bf55e0c0deca54563461985c94f13694a0ad919'")

        fetcher = cur.fetchone()

        money = json.loads(fetcher[1])
        inventory = json.loads(fetcher[3].strip('"'))
        weapons = json.loads(fetcher[6])

        weapons_list = []

        for i in weapons:
            to_add = ''
            to_add.join(f'{i} {weapons[i]["ammo"]}/255')
            print(to_add)

        user = {
            'username': 'clx',
            'license': 'coggers',
            'job': fetcher[4],
            'job_grade': fetcher[5],
            'cash': money.get('money'),
            'bank': money.get('bank'),
            'bm': money.get('black_money'),
            'veh': '',
            'weapons': weapons_list,
            'inv': inventory,
            'firstname': fetcher[7],
            'lastname': fetcher[8],
            'phone_number': fetcher[9]
        }

        await ctx.send(embed=user_info(user=user))

    @commands.command()
    async def delete(self, ctx, *args):
        pass

    @commands.command()
    async def add(self, ctx, *args):
        pass

    @commands.command()
    async def clear(self, ctx, *args):
        pass


def setup(bot):
    bot.add_cog(Admin(bot))
