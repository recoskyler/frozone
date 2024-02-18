import click
from subprocess import PIPE, run, check_output
from os.path import expanduser, dirname

display = ':0.0'
top_offset = -80
left_offset = -10
config_path = expanduser('~/.config/frozone/frozone.conf')
default_windows_path = '~/.config/frozone/windows.json'

def print_verbose(verbose, message):
    if verbose:
        print(message)

def create_config(verbose):
    global config_path
    global left_offset
    global top_offset

    from os.path import exists

    if exists(config_path):
        print_verbose(verbose, "The configuration file already exists")
        return

    from configparser import ConfigParser
    from os import makedirs

    makedirs(dirname(config_path), exist_ok=True)

    config = ConfigParser()

    config['DEFAULT'] = {
        'left_offset': left_offset,
        'top_offset': top_offset,
        'cmd_regex': ".*"
    }

    with open(config_path, 'w') as config_file:
        config.write(config_file)

    print_verbose(verbose, f"Configuration file created at {config_path}")

def get_config(verbose):
    global config_path

    config_path = expanduser(config_path)

    print_verbose(verbose, f'Getting configuration from {config_path}')

    from os.path import exists

    if not exists(config_path):
        create_config(verbose)

    from configparser import ConfigParser

    config = ConfigParser()
    config.read(config_path)

    print_verbose(verbose, 'Configuration file read')

    return config['DEFAULT']

def print_window_details(verbose, window):
    print_verbose(verbose, f'Title: {window["title"]}')
    print_verbose(verbose, f'X: {window["x_offset"]}')
    print_verbose(verbose, f'Y: {window["y_offset"]}')
    print_verbose(verbose, f'Width: {window["width"]}')
    print_verbose(verbose, f'Height: {window["height"]}')
    print_verbose(verbose, f'Command: {window["cmd"]}')
    print_verbose(verbose, f'Desktop: {window["desktop"]}')
    print_verbose(verbose, "-------------------------------------------")

def get_window_cmd(verbose, pid):
    print_verbose(verbose, f'Getting command for window with PID {pid}')

    output = check_output(f'ps -aux | grep {pid}', shell=True).decode('utf-8').strip().split('\n')[0]

    return output.split(maxsplit=10)[10]

def get_windows(verbose, cmd_regex):
    global display

    print_verbose(verbose, 'Getting windows...')

    cmd = "wmctrl -lpG"
    output = check_output(cmd.split(), stderr=PIPE).decode('utf-8').strip()

    print_verbose(verbose, 'Windows retrieved')

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

        cmd = get_window_cmd(verbose, pid)

        if not cmd:
            print(f"Could not get the command for the window with title {title}")
            continue

        import re

        print_verbose(verbose, f"Checking {cmd} against {cmd_regex}")

        if not re.match(cmd_regex, cmd):
            print_verbose(verbose, f'Command {cmd} does not match the regex {cmd_regex}')
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

        print_window_details(verbose, window)

        windows.append(window)

    return windows

def save_windows(verbose, windows, output):
    global default_windows_path

    json_path = output if output else default_windows_path

    if not json_path.endswith('.json'):
        print("The output file must be a JSON file")
        return

    import json

    json_path = expanduser(json_path)

    print_verbose(verbose, f"Saving windows to {json_path}")

    with open(json_path, 'w') as file:
        json.dump(windows, file, indent=4)

def restore_windows(verbose, input_):
    global top_offset
    global left_offset
    global default_windows_path

    json_path = input_ if input_ else default_windows_path

    if not json_path.endswith('.json'):
        print("The input file must be a JSON file")
        return

    import json
    from operator import itemgetter
    from os.path import exists

    json_path = expanduser(json_path)

    print_verbose(verbose, f"Restoring windows from {json_path}")

    if not exists(json_path):
        print(f"The file {json_path} does not exist")
        return

    with open(json_path, 'r') as file:
        windows = json.load(file)

    windows.sort(key=itemgetter('desktop'))

    print_verbose(verbose, 'Restoring windows...')

    for window in windows:
        x_offset = window['x_offset'] + left_offset
        y_offset = window['y_offset'] + top_offset
        width = window['width']
        height = window['height']
        title = window['title']
        cmd = window['cmd']
        desktop = window['desktop']

        print_window_details(verbose, window)

        run(f'restore.sh "{cmd}" {x_offset} {y_offset} {width} {height} {desktop}', shell=True)

@click.command()
@click.option('-v', '--verbose', is_flag=True, help="increase output verbosity", default=False, show_default=True)
@click.option('-o', '--output', help="set an output path for the JSON file", default="~/.config/frozone/windows.json", show_default=True)
@click.option('-c', '--cmd-regex', "cmd_regex", help="set the command regex to filter the windows to be saved", default=None, show_default=False)
def freeze(verbose, output, cmd_regex):
    global display

    config = get_config(verbose)

    cmd_regex = cmd_regex if cmd_regex else config.get('cmd_regex', ".*")

    from os import environ

    display = environ.get('DISPLAY', ':0')
    windows = get_windows(verbose, cmd_regex)

    save_windows(verbose, windows, output)

@click.command()
@click.option('-v', '--verbose', is_flag=True, help="increase output verbosity", default=False, show_default=True)
@click.option('-i', '--input', 'input_', help="set the input path for the JSON file", default="~/.config/frozone/windows.json", show_default=True)
def restore(verbose, input_):
    global display
    global top_offset
    global left_offset

    config = get_config(verbose)

    left_offset = config.getint('left_offset', left_offset)
    top_offset = config.getint('top_offset', top_offset)

    from os import environ

    display = environ.get('DISPLAY', ':0')

    restore_windows(verbose, input_)
