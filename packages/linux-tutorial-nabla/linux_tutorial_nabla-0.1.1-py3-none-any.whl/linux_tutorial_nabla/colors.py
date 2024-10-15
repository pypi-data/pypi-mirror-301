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

    @staticmethod
    def command(s):
        return Colors.M(s) + Fore.GREEN + Style.NORMAL
    
    @staticmethod
    def highlight(s):
        return Colors.B(s) + Fore.GREEN + Style.NORMAL
    
    @staticmethod
    def error(s):
        return Colors.R(s) + Fore.GREEN + Style.NORMAL
    
    @staticmethod
    def success(s):
        return Colors.G(s) + Fore.GREEN + Style.NORMAL
    
    @staticmethod
    def info(s):
        return Colors.C(s) + Fore.GREEN + Style.NORMAL
    
    @staticmethod
    def warning(s):
        return Colors.Y(s) + Fore.GREEN + Style.NORMAL
    
    @staticmethod
    def bold(s):
        return Style.BRIGHT + s + Style.NORMAL
    
    @staticmethod
    def nabla_text(s):
        return Colors.g(s)
    
    @staticmethod
    def other_text(s):
        return Colors.b(s) + Fore.GREEN + Style.NORMAL

