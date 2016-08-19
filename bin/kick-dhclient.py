# coding=utf-8
#
# Copyright 2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Kick the dhclient process on Virtualbox BIG-IP.
#
# When BIG-IP comes back from a snapshot state, the networking is not
# functional. One might normally wait for dhclient to resolve this issue
# by having it reach out for an IP address from Virtualbox's built-in
# DHCP service.
#
# While this method will work, the time interval between when dhclient
# will refresh the eth0 IP address, and when you might want to start
# using BIG-IP (immediately) might be too long.
#
# Consider this Virtualbox image being used in a test sequence where you
# want near immediate access to your restored BIG-IP. Without this script,
# you would need to wait the default dhclient timeout period before running
# your tests. This can be 300 or more seconds which is far too long to wait
# when doing more rapid development.
#
# By bouncing dhclient, you are effectively bringing BIG-IP back online
# within seconds.
#
# Usage:
#
#    python kick-dhclient.py --vmname XXXX
#
# Examples:
#
#    Kick the dhclient process on BIG-IP named big-ip01.internal
#
#    python kick-dhclient.py --vmname big-ip01.internal
#
# Arguments:
#
#    vmname       The name of the BIG-IP virtual machine in Virtualbox
#

import subprocess
import time
import argparse

SCAN_CODES = {
    '1': '02', '2': '03', '3': '04', '4': '05', '5': '06', '6': '07', '7': '08',
    '8': '09', '9': '0A', '0': '0B', '-': '0C', '=': '0D', '<bs>': '0E',
    '<tab>': '0F', 'q': '10', 'w': '11', 'e': '12', 'r': '13', 't': '14',
    'y': '15', 'u': '16', 'i': '17', 'o': '18', 'p': '19', '[': '1A',
    ']': '1B', '<enter>': '1C', '<ctrl>': '1D', 'a': '1E', 's': '1F',
    'd': '20', 'f': '21', 'g': '22', 'h': '23', 'j': '24', 'k': '25',
    'l': '26', ';': '27', '<shift>': '2A', 'z': '2C', 'x': '2D', 'c': '2E',
    'v': '2F', 'b': '30', 'n': '31', 'm': '32', ',': '33', '.': '34', '/': '35',
    ' ': '39'
}

def command(cmd):
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout,stderr = p.communicate()
    if stderr or 'pause' in stdout or 'savestate' in stdout:
        raise Exception(stderr)

def keyboardputscancode(vmname, codes):
    codes = reduce(lambda x,y: x + y, codes, [])
    cmd = [
        'vboxmanage',
        'controlvm',
        vmname,
        'keyboardputscancode'
    ]
    cmd += codes
    command(cmd)

def getBreakCode(key):
    if key not in SCAN_CODES:
        raise Exception('Undefined key: ' + key)
    makeCode = SCAN_CODES[key]
    a = int(makeCode, 16)
    b = int('80', 16)
    c = a + b
    d = format(c, 'x')
    return d

def toScanCode(s):
    result = []
    tmp = ''
    special = False

    for c in s:
        if c == '<':
            tmp = tmp + c
            special = True
            continue
        elif c == '>':
            tmp = tmp + c
            special = False
            c = tmp
            tmp = ''
        elif special:
            tmp = tmp + c
            continue

        if c == c.upper() and not c.isdigit() and c is not ' ':
            stopCodeShift = getBreakCode('<shift>')
            stopCodeInput = getBreakCode(c)
            result.append([
                SCAN_CODES['<shift>'],
                SCAN_CODES[c],
                stopCodeInput,
                stopCodeShift
            ])
        else:
            stopCode = getBreakCode(c)
            result.append([
                SCAN_CODES[c],
                stopCode
            ])
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Re-kicks dhclient after restoring snapshot'
    )
    parser.add_argument('--vmname',
                        help='The name of the virtual machine in Virtualbox',
                        required=True)
    args = parser.parse_args()

    codes = [
        'root<enter>',
        'default<enter>',
        'killall dhclient<enter>',
        'dhclient eth0<enter>',
        'exit<enter>'
    ]

    for code in codes:
        sc = toScanCode(code)
        keyboardputscancode(args.vmname, sc)
        time.sleep(.5)