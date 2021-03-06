#!/usr/bin/env python
#
# Copyright (C) 2014 Cisco Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# This script will accept as a parameter an IP or range of IP address
# and attempt to ping them all from the switch it is running on
# Ranges can be specified in any octet, e.g.,
# python pingrange.py 10.1.0-1.0-255 will ping 10.1.0.0/23
#
#
import re
try:
    from cli import cli
except ImportError:
    from cisco import cli
from argparse import ArgumentParser




def get_range(octet):
    if(octet.find("-") == -1):

        return range(int(octet),int(octet)+1)

    ints = octet.split("-")
    return range(int(ints[0]), int(ints[1])+1)

def expandrange(ip_addr):

    ip_addr = ip_addr.split(".")
    for octet1 in get_range(ip_addr[0]):
        for octet2 in get_range(ip_addr[1]):
            for octet3 in get_range(ip_addr[2]):
                for octet4 in get_range(ip_addr[3]):
                    yield str(octet1) + "." + str(octet2) + "." + str(octet3) + "." + str(octet4)


parser = ArgumentParser('pingrange')
parser.add_argument('ip', help='IP range to ping, e.g., 10.1.0-1.0-255 will expand to 10.1.0.0/23')
parser.add_argument('options', nargs='*', help='Options to pass to ping', default=['count 1'])
args = parser.parse_args()
targets = expandrange(args.ip)

for ip in targets:
    m = re.search('([0-9\.]+)% packet loss', cli('ping %s %s' % (ip, ' '.join(args.options))))
    print('%s - %s' % (ip, 'UP' if float(m.group(1)) == 0.0 else 'DOWN'))