# ![youtube-dl-firefox-addon](./add-on/icons/message.svg)Youtube-dl Firefox Addon
 - Firefox addon to download youtube videos using [youtube-dl](https://github.com/rg3/youtube-dl)

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-green.svg)](http://www.gnu.org/licenses/gpl-3.0) [![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=UY6TVJXST724J)

## Table of Contents

 * [What Youtube Dl Firefox Addon does](#what-youtube-dl-firefox-addon-does)
 * [Prerequisites](#prerequisites)
 * [How to install Youtube Dl Firefox Addon](#how-to-install-youtube-dl-firefox-addon)
 * [Donations](#donations)
 * [License](#license)

## What Youtube Dl Firefox Addon does

This is a firefox addon to which downloads youtube videos using [youtube-dl](https://github.com/rg3/youtube-dl).

You can configure youtube dl to download only audio, or convert into any desired format after installing, or even download full youtube playlists.

## Prerequisites

1. Needs [youtube-dl](https://github.com/rg3/youtube-dl) installed.
1. Needs python installed.

## How to install Youtube Dl Firefox Addon

1. Clone this repo
1. Add the addon [command_runner-1.0-an+fx-linux.xpi](./command_runner-1.0-an+fx-linux.xpi?raw=true) from this repo to firefox by double-clicking.
1. Edit the file [firefox_command_runner.json](./app/firefox_command_runner.json) and edit the `path` to the location of the file `./app/firefox-command-runner.py` (i.e., where you cloned this repo to.).
1. Copy the file `firefox_command_runner.json` to the folder `/home/akhil/.mozilla/native-messaging-hosts/` (create the folder if it does not exist).

## Donations
If you like this project, buy me a cup of coffee! :)

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=UY6TVJXST724J)

## License

This program is Youtube Dl Firefox Addon
Copyright (C) 2017  Akhil Kedia

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.