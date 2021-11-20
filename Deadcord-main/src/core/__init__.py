from .Util import *

if not os.path.exists('config.json'):
    with open('config.json', 'w') as config:
        config.write("""{"boot_mode": 0, "use_tor": false, "tor_port": "9150"}""")
        config.close()

console_log(f'Booting on mode {str(get_config("boot_mode"))}.')
