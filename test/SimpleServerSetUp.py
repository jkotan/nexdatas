#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012 Jan Kotanski
#
#    nexdatas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nexdatas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nexdatas.  If not, see <http://www.gnu.org/licenses/>.
## \package test nexdatas
## \file ServerSetUp.py
# class with server settings
#
import unittest
import os
import sys
import subprocess

import PyTango
import time
from pni.nx.h5 import open_file
from  xml.sax import SAXParseException
import SimpleServer


## test fixture
class SimpleServerSetUp(object):

    ## constructor
    # \brief defines server parameters
    def __init__(self):
        ## information about tango writer
        self.new_device_info_writer = PyTango.DbDevInfo()
        self.new_device_info_writer._class = "SimpleServer"
        self.new_device_info_writer.server = "SimpleServer/S1"
        self.new_device_info_writer.name = "stestp09/testss/s1r228"

        self._psub = None



    ## test starter
    # \brief Common set up of Tango Server
    def setUp(self):
        print "\nsetting up..."
        db = PyTango.Database()
        db.add_device(self.new_device_info_writer)
        db.add_server(self.new_device_info_writer.server, self.new_device_info_writer)

        path = os.path.dirname(SimpleServer.__file__)
        
        if os.path.isfile("%s/ST" % path):
            self._psub = subprocess.Popen(
                "cd %s; ./ST S1 &" % path ,stdout =  subprocess.PIPE, 
                stderr =  subprocess.PIPE,  shell= True)
        print "waiting for simple server",
        
        found = False
        cnt = 0
        while not found and cnt < 1000:
            try:
                print "\b.",
                dp = PyTango.DeviceProxy(self.new_device_info_writer.name)
                time.sleep(0.01)
                if dp.state() == PyTango.DevState.ON:
                    found = True
            except:    
                found = False
            cnt +=1
        print ""

    ## test closer
    # \brief Common tear down oif Tango Server
    def tearDown(self): 
        print "tearing down ..."
        db = PyTango.Database()
        db.delete_server(self.new_device_info_writer.server)
        
        output = ""
        pipe = subprocess.Popen(
            "ps -ef | grep 'SimpleServer.py S1'", stdout=subprocess.PIPE , shell= True).stdout

        res = pipe.read().split("\n")
        for r in res:
            sr = r.split()
            if len(sr)>2:
                 subprocess.call("kill -9 %s" % sr[1],stderr=subprocess.PIPE , shell= True)

        

if __name__ == "__main__":
    simps = SimpleServerSetUp()
    simps.setUp()
    dp = PyTango.DeviceProxy("stestp09/testss/s1r228")
    print dp.status()
    simps.tearDown()
