from main_funcs import login_stuff, post_cat
from creds      import username, password
from util_funcs import logme

from rich         import print as printf
from rich.console import Console

import time as t






def main():
    CONFIG = {
        'username':        username,
        'password':        password,
        'settings_fp':    'settings.json',
        'eyebleach_dir':  '/Users/ravi/Pictures/Eyebleach',
        'delay':           60*60
    }

    COLORS = {
        'log': 'green1',
        'war': 'yellow1',
        'err': 'red1',
        'post': 'deep_sky_blue1',
    }

    # Does all the login stuff
    client           = login_stuff(CONFIG)
    # Gets the username of the acc I am logged into
    logged_username  = client.username_from_user_id(client.user_id)
    logme(f'[green1][b][LOG]    [/] Logged in as [u magenta1]@{logged_username}[/][/]')
    # Posts the cat
    while True:
        post_cat(CONFIG, COLORS, client)
        t.sleep(CONFIG['delay'])









def init_main():
    console = Console()
    try:
        main()
    except Exception as e:
        console.print_exception()




if __name__ == '__main__':
    init_main()











'''

config is gonna be like
{
    username
    password
    eyebleach_dir
    settings_fp
    delay
}

'''

