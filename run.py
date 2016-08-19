#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Sibyl: A modular Python chat bot framework
# Copyright (c) 2015-2016 Joshua Haas <jahschwa.com>
#
# This file is part of Sibyl.
#
# Sibyl is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

import sys,os,argparse

from lib.sibylbot import SibylBot

def main():

  # change directories so cmds can imports and saving files works correctly
  current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'.'))
  os.chdir(current_dir)

  # parse command line arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-c',default='sibyl.conf',help='path to config file',metavar='file')
  parser.add_argument('-d',action='store_true',help='run as daemon')
  args = parser.parse_args()

  # initialise bot (plug-in and config errors will occur here)
  bot = SibylBot(args.c)

  # if we're running as a daemon we need to put our PID in the pidfile
  if args.d:
    with open('/var/run/sibyl/sibyl.pid','w') as f:
      f.write(str(os.getpid()))

  # run the bot and store reboot flag
  reboot = bot.run_forever()

  # remove the pid file
  if args.d:
    os.remove('/var/run/sibyl/sibyl.pid')

  # reboot if needed
  if reboot:
    python = sys.executable
    this = os.path.abspath(os.path.basename(__file__))
    args = [python,this]
    args.extend(sys.argv[1:])
    os.execv(python,args)

if __name__ == '__main__':
  main()
