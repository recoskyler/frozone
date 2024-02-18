#!/usr/bin/env python3

import argparse
from subprocess import PIPE, run, check_output
from os.path import expanduser, dirname

display = ':0.0'
top_offset = -80
left_offset = -10
cmd_regex = '.*'
config_path = expanduser('~/.config/frozone/frozone.conf')

def create_config():
    global config_path
    global left_offset
    global top_offset
    global cmd_regex

    from os.path import exists

    if exists(config_path):
        # print("The configuration file already exists")
        return

    from configparser import ConfigParser
    from os import makedirs

    makedirs(dirname(config_path), exist_ok=True)

    config = ConfigParser()

    config['DEFAULT'] = {
        'left_offset': left_offset,
        'top_offset': top_offset,
        'cmd_regex': cmd_regex
    }

    with open(config_path, 'w') as config_file:
        config.write(config_file)

def get_config():
    config_path = expanduser('~/.config/frozone/frozone.conf')

    from os.path import exists

    if not exists(config_path):
        create_config()

    from configparser import ConfigParser

    config = ConfigParser()
    config.read(config_path)

    return config['DEFAULT']

def print_window_details(window):
    print(f'Title: {window["title"]}')
    print(f'X: {window["x_offset"]}')
    print(f'Y: {window["y_offset"]}')
    print(f'Width: {window["width"]}')
    print(f'Height: {window["height"]}')
    print(f'Command: {window["cmd"]}')
    print(f'Desktop: {window["desktop"]}')
    print("-------------------------------------------")

def get_window_cmd(pid):
    output = check_output(f'ps -aux | grep {pid}', shell=True).decode('utf-8').strip().split('\n')[0]

    return output.split(maxsplit=10)[10]

# def get_window_frame(wid):
#     global top
#     global left

#     #  _NET_FRAME_EXTENTS(CARDINAL): left, right, top, bottom

#     try:
#         output = check_output(f'xprop -id {wid} | grep FRAME', shell=True).decode('utf-8').strip().split('=')[1].strip().split(',')

#         o_left = int(output[0].strip())
#         o_top = int(output[2].strip())

#         left = o_left if o_left > left else left
#         top = o_top if o_top > top else top

#         return o_left, o_top
#     except:
#         return left, top

def get_windows():
    global display
    global args
    global top_offset
    global left_offset

    cmd = "wmctrl -lpG"
    output = check_output(cmd.split(), stderr=PIPE).decode('utf-8').strip()

    lines = output.split('\n')

    windows = []

    for line in lines:
        window = line.split(maxsplit=8)

        wid = window[0]
        desktop = int(window[1])
        pid = window[2]
        x_offset = int(window[3])
        y_offset = int(window[4])
        width = int(window[5])
        height = int(window[6])
        title = window[8]

        cmd = get_window_cmd(pid)

        if not cmd:
            print(f"Could not get the command for the window with title {title}")
            continue

        import re

        if args.cmd_regex:
            if not re.match(args.cmd_regex, cmd):
                continue
        else:
            if not re.match(cmd_regex, cmd):
                continue

        window = {
            'x_offset': x_offset,
            'y_offset': y_offset,
            'width': width,
            'height': height,
            'title': title,
            'cmd': cmd,
            'desktop': desktop
        }

        if args.verbose:
            print_window_details(window)

        windows.append(window)

    return windows

def save_windows(windows):
    global args

    json_path = args.output if args.output else './windows.json'

    if not json_path.endswith('.json'):
        print("The output file must be a JSON file")
        return

    import json

    json_path = expanduser(json_path)

    print(f"Saving windows to {json_path}")

    with open(json_path, 'w') as file:
        json.dump(windows, file, indent=4)

def restore_windows():
    global args
    global top_offset
    global left_offset

    json_path = args.input if args.input else './windows.json'

    if not json_path.endswith('.json'):
        print("The input file must be a JSON file")
        return

    import json
    from operator import itemgetter
    from os.path import exists

    json_path = expanduser(json_path)

    print(f"Restoring windows from {json_path}")

    if not exists(json_path):
        print(f"The file {json_path} does not exist")
        return

    with open(json_path, 'r') as file:
        windows = json.load(file)

    windows.sort(key=itemgetter('desktop'))

    for window in windows:
        x_offset = window['x_offset'] + left_offset
        y_offset = window['y_offset'] + top_offset
        width = window['width']
        height = window['height']
        title = window['title']
        cmd = window['cmd']
        desktop = window['desktop']

        if args.verbose:
            print_window_details(window)

        run(f'./frozone.sh "{cmd}" {x_offset} {y_offset} {width} {height} {desktop}', shell=True)

def main():
    global display
    global args
    global top_offset
    global left_offset
    global cmd_regex

    parser = define_args()
    args = parser.parse_args()

    if args.output and args.restore:
        print("You cannot use -o and -r at the same time")
        exit()

    config = get_config()

    left_offset = config.getint('left_offset', left_offset)
    top_offset = config.getint('top_offset', top_offset)
    cmd_regex = config.get('cmd_regex', cmd_regex)

    from os import environ

    display = environ.get('DISPLAY', ':0')

    if args.restore:
        restore_windows()
        return

    windows = get_windows()
    save_windows(windows)

def define_args():
    parser = argparse.ArgumentParser(description="Frozone is a tool to save and restore the position of windows using wmctrl. Configuration file can be found at ~/.config/frozone/frozone.conf")

    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true"
    )

    parser.add_argument(
        "-r",
        "--restore",
        help="restore the windows to their previous state using the default JSON file",
        action="store_true"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="set an output path for the JSON file"
    )

    parser.add_argument(
        "-i",
        "--input",
        help="set the input path for the JSON file"
    )

    parser.add_argument(
        "-c",
        "--cmd-regex",
        help="set the command regex to filter the windows to be saved",
    )

    return parser

if __name__ == '__main__':
    main()
