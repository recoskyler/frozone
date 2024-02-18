# Frozone

A tool to save and restore the position of windows using `wmctrl`.

## Requirements

- `wmctrl`
- Python >= 3.2
- pip

*Tested on Zorin OS 17 Core.*

## Installation

```bash
$ pip install frozone
```

## Usage

`frozone.py [-h] [-v] [-r] [-o OUTPUT] [-i INPUT] [-c CMD_REGEX]`

### Saving open windows

`frozone`

### Restoring open windows

`frozone -r`

### Command line arguments

|Argument|Description|
|---|---|
|`-h`, `--help`|Show the help message|
|`-v`, `--verbose`|Increase output verbosity|
|`-r`, `--restore`|Restore the windows to their previous state using the default JSON file. Can be used with `-i`, `--input` to specify the JSON file location|
|`-o OUTPUT`, `--output OUTPUT`|Set an output path for the JSON file|
|`-i INPUT`, `--input INPUT`|Set the input path for the JSON file|
|`-c CMD_REGEX`, `--cmd-regex CMD_REGEX`|Set the command regex to filter the windows to be saved|

## Configuration

`wmctrl` has an issue with positioning due to window frames. To mitigate this issue, you can configure the top and left offsets in the `~/.config/frozone/frozone.conf`.

## About

By [recoskyler](https://github.com/recoskyler) - Adil Atalay Hamamcioglu - 2024
