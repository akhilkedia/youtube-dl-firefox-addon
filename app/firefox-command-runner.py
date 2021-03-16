#!/usr/bin/env python2

""" This is started (by firefox) as follows: 

    python2 $HOME/.mozilla/native-messaging-hosts/firefox-command-runner.py    \
            $HOME/.mozilla/native-messaging-hosts/firefox_command_runner.json  \
            firefox-command-runner@example.org
"""

import sys
import os
import json
import struct
import subprocess
import tempfile
# a simple POSIX/Unix - only extension ;
# use something like multiprocessing to make it portable
import signal as S
import time
import select
import errno as E
import traceback as tb

# -------------------------------------------------------------------------
# settings

HOMEDIR = os.environ.get("HOME", '/tmp')
# replace the last '.' for 'Downloads' or whatever
DOWNLOADS = os.path.join( HOMEDIR, '.' )
WAIT_PERIOD = 1 # select() timeout, seconds

# -------------------------------------------------------------------------
# fixes

# [ https://bugs.python.org/issue1652 ]
# [ https://docs.python.org/3/library/signal.html#signal.signal ]
S.signal(S.SIGPIPE, lambda signum, stfr: None)


# -------------------------------------------------------------------------
# logging ( nb: better use syslog for this )

LOGFILE = os.path.join( HOMEDIR, '.mozilla/native-messaging-hosts/firefox-command-runner.log' )

with open(LOGFILE, 'w') as L:
    print >>L, "SIGPIPE wrapper installed at %s" % ( time.strftime('%F %T'), )


def _log(fmt, *args):
    with open(LOGFILE, 'a') as L:
        print >>L, fmt % args

# firefox' process id
PPID = None
try:
    PPID = os.getppid()
except Exception as err:
    _log('exception: %s', tb.format_exc())

# -------------------------------------------------------------------------
# helpers

# Read a message from stdin and decode it.
def getMessage():
    rawLength = sys.stdin.read(4)
    if len(rawLength) == 0:
        ## sys.exit(0)
        return None
    messageLength = struct.unpack('@I', rawLength)[0]
    raw_message = sys.stdin.read(messageLength)
    ## _log("| %r", raw_message)
    message = raw_message.decode('string_escape').strip("'\"")
    return message


# Encode a message for transmission,
# given its content.
def encodeMessage(messageContent):
    encodedContent = json.dumps(messageContent)
    encodedLength = struct.pack('@I', len(encodedContent))
    return {'length': encodedLength, 'content': encodedContent}


# Send an encoded message to stdout
def sendMessage(encodedMessage):
    sys.stdout.write(encodedMessage['length'])
    sys.stdout.write(encodedMessage['content'])
    sys.stdout.flush()

# -------------------------------------------------------------------------
# cookie handling code

# thanks @Lennon Hill for the cookie management code (see https://github.com/lennonhill/cookies-txt)
cookie_header = \
    '# Netscape HTTP Cookie File\n' + \
    '# https://curl.haxx.se/rfc/cookie_spec.html\n' + \
    '# This is a generated file! Do not edit.\n\n';

def makeCookieJar(cookies):
    with tempfile.NamedTemporaryFile(mode='w+t', suffix=".txt", delete=False) as my_jar:
        my_jar.write(cookie_header)
        my_jar.write(''.join(cookies))
        return my_jar.name


# -------------------------------------------------------------------------
# main loop

tasks = {} # { pid: (my_jar, url) }
# "reverse index"
urls = {}

while True:
    try:
        # check parent: somehow firefox does not always close us
        ppid = os.getppid()
        if PPID != ppid:
            _log("/ppid/ %d != %d /original ppid/, so it's probably time to go", ppid, PPID)
            os.exit(2)

        r_, _, _ = select.select([sys.stdin], [], [], WAIT_PERIOD)
        if r_:
        
            my_jar = None
            encodedMessage = getMessage()
            if not encodedMessage:
                continue
            # else ..
            receivedMessage = json.loads(encodedMessage) # if this fails, we try it again
            #receivedMessage = {'url':"--help", 'cookies':['bla']}
            url = receivedMessage['url']
            use_cookies = bool('cookies' in receivedMessage and receivedMessage['cookies'])

            if url not in urls:
                sendMessage(encodeMessage('Starting download: ' + url))
                try:
                    command_vec = ['youtube-dl']
                    config_path = os.path.join(os.pardir, 'config')
                    if os.path.isfile(config_path):
                        command_vec += ['--config-location', config_path]

                    if use_cookies:
                        my_jar = makeCookieJar(receivedMessage['cookies'])
                        command_vec += ['--cookies', my_jar]

                    command_vec.append(url)
                    ## sendMessage(encodeMessage('starting ' + str(command_vec)))
                    ## subprocess.check_output(command_vec)
                    pid = os.fork()
                    if 0 == pid :
                        try:
                            subprocess.check_output(command_vec, cwd=DOWNLOADS)
                        except:
                            pass
                        finally:
                            # exit the child process
                            sys.exit(0)
                    else:
                        tasks[ pid ] = ( my_jar, url)
                        urls[ url ] = pid
                        _log("[%s]: %r", pid, url)
                
                # todo: review and most likely clear this internal try .. except block
                except Exception as err:
                    sendMessage(encodeMessage('Error Running: ' + str(command_vec) + ': ' + str(err)))
            else:
                sendMessage(encodeMessage('Already downloading: ' + url))

        if tasks.keys():
            while True:
                try:
                    pid, status = os.waitpid( -1, os.WNOHANG )
                except OSError as e:
                    # no more children to wait for so far
                    if e.errno == E.ECHILD:
                        break

                # children exist, but did not yet change state
                if 0 == pid: 
                    break

                # else
                my_jar, url = tasks.pop(pid, (None, None))
                
                if url is not None:
                    if url in urls:
                        del urls[url]
                
                if my_jar is not None:
                    os.unlink(my_jar)
                if url is None :
                    _log('<%s>: unknown task', pid)
                elif status != 0:
                    _log('[%s]: %r : FAILED (%08Xh)', pid, url, status)
                    sendMessage(encodeMessage('Error downloading: %s (%08Xh)' % ( url, status)))
                else:
                    _log('[%s]: %r : Ok', pid, url)
                    sendMessage(encodeMessage('Finished downloading to %s : %r' % ( DOWNLOADS, url)))
            
            
    except Exception as err:
        ## _log('exc: %s', err)
        _log('exception: %s', tb.format_exc())
        sendMessage(encodeMessage('JSON error: ' + str(err)))

