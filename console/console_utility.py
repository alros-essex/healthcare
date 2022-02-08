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

    def print_conversation(line:str):
        ConsoleUtility._print(line, Fore.YELLOW, Back.BLACK)

    @staticmethod
    def prompt_user_for_input(options = None, validation = None):
        if options is None:
            while True:
                user_input = input(' > ')
                if validation is None or validation(user_input):
                    return user_input
                else:
                    ConsoleUtility.print_error('Err. invalid input')  
        else:
            while True:
                # infinite loop waiting for a valid input
                user_input = input('{} > '.format(options))
                if user_input in options:
                    return user_input
                elif validation is not None:
                    return user_input
                else:
                    # error, let the user know the valid options
                    ConsoleUtility.print_error('Err. valid options are {}'.format(options))  

    def _print(line:str, color_fg, color_bg):
        print('{color_fg}{color_bg}{line}{reset_bg}{reset_fg}'.format(line = line,
            color_fg = color_fg, color_bg = color_bg, reset_bg = Back.RESET, reset_fg = Fore.RESET))