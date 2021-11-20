import sys
import emoji
import random
from time import sleep
from src.core.Util import *
from src.core.Endpoints import *


def ping_token(token):
    token_ping = send('users/@me/library', 'GET', token).status_code

    if token_ping == 200:
        return 0, token
    elif token_ping == 401:
        return 1, token
    elif token_ping == 403:
        return 2, token
    elif token_ping == 429:
        return 3, token


def start_message_thread(token, messages, channels, mode, users=None):
    if users is None:
        users = []

    #message = random.choice(messages)
    message = messages
    if mode == 1:
        built_message = f'@everyone'
    elif mode == 2:
        built_message = f'<@{random.choice(users)}> {message}'
    elif mode == 3:
        blank_payload = ""
        for newline in range(1700):
            blank_payload += "\n"

        built_message = f"\n‎{blank_payload}‎\n"
    elif mode == 4:
        lag_payload = ""
        for newline in range(140):
            lag_payload += ":chains: "

        built_message = f"\n‎{lag_payload}‎\n"
    else:
        built_message = message

    while get_temp_data('spam_flag') == 0:
        try:
            bot_send = bot_message(token, random.choice(channels), built_message)

            if "global" in bot_send:
                sleep(9)

        except Exception as e:
            pass


def bot_message(token, channel, message):
    bot_message_send = send(f'channels/{channel}/messages', 'POST', token, {"content": message})
    bot_message_send.json()
    return bot_message_send.json()


def change_avatar(url, token):
    avatar = requests.get(url)
    image = "data:image/png;base64," + b64encode(avatar.content).decode('utf-8')
    imagePayload = {"avatar": image}

    avatar_change = send("users/@me", "PATCH", token, imagePayload).text

    if "code" in avatar_change:
        return False
    else:
        return True


def reset_avatar(token):
    imagePayload = {"avatar": None}
    avatar_change = send("users/@me", "PATCH", token, imagePayload).text

    if "code" in avatar_change:
        return False
    else:
        return True


def change_nick(name, server_id, token):
    if name == "random":
        nickname = random_name()
    else:
        nickname = name

    nickname_send = send(f'guilds/{server_id}/members/@me', 'PATCH', token, {'nick': nickname})
    return nickname_send.json()


def scrape_usernames(channel_id, amount, token):
    usernames = []
    for username in json.loads(send(f'channels/{channel_id}/messages?limit={amount}', 'GET', token).text):
        if username['author']['username'] not in usernames:
            usernames.append(username['author']['username'])

    return usernames


def scrape_user_ids(channel_id, amount, token):
    user_ids = []
    for author in json.loads(send(f'channels/{channel_id}/messages?limit={amount}', 'GET', token).text):
        if author['author']['id'] not in user_ids:
            user_ids.append(author['author']['id'])

    return user_ids


def scrape_avatars(channel_id, amount, token):
    avatars = {}
    for avatar in json.loads(send(f'channels/{channel_id}/messages?limit={amount}', 'GET', token).text):
        if avatar['author']['username'] not in avatars.keys():
            if avatar['author']['avatar'] is not None:
                avatars[avatar['author']['avatar']] = [avatar['author']['username'], avatar['author']['id']]

    return avatars


def scrape_channels(server_id, token):
    channels = send(f'guilds/{server_id}/channels', 'GET', token)
    data = json.loads(channels.text)

    if channels.status_code == 200:
        found_channels = []

        for channel in data:
            if 'bitrate' not in channel and channel['type'] == 0:
                if channel not in found_channels:
                    found_channels.append(channel["id"])

        return found_channels

    else:
        return False


def can_ping_everyone(channel, token):
    msg = json.loads(bot_message(token, channel, "@everyone"))
    if msg["mention_everyone"]:
        return True
    else:
        return False


def react(channel_id, message_id, emoji_name, token):
    react_emoji = emoji.emojize(f':{emoji_name}:', use_aliases=True)
    react_send = send(f'channels/{channel_id}/messages/{message_id}/reactions/{react_emoji}/@me', 'PUT', token)
    return react_send


def random_name():
    name_fetch = requests.get('https://api.namefake.com/').text
    name = json.loads(name_fetch)
    return name["username"]


def disguise_token(server_id, token):
    reset_avatar(token)
    avatar_change = change_avatar(f'https://picsum.photos/200/200', token)

    if avatar_change:
        send(f'guilds/{server_id}/members/@me', 'PATCH', token, {'nick': random_name() + str(random.randint(1, 100))})
        return True
    else:
        return False
