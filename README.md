# ![youtube-dl-firefox-addon](./add-on/icons/message.svg)Youtube-dl Firefox Addon
 - Firefox addon to download youtube videos using [youtube-dl](https://github.com/rg3/youtube-dl)

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-green.svg)](http://www.gnu.org/licenses/gpl-3.0) [![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=UY6TVJXST724J) ![Mozilla Add-on](https://img.shields.io/amo/users/youtube-dl-for-linux?style=social)

## Table of Contents

 * [What Youtube Dl Firefox Addon does](#what-youtube-dl-firefox-addon-does)
 * [Prerequisites](#prerequisites)
 * [How to install Youtube Dl Firefox Addon](#how-to-install-youtube-dl-firefox-addon)
 * [How to use this addon](#how-to-use-this-addon)
 * [Donations](#donations)
 * [License](#license)

## What Youtube Dl Firefox Addon does

This is a firefox addon to which downloads youtube videos using [youtube-dl](https://github.com/rg3/youtube-dl).

You can configure youtube-dl to download only audio, or convert into any desired format after installing, or even download full youtube playlists. These options are controlled via youtube-dl's own [configuration](https://github.com/ytdl-org/youtube-dl#configuration)

## Prerequisites

1. Needs [youtube-dl](https://github.com/rg3/youtube-dl) installed.
1. Needs python installed.
1. This has only been tested on Ubuntu linux, but should ideally work on all platforms where youtube-dl works. You will need to change the path for the `firefox_command_runner.json` for other platforms.

## How to install Youtube Dl Firefox Addon

1. Clone this repo
2. Install the add on from [Firefox Addons Website](https://addons.mozilla.org/en-US/firefox/addon/youtube-dl-for-linux/). Or you can install the addon [command_runner-1.0-an+fx-linux.xpi](./command_runner-1.0-an+fx-linux.xpi?raw=true) from this repo to firefox by double-clicking.
3. Edit the file [firefox_command_runner.json](./app/firefox_command_runner.json) and edit the `path` to the location of the file `./app/firefox-command-runner.py` (i.e., where you cloned this repo to.).
4. Edit the [local youtube-dl config](config) to fit your needs or delete it to use youtube-dl's global configuration
5. Copy the file `firefox_command_runner.json` to the folder `/home/<username>/.mozilla/native-messaging-hosts/` (replace `<username>` wtih your own username. Create the folder if it does not exist).

## How to use this addon

1. Go to any youtube video page
1. Press the addon's logo in the toolbar once. (The logo looks like a YouTube icon).
1. The video will be downloaded automatically in the background.
1. After the download is finished, you will get a notification saying the download has finished. For the download locations, format, etc, please see youtube-dl's own [configuration](https://github.com/ytdl-org/youtube-dl#configuration)

## Donations
If you like this project, buy me a cup of coffee! :)

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=UY6TVJXST724J)

## License

This program is Youtube Dl Firefox Addon
Copyright (C) 2017  Akhil Kedia

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
