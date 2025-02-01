from colorama import Style, Fore

green = Fore.GREEN
yellow = Fore.YELLOW
blue = Fore.BLUE
cyan = Fore.CYAN
magenta = Fore.MAGENTA
red = Fore.RED
reset = Style.RESET_ALL

ok = f"{green}[  OK  ]{reset}"
info = f"{blue}[ INFO ]{reset}"
warning = f"{yellow}[ WARN ]{reset}"
error = f"{red}[ ERROR ]{reset}"
