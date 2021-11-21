import random
import threading
import subprocess
from src.core.Util import *
from src.core.RaidLaunchpad import *
from src.core.Container import tokens
from multiprocessing.dummy import Pool as ThreadPool

lead_token = tokens.return_tokens()[0]


def bots_in_server(server_id):
    all_tokens = tokens.return_tokens()
    in_server = 0
    for token in all_tokens:
        server_check = send(f'users/@me/guilds/{server_id}/settings', 'PATCH', token,
                                {'hide_muted_channels': 'false'}).status_code

        if server_check == 200:
            in_server += 1
        else:
            in_server -= 1

    if in_server == len(all_tokens):
        return True
    else:
        return False


def start_spam(server_id, messages, mode):
    if bots_in_server(server_id):

        channels = scrape_channels(server_id, lead_token)
        user_ids = scrape_user_ids(channels[0], 20, lead_token)

        change_temp_data('spam_flag', 0)

        spam_threads = []

        for token in tokens.return_tokens():
            spam_thread = threading.Thread(target=start_message_thread, args=[token, messages, channels, mode, user_ids])
            spam_thread.daemon = True
            spam_threads.append(spam_thread)

        execute_threads(spam_threads)

    else:
        return response(500, "Could not start spam, make sure all bots are in the current server.")


def ping_all_tokens():
    alive = []
    invalid = []
    locked = []
    limited = []

    pool = ThreadPool(5)
    tokens_pinged = pool.map(ping_token, tokens.return_tokens())
    pool.close()
    pool.join()

    for ping_type, token in tokens_pinged:
        if ping_type == 0:
            alive.append(token)
        elif ping_type == 1:
            invalid.append(token)
        elif ping_type == 2:
            locked.append(token)
        elif ping_type == 3:
            limited.append(token)

    console_log(
        f'{"Tokens Pinged: " + Fore.LIGHTMAGENTA_EX + str(len(alive)) + Fore.RESET} alive, {Fore.LIGHTCYAN_EX + str(len(invalid)) + Fore.RESET} invalid, '
        f'{Fore.RED + str(len(locked)) + Fore.RESET} phone-locked, {Fore.LIGHTYELLOW_EX + str(len(limited)) + Fore.RESET} '
        f'rate-limited, out of {str(len(tokens.return_tokens())) + " tokens."}')

    if len(invalid) or len(locked) > 0:
        os.remove('tokens.txt')

        valid_tokens = alive + limited
        tokens.clear_tokens()
        tokens.build_token_format(valid_tokens)

        with open('tokens.txt', mode='w') as token_file:
            token_file.write('\n'.join(valid_tokens))

    return response(200, "All tokens have been pinged. Check console for info.")


def all_bots_join(invite_link):
    check_invite = invite_link.split("/")

    if check_invite[3] == 'invite':
        invite_code = check_invite[4]
    else:
        invite_code = check_invite[3]

    join_threads = []

    for token in tokens.return_tokens():
        join_thread = threading.Thread(target=send, args=[f'invites/{invite_code}', "POST", token, {}])
        join_thread.daemon = True
        join_threads.append(join_thread)

    execute_threads(join_threads, random.randint(0, 2))

    return response(200, f"All bots have attempted to join the target server. Server invite: {invite_link}")


def all_bots_leave(server_id):
    leave_threads = []

    for token in tokens.return_tokens():
        leave_thread = threading.Thread(target=send, args=[f'users/@me/guilds/{server_id}', 'DELETE', token, {'lurking': False}])
        leave_thread.daemon = True
        leave_threads.append(leave_thread)

    execute_threads(leave_threads)

    return response(200, f"All bots have attempted to leave the target server. Server: {server_id}")


def change_all_bots_nick(server_id, nick):
    nick_threads = []

    for token in tokens.return_tokens():
        nick_thread = threading.Thread(target=change_nick, args=[nick, server_id, token])
        nick_thread.daemon = True
        nick_threads.append(nick_thread)

    execute_threads(nick_threads)

    return response(200, f"Try to change bot names to {nick}")


def disguise_all_bots(server_id):
    disguise_threads = []

    for token in tokens.return_tokens():
        disguise_thread = threading.Thread(target=disguise_token, args=[server_id, token])
        disguise_thread.daemon = True
        disguise_threads.append(disguise_thread)

    execute_threads(disguise_threads)

    return response(200, "All bots tryed to disguise.")


def all_bots_speak(server_id, message):
    speak_threads = []
    bot_tokens = tokens.return_tokens()
    channels = scrape_channels(server_id, lead_token)
    message = clean_input(message)[0]

    for channel in channels:
        speak_thread = threading.Thread(target=bot_message, args=[random.choice(bot_tokens), channel, message])
        speak_thread.daemon = True
        speak_threads.append(speak_thread)

    execute_threads(speak_threads, 0.06)

    return response(200, "Bots attempted to speak in all available channels.")


def all_bots_react(channel_id, message_id, emoji):
    react_threads = []

    for token in tokens.return_tokens():
        react_thread = threading.Thread(target=react, args=[channel_id, message_id, emoji, token])
        react_thread.daemon = True
        react_threads.append(react_thread)

    execute_threads(react_threads)

    return response(200, f'Bots attempted to react to message: {message_id}.')

