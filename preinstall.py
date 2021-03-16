#!/usr/bin/env python2

""" 
    Installation helper for our addon.
    
    By default, this puts both firefox-command-runner.py and firefox-command-runner.json 
    under "$HOME/.mozilla/native-messaging-hosts", and edits the latter accordingly.
    
    This behaviour can be altered with a few options -- please see `./preinstall.py --help`
"""

import os
import sys
import optparse
import json
import shutil
import errno

# 1. create "$HOME/.mozilla/native-messaging-hosts"
# 2. locate 'firefox-command-runner.py' and put it there or as specified
# 3. update the dictionary and save it there as "firefox-command-runner.json"


# -------------------------------------------------------------------------
# installer data: app/firefox-command-runner.json

# // or use json.loads( open('app/firefox-command-runner.json').read() )
JSON_DATA = {
  "name": "firefox_command_runner",
  "description": "Run native linux commands from firefox",
  "path": "/home/akhil/opt/firefox-command-runner/app/firefox-command-runner.py",
  "type": "stdio",
  "allowed_extensions": [ "firefox-command-runner@example.org" ]
}


# -------------------------------------------------------------------------
# options and help strings


USAGE = """

By default, this will install app/firefox-command-runner.py' 
under "$HOME/.mozilla/native-messaging-hosts", 
along with a 'firefox-command-runner.json' file.

This machinery is needed by our FF extension to work.

See below for available options.

""".strip() 


# [ https://wiki.python.org/moin/OptParse ]
parser = optparse.OptionParser( USAGE )

parser.add_option( '--appdir', '-A'
                 , action="store", dest="command_runner_dir", metavar='APPDIR'
                 , default=None
                 , help = "where to put firefox-command-runner.py" ) 

parser.add_option( '--logdir', '-L'
                 , action="store", dest="logdir"
                 , default=None
                 , help = "where to put the log file (rewritten at every restart)" ) 


# parse command line for options 
options, args = parser.parse_args( sys.argv )



# -------------------------------------------------------------------------
# accessory code

# 'HOME' is guaranteed by POSIX -- see e.g. this Open Group spec:
# [ https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap08.html ]
# .. hence, we do not expect it to be missing and consider that a severe error
HOME = os.environ.get('HOME', None)

# By default, Firefox would expect "native messaging" folder 
# // https://wiki.mozilla.org/WebExtensions/Native_Messaging
# to be here
FF_NMDIR = os.path.join( HOME, '.mozilla/native-messaging-hosts' )


def mkdir(path):
    """ in shell terms, it's "mkdir -p $path" """
    
    try:
        os.makedirs( path )
    except OSError as e:
        if errno.EEXIST != e.errno:
            raise


# -------------------------------------------------------------------------
# ok, let us do our prerequisite install

# 1. create "$HOME/.mozilla/native-messaging-hosts"
mkdir( FF_NMDIR )

# 2. locate 'firefox-command-runner.py' and put it there or as specified
FF_RUNNER_PATH = options.command_runner_dir
if FF_RUNNER_PATH is None:
    FF_RUNNER_PATH = FF_NMDIR

shutil.copy( 'app/firefox-command-runner.py', FF_RUNNER_PATH )

# 3. update the dictionary and save it there as "firefox-command-runner.json"
runner_fullname = os.path.join( FF_RUNNER_PATH, 'firefox-command-runner.py' )
JSON_DATA['path'] = runner_fullname

if options.logdir is not None:
    JSON_DATA['logdir'] = options.logdir

with open( os.path.join(FF_NMDIR, 'firefox-command-runner.json'), 'w' ) as jsonfile:
    
    json.dump(JSON_DATA, jsonfile, indent=2)

