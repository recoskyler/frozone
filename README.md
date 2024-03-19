# Frozone

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/frozone)](https://pypi.org/project/frozone)

<a href='https://ko-fi.com/recoskyler' target='_blank'><img height='35' style='border:0px;height:46px;' src='https://az743702.vo.msecnd.net/cdn/kofi3.png?v=0' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

A tool to save and restore the position of windows using `wmctrl`.

## Requirements

- `wmctrl`
- Python >= 3.2
- pip

*Tested on Zorin OS 17 Core.*

## Installation

```bash
$ pip3 install frozone
```

## Usage

### Saving open windows

`frozone freeze`

### Restoring open windows

`frozone restore`

### Command line arguments

|Argument|Description|
|---|---|
|`--help`|Show the help message|
|`-v`, `--verbose`|Increase output verbosity|
|`-r`, `--restore`|Restore the windows to their previous state using the default JSON file. Can be used with `-i`, `--input` to specify the JSON file location|
|`-o OUTPUT`, `--output OUTPUT`|Set an output path for the JSON file|
|`-i INPUT`, `--input INPUT`|Set the input path for the JSON file|
|`-c CMD_REGEX`, `--cmd-regex CMD_REGEX`|Set the command regex to filter the windows to be saved|

## Configuration

`wmctrl` has an issue with positioning due to window frames. To mitigate this issue, you can configure the top and left offsets in the `~/.config/frozone/frozone.conf`.

`cmd_regex` can also be configured in the same file.

## About

By [recoskyler](https://github.com/recoskyler) - Adil Atalay Hamamcioglu - 2024
