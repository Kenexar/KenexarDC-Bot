from cogs.etc.config import ESCAPE


def parser(rounds, toParse, option) -> list or None:
    """ This is a small self written Argparser

    This Function parse given Arguments for administration

    :param rounds: Insert the max number of words for the return
    :param toParse: Gives the Arg to Parse
    :param option: Insert option for parsing


    :return: list
    """

    return_list = []

    for key in toParse:
        if ESCAPE + toParse[toParse.index(key)] in option:
            for i in range(rounds + 1):
                return_list.append(toParse[i])
            return return_list
        return None
