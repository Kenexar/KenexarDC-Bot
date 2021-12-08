# here comes the logger function
from datetime import datetime

from cogs.logger.console_color_codes import ANSI


logger_conf = {
    'log_mode': 'normal',
    'enable_logging': True,
    'enable_logfile': True,
}


def logger(mode, message):
    """ Logger function

    @param mode: Possible: error, warning, info
    @param message: what should to send
    @return: Commandline or Discord message
    """
    if not logger_conf.get('enable_logging'):
        return 'logging is not enabled!'

    template = ''

    with open(f'cogs/logs/log_{datetime.now().date()}', 'a+') as f:
        if mode == 'error':
            template = f'{ANSI.get("RED", "X")}[ ERROR]{ANSI.get("RESET")}' + ' ' * 2

        if mode == 'warning':
            template = f'{ANSI.get("YELLOW", "~")}[  WARN]{ANSI.get("RESET")}' + ' ' * 2

        if mode == 'info':
            template = f'{ANSI.get("GREEN", "+")}[  INFO]{ANSI.get("RESET")}' + ' ' * 2

        if logger_conf.get('enable_logfile', False):
            f.write(f"{template}{message}\n")

    return f"[ {datetime.now().strftime('%H:%M:%S')} ]" + template + message

