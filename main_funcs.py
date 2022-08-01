from util_funcs import get_file_path, convert_img, logme

from instagrapi.exceptions import PhotoNotUpload, UnknownError
from rich                  import print as printf
from instagrapi            import Client

import os









def login_stuff(config:dict) -> Client:
    # Loads the config
    username    = config['username']
    password    = config['password']
    settings_fp = config['settings_fp']
    client      = Client()
    # If the setting file exists, uses it to login
    if os.path.exists(settings_fp):
        client.load_settings(settings_fp)
        client.login('','')
        logme(f'[green1][b][LOG]    [/] Loaded the settings from [u magenta1]{settings_fp}[/][/]')
    # Else, logins to insta and saves the settings
    else:
        client.login(username, password)
        client.dump_settings(settings_fp)
        logme(f'[green1][b][LOG]    [/] Saved the settings to [magenta1]{settings_fp}[/][/]')

    return client







def post_cat(config:dict, colors:dict, client:Client):
    war, err, pos = colors['war'], colors['err'], colors['post']
    # Gets the file info
    file_dic = get_file_path(config['eyebleach_dir'])[0]
    fp       = file_dic['fp']
    fname    = file_dic['fname']
    ext      = file_dic['ext']
    # Posts it
    posted = True
    try:
        logme(f'[{pos}][b][POST]   [/] Posting    [u magenta1]{fname}[/][/]')
        if ext == 'mp4':    client.video_upload(fp, caption= fname)
        else:               client.photo_upload(fp, caption= fname)
    # In case the photo wasnt uploaded. It usually happens because the size of the photo is incompatible. Update: Nvm, it happens cz its a png (https://github.com/adw0rd/instagrapi/issues/84)
    except PhotoNotUpload:
        logme(f'[{war}][b][WARNING][/] Converting [u magenta1]{fname}[/][/]')
        new_fp  = convert_img(fp)
        client.photo_upload(new_fp, caption=fname)
    # If its an unknown error from insta (https://github.com/adw0rd/instagrapi/issues/770)
    except UnknownError as e:
        logme(f"[{err}][b][ERROR]  [/] Can't post [u magenta1]{fname}[/] ({e})[/]")
        posted   = False
        post_cat(config, colors, client)

    # Acknowledges that it was posted
    if posted:    logme(f'[{pos}][b][POST]   [/] Posted     [u magenta1]{fname}[/][/]')
    







