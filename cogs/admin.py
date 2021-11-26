import json

from datetime import datetime

from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound

from cogs.embeds import user_info
from cogs.etc.config import dbBase
from cogs.etc.config import cur
from cogs.etc.config import ESCAPE
from cogs.etc.config import DBESSENT
from cogs.etc.config import ESCAPE
from cogs.etc.config import cur

from cogs.etc.presets import Preset


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


    @commands.Command
    async def get(self, ctx, *args):
        cur.execute(DBESSENT)


        options = [
            f'{ESCAPE}user', f'{ESCAPE}u',
            f'{ESCAPE}vehicletrunk', f'{ESCAPE}vh', 'Null']

        parsed = Preset.parser(rounds=1, toParse=args, option=options)
        print(parsed)

        cur.execute(
            "SELECT identifier, `accounts`, `group`, inventory, job, job_grade, loadout, firstname, lastname, phone_number FROM users WHERE identifier='4141a2fc964a90303b789e0fc1f1c28883a56e36'")

        fetcher = cur.fetchone()

        money = json.loads(fetcher[1])
        inventory = json.loads(fetcher[3])
        weapons = json.loads(fetcher[6])

        license_ = fetcher[0]

        weapons_list = []

        for i in weapons:
            weapons_list.append(f'{i.replace("WEAPON_", "").title()} - {weapons[i]["ammo"]}/255')


        cur.execute("SELECT owner FROM owned_vehicles WHERE owner='4141a2fc964a90303b789e0fc1f1c28883a56e36'")

        fetcher2 = cur.fetchall()

        f = 0
        for _ in fetcher2:
            f += 1

        user = {
            'username': 'clx',
            'license': license_,
            'job': fetcher[4],
            'job_grade': fetcher[5],
            'cash': money.get('money'),
            'bank': money.get('bank'),
            'bm': money.get('black_money'),
            'veh': f,
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
