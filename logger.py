import colorlog
import logging
from colorama import init, Fore




FORMAT = "|%(log_color)s%(asctime)s| - Profile [%(name)s] - %(levelname)s - %(message)s"



def SetupGayLogger(logger_name, rainbow=False):
    init()

    def rainbow_colorize(text):
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
        colored_message = ''
        for index, char in enumerate(text):
            color = colors[index % len(colors)]
            colored_message += color + char
        return colored_message

    class RainbowColoredFormatter(colorlog.ColoredFormatter):
        def format(self, record):
            message = super().format(record)
            if rainbow:
                return rainbow_colorize(message)
            return message

    logger = colorlog.getLogger(logger_name)
    while logger.hasHandlers():
        logger.removeHandler(logger.handlers[0])
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        RainbowColoredFormatter(
            FORMAT,
            datefmt=None,
            reset=False,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        )
    )
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger