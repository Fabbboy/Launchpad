import sys
import random
import logging
from src.core import *
from flask import Flask
from src.app import api_bp
from src.core.Container import tokens

CURRENT_VERSION = 0.2


def check_for_updates():
    update = float(requests.get('https://raw.githubusercontent.com/Galaxzy345/Deadcord-Client/main/version.txt').text)

    if update <= CURRENT_VERSION:
        return f'{Fore.LIGHTWHITE_EX}Up to date.{Fore.RESET}'
    else:
        return f'{Fore.LIGHTYELLOW_EX}Update Available at https://github.com/Galaxzy345/Deadcord.{Fore.RESET}'


quotes = [
    "This ain't hacking lol.",
    "Lagging Discord since last month.",
    "So, you here to lag a server?",
    "Great to see you again.",
    "I am sentient.",
    "Don't worry. This is ban proof.",
    "R.I.P Groovy & Rhythm.",
    "We built an entire GUI before switching to a terminal window.",
    "Built to protest against Discord.",
    "The only raid tool that adapts and fights back.",
    "We are open source (duh).",
    "Discord is shooting themselves in the foot."
]

os.system('cls')

startup = Style.BRIGHT + f'''

   ██████╗ ███████╗ █████╗ ██████╗  ██████╗ ████████╗ ██████╗ ██████╗   ┏━━━━━━━━━━━━━━━━━━ Info ━━━━━━━━━━━━━━━━┓
   ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██████████╗██╔══██╗██╔══██╗    {Fore.RESET}{Fore.LIGHTMAGENTA_EX}@ Package: {Fore.WHITE}Deadcord-Engine{Fore.LIGHTMAGENTA_EX}
   ██║  ██║█████╗  ███████║██║  ██║██║     ██║ ██  ██║██████╔╝██║  ██║    {Fore.RESET}{Fore.LIGHTMAGENTA_EX}@ Author: {Fore.WHITE}Galaxzy#4845{Fore.LIGHTMAGENTA_EX}
   ██║  ██║██╔══╝  ██╔══██║██║  ██║██║     ████  ████║██╔══██╗██║  ██║    {Fore.RESET}{Fore.LIGHTMAGENTA_EX}@ Tokens: {Fore.WHITE + str(len(tokens.return_tokens())) + " tokens loaded" + Fore.LIGHTMAGENTA_EX}
   ██████╔╝███████╗██║  ██║██████╔╝╚██████╗╚████████╔╝██║  ██║██████╔╝    {Fore.RESET}{Fore.LIGHTMAGENTA_EX}@ Warning: {Fore.RED}Use at your own risk!{Fore.LIGHTMAGENTA_EX}
   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ █═█═█═█═╝ ╚═╝  ╚═╝╚═════╝   ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛       
   
                                    
{Fore.LIGHTBLACK_EX} Starting the Deadcord Engine: {random.choice(quotes)}{Fore.RESET} ~ {Fore.LIGHTMAGENTA_EX}Version 0.0.1{Fore.RESET} ~ {check_for_updates()}
{Fore.WHITE}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────{Fore.RESET}
'''.replace('█', f'{Fore.WHITE}█{Fore.LIGHTMAGENTA_EX}')

print(startup)

if get_config("use_tor"):
    console_log('WARNING: Using Tor with Deadcord is still in early beta stages. Requests may become slow or not go through.', 3)

console_log('Deadcord is ready. Join our Discord if you do not have our BetterDiscord plugin.', 2)
console_log('Our BetterDiscord plugin is needed to interact with Deadcord.', 2)

app = Flask(__name__)

if not get_config("boot_mode") == 1:
    app.logger.disabled = True
    log = logging.getLogger('werkzeug')
    log.disabled = True

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app.register_blueprint(api_bp, url_prefix='/deadcord')


@app.after_request
def after_request(status):
    status.headers.add('Access-Control-Allow-Origin', '*')
    status.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    status.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return status
