import json

from cogs.etc.embeds import help_site
from cogs.etc.embeds import user_info
from cogs.etc.presets import parser, get_perm
from nextcord.ext import commands


class GtaRP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.whitelist = self.bot.fetch_whitelist()

        self.guild = None
        self.logger = None

        self.GET_OPTIONS = [
            'user', 'u',
            'vehicletrunk', 'vh', 'Null'
        ]

        self.DEL_OPTIONS = [
            'fuser', 'fu',
            'veh', 'vehicle',
            'vehtrunk', 'veht',
            'usermoney', 'um',
            'inv', 'inventory',
            'weapons', 'Null'
        ]

        self.ADD_OPTIONS = [
            'um', 'usermoney',
            'weapons'
        ]

    @commands.Command
    async def get(self, ctx, *args):
        """ Get function [user|veht|Null]
            Get for specific users the player data from the db

        """
        if await get_perm(
                ctx.message.author.id) < 2 and ctx.message.author.id in self.whitelist:  # permission checker if user is mod or higher and in whitelist
            return await ctx.send('You are not Authorized to use the Get function!'), \
                   await self.logger.send(f'{ctx.message.author} tried to use the `get` command!')

        cur = self.bot.dbBase.cursor(buffered=True)
        cur.execute(self.bot.dbessent)

        parsed = await parser(rounds=2, toparse=args, option=self.GET_OPTIONS)
        if parsed[0] in self.GET_OPTIONS[0:2]:  # if argument user or u
            cur.execute(
                "SELECT identifier, `accounts`, `group`, inventory, job, job_grade, loadout, firstname, lastname, phone_number FROM users WHERE identifier=%s",
                (parsed[1],))

            fetcher = cur.fetchone()

            try:
                money = json.loads(fetcher[1])
            except TypeError:
                return await ctx.send(f'{parsed[1]} is not an Valid id!')

            inventory = json.loads(fetcher[3])
            weapons = json.loads(fetcher[6])

            license_ = fetcher[0]

            weapons_list = []

            for i in weapons:
                weapons_list.append(f'{i.replace("WEAPON_", "").title()} - {weapons[i]["ammo"]}/255')

            cur.execute("SELECT owner FROM owned_vehicles WHERE owner=%s", (parsed[1],))

            fetcher2 = cur.fetchall()
            veh = 0

            for i in fetcher2:
                veh += 1

            user = {
                'username': 'clx',
                'license': license_,
                'job': fetcher[4],
                'job_grade': fetcher[5],
                'cash': money.get('money'),
                'bank': money.get('bank'),
                'bm': money.get('black_money'),
                'veh': veh,
                'weapons': weapons_list,
                'inv': inventory,
                'firstname': fetcher[7],
                'lastname': fetcher[8],
                'phone_number': fetcher[9]
            }

            await ctx.send(embed=user_info(user=user))
        elif parsed[0] in self.GET_OPTIONS[2:4]:  # if argument vehicle trunk or veht
            pass
        elif parsed[0] == 'Null':  # get all null entries
            pass

        cur.close()

    @commands.command()
    async def delete(self, ctx, *args):
        """ Delete command for delete entire user entry in the database
            this command is high sensible, of course you need rank 4 or higher to use it
            you can also delete single things like weapons or vehicles, to prevent duping
            you can remove/clear weapons, money, vehicles, maybe sprays
        """

    pass

    @commands.command()
    async def add(self, ctx, *args):
        """ Add command to add something like items or weapons to users inventory
            an example when a mod is in the support channel and no one with database permission is online, then you can
            add thing to the users entrie.
            you can add usermoney, weapons, vehicles
        """

    pass

    @commands.Command
    async def einreise(self, ctx, *args):
        if not ctx.message.author.id in self.whitelist:
            return await ctx.send('You are not Authorized to delete user Entries'), \
                   await self.logger.send(f'{ctx.message.author} tried to use the `einreise` command!')

        if get_perm(ctx.message.author.id) >= 4:
            cur = self.bot.dbBase.cursor()
            cur.execute(self.bot.dbessent)

            if not args:
                return await ctx.send(embed=help_site('einreise'))

            if args[0]:
                cur.execute("SELECT identifier FROM users WHERE identifier=%s;", (args[0],))

                if not cur.fetchone():
                    return await ctx.send('Invalid id!')

                cur.execute("DELETE FROM users WHERE identifier=%s;", (args[0],))
                self.bot.dbBase.commit()

                return await ctx.send('User got deleted from the Db')

            cur.close()
            return await ctx.send('You are not Authorized to delete user Entries'), \
                   await self.logger.send(f'{ctx.message.author} tried to use the `einreise` command!')


def setup(bot):
    bot.add_cog(GtaRP(bot))
