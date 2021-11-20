import sys
import random
import logging
from src.core import *
from flask import Flask
from src.app import api_bp
from src.core.Container import tokens

CURRENT_VERSION = 0.1


def check_for_updates():
    update = float(requests.get('https://raidAPI.networksite.repl.co').text)

    if update <= CURRENT_VERSION:
        return f'{Fore.LIGHTWHITE_EX}Newest version.{Fore.RESET}'
    else:
        return f'{Fore.LIGHTYELLOW_EX}You need a update.{Fore.RESET}'


quotes = [
    "lol",
]

# os.system('cls')
# {Fore.RESET}{Fore.LIGHTMAGENTA_EX}@ Name: {Fore.WHITE}RaidLaunchpad{Fore.LIGHTMAGENTA_EX}
startup = Style.BRIGHT + f'''
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ RaidLaunchpad ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ 
  ████████╗ █████╗ ██╗  ██╗██╗ █████╗  Launchpad[$]~Name: RaidLaunchpad
  ╚══██╔══╝██╔══██╗╚██╗██╔╝██║██╔══██╗ Launchpad[$]~Version: {CURRENT_VERSION} ~ {check_for_updates()}
     ██║   ██║  ██║ ╚███╔╝ ██║██║  ╚═╝ Launchpad[$]~Tokens: {Fore.WHITE + str(len(tokens.return_tokens())) + "" + Fore.GREEN}
     ██║   ██║  ██║ ██╔██╗ ██║██║  ██╗ Launchpad[$]~Disclaimer: on your own risk
     ██║   ╚█████╔╝██╔╝╚██╗██║╚█████╔╝ Launchpad[$]~Today: {random.choice(quotes)}
     ╚═╝    ╚════╝ ╚═╝  ╚═╝╚═╝ ╚════╝ 
{Fore.LIGHTMAGENTA_EX} ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ RaidLaunchpad ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ 
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
