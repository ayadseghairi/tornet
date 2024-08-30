#!/usr/bin/python
green = "\033[92m"
red = "\033[91m"
white = "\033[97m"
reset = "\033[0m"
cyan = "\033[36m"

def print_banner():
    banner = f"""
{white} +-------------------------------------------------------+
{white} |{green} ████████╗ ██████╗ ██████╗ ███╗   ██╗███████╗████████╗{white} |
{white} |{green} ╚══██╔══╝██╔═══██╗██╔══██╗████╗  ██║██╔════╝╚══██╔══╝{white} |
{white} |{green}    ██║   ██║   ██║██████╔╝██╔██╗ ██║█████╗     ██║   {white} |
{white} |{green}    ██║   ██║   ██║██╔══██╗██║╚██╗██║██╔══╝     ██║   {white} |
{white} |{green}    ██║   ╚██████╔╝██║  ██║██║ ╚████║███████╗   ██║   {white} |
{white} |{green}    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   {white} |
{white} +---------------------{cyan}({red}ByteBreach{cyan}){white}----------------------+{reset}
{white} +--------------{cyan}({red}Improved by Ayad Seghiri{cyan}){white}--------------------+{reset}
"""
    print(banner)
