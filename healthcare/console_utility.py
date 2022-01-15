from os import stat
from colorama import Fore, Back, Style

class ConsoleUtility:

    @staticmethod
    def print_light(line:str):
        ConsoleUtility._print(line, Fore.WHITE, Back.BLACK)

    @staticmethod
    def print_option(line:str):
        ConsoleUtility._print(line, Fore.CYAN, Back.BLACK)

    @staticmethod
    def print_error(line:str):
        ConsoleUtility._print(line, Fore.RED, Back.YELLOW)

    @staticmethod
    def prompt_user_for_input(options = None):
        if options is None:
            return input(' > ')
        while True:
            # infinite loop waiting for a valid input
            user_input = input('{} > '.format(options))
            if user_input in options:
                return user_input
            else:
                # error, let the user know the valid options
                ConsoleUtility.print_error('Err. valid options are {}'.format(options))  

    def _print(line:str, color_fg, color_bg):
        print('{color_fg}{color_bg}{line}{reset_bg}{reset_fg}'.format(line = line,
            color_fg = color_fg, color_bg = color_bg, reset_bg = Back.RESET, reset_fg = Fore.RESET))