from cogs.etc.config import ESCAPE
from cogs.etc.config import PROJECT_NAME
from cogs.etc.config import cur
from cogs.etc.config import dbSun


class Preset:
    """ This is the Main function part for my Administration bot """
    @staticmethod
    def parser(rounds, toparse, option) -> list:
        """ This is a small self written Argparser

        This Function parse given Arguments for administration

        :param rounds: Insert the max number of words for the return
        :param toparse: Gives the Arg to Parse
        :param option: Insert option for parsing

        :return: list
        """

        return_list = []

        for key in toparse:
            if ESCAPE + toparse[toparse.index(key)] in option:
                for i in range(rounds):
                    return_list.append(toparse[i])
                return return_list

    @staticmethod
    def whitelist(mode, member=int) -> str or list:
        """Whitelist function whitelist a member

        :param mode:add: Add a Member to the Whitelist for Administration
        :param mode:list: List all members on the whitelist
        :param mode:remove: Remove a Member from the Whitelist
        :param member: Serve the member

        :returns: SQL Insert/Update
        """

        if mode == 'list':
            compare = []

            cur.execute(f"SELECT uid FROM whitelist WHERE name='{PROJECT_NAME}'")
            fetcher = cur.fetchall()

            if fetcher:
                for i in fetcher:
                    compare.append(i)
            else:
                return 'Cannot find any entries'

            return compare

        elif mode == 'add':
            cur.execute("INSERT INTO whitelist(name, uid) VALUES (?, ?)", (PROJECT_NAME, member))
            dbSun.commit()
            return f'Added <@{member}> to the whitelist'

        elif mode == 'remove':
            cur.execute("DELETE FROM whitelist WHERE uid=? and name=?;", (member, PROJECT_NAME))
            dbSun.commit()
            return f'Removed <@{member}> from whitelist'
        else:
            return f'{mode} is not available'
