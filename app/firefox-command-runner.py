#!/usr/bin/env python2

import sys
import os
import json
import struct
import subprocess
import tempfile

# Read a message from stdin and decode it.
def getMessage():
    rawLength = sys.stdin.read(4)
    if len(rawLength) == 0:
        sys.exit(0)
    messageLength = struct.unpack('@I', rawLength)[0]
    message = sys.stdin.read(messageLength).decode('string_escape').strip("'\"")
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

# thanks @Lennon Hill for the cookie management code (see https://github.com/lennonhill/cookies-txt)
cookie_header = \
    '# Netscape HTTP Cookie File\n' + \
    '# https://curl.haxx.se/rfc/cookie_spec.html\n' + \
    '# This is a generated file! Do not edit.\n\n';

def makeCookieJar(cookies):
    subprocess.check_output(['/tmp/echo_me', "making cookie jar"])
    with tempfile.NamedTemporaryFile(mode='w+t', suffix=".txt", delete=False) as my_jar:
        my_jar.write(cookie_header)
        my_jar.write(''.join(cookies))
        return my_jar.name

while True:
    try:
        receivedMessage = json.loads(getMessage())
        #receivedMessage = {'url':"--help"}
    except Exception as err:
        sendMessage(encodeMessage('JSON error: ' + str(err)))

    # sendMessage(encodeMessage('Starting Download: ' + url))
    url = receivedMessage.get('url', '');
    try:
        command_vec = ['youtube-dl']
        if os.path.isfile('../config'):
            command_vec += ['--config-location', '../config']
        
        if 'cookies' in receivedMessage and receivedMessage['cookies']:
            my_jar = makeCookieJar(receivedMessage['cookies'])
            subprocess.check_output(command_vec + ['--cookies', my_jar, url])
            os.unlink(my_jar)
        else:
            subprocess.check_output(command_vec + [url])

        sendMessage(encodeMessage('Finished Downloading to /data/down: ' + url))
    except Exception as err:
        sendMessage(encodeMessage('Some Error Downloading: ' + url + ': ' + str(err)))

