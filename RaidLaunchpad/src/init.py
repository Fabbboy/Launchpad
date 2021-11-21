import sys
import random
import logging
from src.core import *
from flask import Flask
from src.app import api_bp
from src.core.Container import tokens

CURRENT_VERSION = 0.5


def check_for_updates():
    update = float(requests.get('https://raidAPI.networksite.repl.co').text)

    if update <= CURRENT_VERSION:
        return f'{Fore.LIGHTGREEN_EX}Newest version.{Fore.RESET}'
    else:
        return f'{Fore.LIGHTYELLOW_EX}You need a update. Join our Discord for the files and more info{Fore.RESET}'


quotes = [
    "lol",
]

# os.system('cls')
# {Fore.RESET}{Fore.LIGHTMAGENTA_EX}@ Name: {Fore.WHITE}RaidLaunchpad{Fore.LIGHTMAGENTA_EX}
startup = Style.BRIGHT + f'''
{Fore.LIGHTGREEN_EX}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ RaidLaunchpad ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ 
  ████████╗ █████╗ ██╗  ██╗██╗ █████╗  Launchpad[$]~Name: {Fore.LIGHTGREEN_EX}RaidLaunchpad{Fore.RESET}
  ╚══██╔══╝██╔══██╗╚██╗██╔╝██║██╔══██╗ Launchpad[$]~Version: {CURRENT_VERSION} ~ {check_for_updates()}
     ██║   ██║  ██║ ╚███╔╝ ██║██║  ╚═╝ Launchpad[$]~Tokens: {Fore.LIGHTGREEN_EX + str(len(tokens.return_tokens())) + "" + Fore.LIGHTGREEN_EX}
     ██║   ██║  ██║ ██╔██╗ ██║██║  ██╗ Launchpad[$]~Disclaimer: {Fore.LIGHTGREEN_EX}on your own risk{Fore.RESET}
     ██║   ╚█████╔╝██╔╝╚██╗██║╚█████╔╝ Launchpad[$]~Today: {Fore.LIGHTGREEN_EX}{random.choice(quotes)}{Fore.RESET}
     ╚═╝    ╚════╝ ╚═╝  ╚═╝╚═╝ ╚════╝ 
{Fore.LIGHTGREEN_EX}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ RaidLaunchpad ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ 
'''.replace('█', f'{Fore.WHITE}█{Fore.LIGHTMAGENTA_EX}')

print(startup)

if get_config("use_tor"):
    console_log('WARNING: The use of Tor with RaidLaunchpad is in beta.', 3)

console_log('RaidLaunchpad is ready. You need to use our Webtool for more info https://raidapi.networksite.repl.co/Webtool.', 1)

app = Flask(__name__)

if not get_config("boot_mode") == 1:
    app.logger.disabled = True
    log = logging.getLogger('werkzeug')
    log.disabled = True

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app.register_blueprint(api_bp, url_prefix='/raidrocket')


@app.after_request
def after_request(status):
    status.headers.add('Access-Control-Allow-Origin', '*')
    status.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    status.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return status
