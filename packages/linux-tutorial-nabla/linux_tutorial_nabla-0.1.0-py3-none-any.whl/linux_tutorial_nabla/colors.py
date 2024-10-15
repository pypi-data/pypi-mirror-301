from colorama import *

# These are meant to be shorthand function calls to quickly turn a string
# into something with color.

class Colors:
    @staticmethod
    def G(string): return Fore.GREEN + Style.BRIGHT + string + Fore.RESET + Style.NORMAL

    @staticmethod
    def g(string): return Fore.GREEN + string + Fore.RESET

    @staticmethod
    def B(string): return Fore.BLUE + Style.BRIGHT + string + Fore.RESET + Style.NORMAL

    @staticmethod
    def b(string): return Fore.BLUE + string + Fore.RESET

    @staticmethod
    def R(string): return Fore.RED + Style.BRIGHT + string + Fore.RESET + Style.NORMAL

    @staticmethod
    def r(string): return Fore.RED + string + Fore.RESET

    @staticmethod
    def Y(string): return Fore.YELLOW + Style.BRIGHT + string + Fore.RESET + Style.NORMAL

    @staticmethod
    def y(string): return Fore.YELLOW + string + Fore.RESET

    @staticmethod
    def M(string): return Fore.MAGENTA + Style.BRIGHT + string + Fore.RESET + Style.NORMAL

    @staticmethod
    def m(string): return Fore.MAGENTA + string + Fore.RESET

    @staticmethod
    def C(string): return Fore.CYAN + Style.BRIGHT + string + Fore.RESET + Style.NORMAL

    @staticmethod
    def c(string): return Fore.CYAN + string + Fore.RESET

    @staticmethod
    def W(string): return Fore.WHITE + Style.BRIGHT + string + Fore.RESET + Style.NORMAL

    @staticmethod
    def w(string): return Fore.WHITE + string + Fore.RESET

