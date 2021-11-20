import sys
import json
from time import sleep
from src.core.Util import *
from src.core.Cloudflare import *


class Tokens:

    def __init__(self):
        self.raw_tokens = []
        self.tokens = {}

        console_log(f'Searing  "tokens.tx"')
        sleep(1)
        full_path = os.path.join("./", "tokens.txt")
        if os.path.exists(full_path):
            console_log(f'"tokens.txt" was found\n', 2)
            self.get_tokens(full_path)
            found = True
        else:
            found = False
            console_log(f'no tokens.txt found')

        if not found or len(self.raw_tokens) == 0:
            if console_log('Could not find any tokens. Search again? [y/n]', 4).lower() == 'y':
                self.__init__()
            else:
                console_log('No tokens found, Invalid key or n. ReadLaunchpad is shuting down.', 3)
                sleep(4)
                sys.exit()

    def get_tokens(self, file):
        self.raw_tokens.clear()
        if os.path.exists(file):
            with open(file, "r") as token:
                lines = token.readlines()
                for line in lines:
                    extract = line.replace('\n', '')
                    if not extract[0] == "#":
                        self.raw_tokens.append(extract)

        self.create_token(self.raw_tokens)

    def create_token(self, tokens):
        payload = {}

        for count, token in enumerate(tokens):
            agent_string = rand_user_agent()
            browser_data = agent_string.split(" ")[-1].split("/")
            possible_os_list = ["Windows", "Macintosh"]

            for possible_os in possible_os_list:
                if possible_os in agent_string:
                    agent_os = possible_os
                    break

            if agent_os == "Macintosh":
                os_version = f'Intel Mac OS X 10_15_{str(random.randint(5, 7))}'
            else:
                os_version = "10"

            struct = {
                count: {
                    "token": token,
                    "agent": agent_string,
                    "os": agent_os,
                    "browser": browser_data[0],
                    "browser_version": browser_data[1],
                    "os_version": os_version
                }
            }

            payload.update(struct)
            self.tokens.update(payload)

    def return_tokens(self):
        raw_tokens = []
        for count, data in self.tokens.items():
            raw_tokens.append(data["token"])

        return raw_tokens

    def get_token_info(self, token):
        for token_struct, token_payload in self.tokens.items():
            for data_name, data_content in token_payload.items():
                if token in data_content:
                    return token_payload

    def clear_tokens(self):
        self.tokens.clear()
