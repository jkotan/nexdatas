#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012-2017 DESY, Jan Kotanski <jkotan@mail.desy.de>
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
## \file ElementTest.py
# unittests for field Tags running Tango Server
#
import unittest
import os
import sys
import subprocess
import struct
import random
import binascii
import string
import h5py

import nxswriter.FileWriter as FileWriter
import nxswriter.H5PYWriter as H5PYWriter


## if 64-bit machione
IS64BIT = (struct.calcsize("P") == 8)

class testwriter(object):
    def __init__(self):
        self.commands = []
        self.params = []
        self.result = None

    def open_file(self, filename, readonly=False):
        """ open the new file
        """
        self.commands.append("open_file")
        self.params.append([filename, readonly])
        return self.result


    def create_file(self,filename, overwrite=False):
        """ create a new file
        """
        self.commands.append("create_file")
        self.params.append([filename, overwrite])
        return self.result


    def link(self,target, parent, name):
        """ create link
        """
        self.commands.append("link")
        self.params.append([target, parent, name])
        return self.result


    def deflate_filter(self):
        self.commands.append("deflate_filter")
        self.params.append([])
        return self.result




## test fixture
class H5PYWriterTest(unittest.TestCase):

    ## constructor
    # \param methodName name of the test method
    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)

        try:
            self.__seed  = long(binascii.hexlify(os.urandom(16)), 16)
        except NotImplementedError:
            self.__seed  = long(time.time() * 256)
#        self.__seed =241361343400098333007607831038323262554

        self.__rnd = random.Random(self.__seed)


    ## Exception tester
    # \param exception expected exception
    # \param method called method
    # \param args list with method arguments
    # \param kwargs dictionary with method arguments
    def myAssertRaise(self, exception, method, *args, **kwargs):
        try:
            error =  False
            method(*args, **kwargs)
        except exception, e:
            error = True
        self.assertEqual(error, True)


    ## test starter
    # \brief Common set up
    def setUp(self):
        print "\nsetting up..."
        print "SEED =", self.__seed

    ## test closer
    # \brief Common tear down
    def tearDown(self):
        print "tearing down ..."

    ## constructor test
    # \brief It tests default settings
    def test_constructor(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)
        w = "weerew"
        el = FileWriter.FTObject(w)

        self.assertEqual(el.h5object, w)

    ## default createfile test
    # \brief It tests default settings
    def test_default_createfile(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)
        self._fname= '%s/%s%s.h5' % (os.getcwd(), self.__class__.__name__, fun )
        try:
            fl = H5PYWriter.create_file(self._fname)
            fl.close()
            fl = H5PYWriter.create_file(self._fname, True)
            fl.close()

            fl = H5PYWriter.open_file(self._fname, readonly=True)
            f = fl.root()
            self.assertEqual(6, len(f.attributes))
            self.assertEqual(
                f.attributes["file_name"][...],
                self._fname)
            for at in f.attributes:
                print at.name , at.read() , at.dtype
                at.close()
            self.assertTrue(f.attributes["NX_class"][...],"NXroot")
            self.assertEqual(f.size, 0)
            f.close()
            fl.close()

            fl = H5PYWriter.open_file(self._fname, readonly=True)
            f = fl.root()
            self.assertEqual(6, len(f.attributes))
            self.assertEqual(
                f.attributes["file_name"][...],
                self._fname)
            for at in f.attributes:
                print at.name ,  at.dtype, at.read()
            self.assertTrue(f.attributes["NX_class"][...],"NXroot")
            self.assertEqual(f.size, 0)
            fl.close()
            fl.reopen()
            self.assertEqual(6, len(f.attributes))
            atts = []
            for at in f.attributes:
                print at.name , at.read() , at.dtype
            self.assertEqual(
                f.attributes["file_name"][...],
                self._fname)
            self.assertTrue(f.attributes["NX_class"][...],"NXroot")
            self.assertEqual(f.size, 0)
            fl.close()

            self.myAssertRaise(
                Exception, H5PYWriter.create_file, self._fname)

            self.myAssertRaise(
                Exception, H5PYWriter.create_file, self._fname,
                False)

            fl2 = H5PYWriter.create_file(self._fname, True)
            fl2.close()

        finally:
            os.remove(self._fname)


    ## default createfile test
    # \brief It tests default settings
    def test_h5pyfile(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)
        self._fname= '%s/%s%s.h5' % (os.getcwd(), self.__class__.__name__, fun )

        overwrite = False
        nxfl = h5py.File(self._fname, "a", libver='latest')
        fl = H5PYWriter.H5PYFile(nxfl, self._fname)
        self.assertTrue(
            isinstance(fl, FileWriter.FTFile))

        self.assertEqual(fl.name, self._fname)
        self.assertEqual(fl.path, None)
        self.assertTrue(
            isinstance(fl.h5object, h5py.File))
        self.assertEqual(fl.parent, None)

        rt = fl.root()
        fl.flush()
        self.assertEqual(fl.h5object, rt.h5object)
        self.assertEqual(fl.is_valid, True)
        self.assertEqual(fl.h5object.name is not None, True)
        self.assertEqual(fl.readonly, False)
        self.assertEqual(fl.h5object.mode in ["r"], False)
        fl.close()
        self.assertEqual(fl.is_valid, False)
        self.assertEqual(fl.readonly, None)

        fl.reopen()
        self.assertEqual(fl.name, self._fname)
        self.assertEqual(fl.path, None)
        self.assertTrue(
            isinstance(fl.h5object, h5py.File))
        self.assertEqual(fl.parent, None)
        self.assertEqual(fl.readonly, False)
        self.assertEqual(fl.h5object.mode in ["r"], False)

        fl.close()

        fl.reopen(True)
        self.assertEqual(fl.name, self._fname)
        self.assertEqual(fl.path, None)
        self.assertTrue(
            isinstance(fl.h5object, h5py.File))
        self.assertEqual(fl.parent, None)
        self.assertEqual(fl.readonly, True)
        self.assertEqual(fl.h5object.mode in ["r"], True)

        fl.close()

        self.myAssertRaise(
            Exception, fl.reopen, True, True)
        self.myAssertRaise(
            Exception, fl.reopen, False, True)


        fl = H5PYWriter.open_file(self._fname, readonly=True)
        f = fl.root()
        self.assertEqual(1, len(f.attributes))
        atts = []
        for at in f.attributes:
            print at.name, at.read(), at.dtype
#        self.assertEqual(
#            f.attributes["file_name"][...],
#            self._fname)
#        self.assertTrue(
#            f.attributes["NX_class"][...], "NXroot")
        self.assertEqual(f.size, 0)
        fl.close()

        os.remove(self._fname)


    ## default createfile test
    # \brief It tests default settings
    def test_h5pygroup(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)
        self._fname= '%s/%s%s.h5' % (os.getcwd(), self.__class__.__name__, fun)

        try:
            overwrite = False
            fl = H5PYWriter.create_file(self._fname)

            rt = fl.root()
            nt = rt.create_group("notype")
            entry = rt.create_group("entry12345", "NXentry")
            ins = entry.create_group("instrument", "NXinstrument")
            det = ins.create_group("detector", "NXdetector")
            dt = entry.create_group("data", "NXdata")

            df0 = H5PYWriter.deflate_filter()
            df1 = H5PYWriter.deflate_filter()
            df1.rate = 2
            df2 = H5PYWriter.deflate_filter()
            df2.rate = 4
            df2.shuffle = 6

            strscalar = entry.create_field("strscalar", "string")
            floatscalar = entry.create_field("floatscalar", "float64")
            intscalar = entry.create_field("intscalar", "uint64")
            strspec = ins.create_field("strspec", "string", [10], [6])
            floatspec = ins.create_field("floatspec", "float32", [20], [16])
            intspec = ins.create_field("intspec", "int64", [30], [5])
            strimage = det.create_field("strimage", "string", [2,2], [2,1])
            floatimage = det.create_field(
                "floatimage", "float64", [20,10], dfilter=df0)
            intimage = det.create_field("intimage", "uint32", [0, 30], [1, 30])
            strvec = det.create_field("strvec", "string", [0,2,2], [1,2,2])
            floatvec = det.create_field(
                "floatvec", "float64", [1, 20,10], [1, 10, 10], dfilter=df1)
            intvec = det.create_field(
                "intvec", "uint32", [0, 2, 30], dfilter=df2)


            lkintimage = H5PYWriter.link(
                "/entry12345/instrument/detector/intimage", dt, "lkintimage")
            lkfloatvec = H5PYWriter.link(
                "/entry12345/instrument/detector/floatvec", dt, "lkfloatvec")
            lkintspec = H5PYWriter.link(
                "/entry12345/instrument/intspec", dt, "lkintspec")
            lkdet = H5PYWriter.link(
                "/entry12345/instrument/detector", dt, "lkdet")
            lkno = H5PYWriter.link(
                "/notype/unknown", dt, "lkno")


            attr0 = rt.attributes
            attr1 = entry.attributes

            print attr0.h5object
            self.assertTrue(isinstance(attr0, H5PYWriter.H5PYAttributeManager))
            print dir(attr0.h5object)
            self.assertTrue(
                isinstance(attr0.h5object, h5py.AttributeManager))
            self.assertTrue(isinstance(attr1, H5PYWriter.H5PYAttributeManager))
            self.assertTrue(
                isinstance(attr1.h5object, h5py.AttributeManager))

            print dir(rt)
            self.assertTrue(
                isinstance(rt, H5PYWriter.H5PYGroup))
            self.assertEqual(rt.name, "/")
            self.assertEqual(rt.path, "/")
            attr = rt.attributes
            self.assertEqual(attr["NX_class"][...], "NXroot")
            self.assertTrue(
                isinstance(attr, H5PYWriter.H5PYAttributeManager))
            self.assertEqual(rt.is_valid, True)
            self.assertEqual(rt.parent, fl)
            self.assertEqual(rt.size, 2)
            self.assertEqual(rt.exists("entry12345"), True)
            self.assertEqual(rt.exists("notype"), True)
            self.assertEqual(rt.exists("strument"), False)

            for rr in rt:
                print rr.name

            self.assertTrue(
                isinstance(entry, H5PYWriter.H5PYGroup))
            self.assertEqual(entry.name, "entry12345")
            self.assertEqual(entry.path, "/entry12345:NXentry")
            self.assertEqual(
                len(entry.h5object.attrs), 1)
            attr = entry.attributes
            self.assertEqual(attr["NX_class"][...], "NXentry")
            self.assertTrue(
                isinstance(attr, H5PYWriter.H5PYAttributeManager))
            self.assertEqual(entry.is_valid, True)
            self.assertEqual(entry.parent, rt)
            self.assertEqual(entry.size, 5)
            self.assertEqual(entry.exists("instrument"), True)
            self.assertEqual(entry.exists("data"), True)
            self.assertEqual(entry.exists("floatscalar"), True)
            self.assertEqual(entry.exists("intscalar"), True)
            self.assertEqual(entry.exists("strscalar"), True)
            self.assertEqual(entry.exists("strument"), False)


            self.assertTrue(
                isinstance(nt, H5PYWriter.H5PYGroup))
            self.assertEqual(nt.name, "notype")
            self.assertEqual(nt.path, "/notype")
            print nt.h5object.attrs.keys()
            self.assertEqual(
                len(nt.h5object.attrs), 0)
            attr = nt.attributes
            self.assertTrue(
                isinstance(attr, H5PYWriter.H5PYAttributeManager))
            self.assertEqual(nt.is_valid, True)
            self.assertEqual(nt.parent, rt)
            self.assertEqual(nt.size, 0)
            self.assertEqual(nt.exists("strument"), False)


            self.assertTrue(
                isinstance(ins, H5PYWriter.H5PYGroup))
            self.assertEqual(ins.name, "instrument")
            self.assertEqual(
                ins.path, "/entry12345:NXentry/instrument:NXinstrument")
            self.assertEqual(
                len(ins.h5object.attrs), 1)
            attr = ins.attributes
            self.assertEqual(attr["NX_class"][...], "NXinstrument")
            self.assertTrue(
                isinstance(attr, H5PYWriter.H5PYAttributeManager))
            self.assertEqual(ins.is_valid, True)
            self.assertEqual(ins.parent, entry)
            self.assertEqual(ins.size, 4)
            self.assertEqual(ins.exists("detector"), True)
            self.assertEqual(ins.exists("floatspec"), True)
            self.assertEqual(ins.exists("intspec"), True)
            self.assertEqual(ins.exists("strspec"), True)
            self.assertEqual(ins.exists("strument"), False)

            kids = set()
            for en in ins:
                kids.add(en.name)

            self.assertEqual(kids, set(["detector", "floatspec",
                                        "intspec", "strspec"]))

            ins_op = entry.open("instrument")
            self.assertTrue(
                isinstance(ins_op, H5PYWriter.H5PYGroup))
            self.assertEqual(ins_op.name, "instrument")
            self.assertEqual(
                ins_op.path, "/entry12345:NXentry/instrument:NXinstrument")
            self.assertEqual(
                len(ins_op.h5object.attrs), 1)
            attr = ins_op.attributes
            self.assertEqual(attr["NX_class"][...], "NXinstrument")
            self.assertTrue(
                isinstance(attr, H5PYWriter.H5PYAttributeManager))
            self.assertEqual(ins_op.is_valid, True)
            self.assertEqual(ins_op.parent, entry)
            self.assertEqual(ins_op.size, 4)
            self.assertEqual(ins_op.exists("detector"), True)
            self.assertEqual(ins_op.exists("floatspec"), True)
            self.assertEqual(ins_op.exists("intspec"), True)
            self.assertEqual(ins_op.exists("strspec"), True)
            self.assertEqual(ins_op.exists("strument"), False)

            kids = set()
            for en in ins_op:
                kids.add(en.name)

            self.assertEqual(kids, set(["detector", "floatspec",
                                        "intspec", "strspec"]))

            self.assertTrue(
                isinstance(det, H5PYWriter.H5PYGroup))
            self.assertEqual(det.name, "detector")
            self.assertEqual(
                det.path,
                "/entry12345:NXentry/instrument:NXinstrument/"
                "detector:NXdetector")
            self.assertEqual(
                len(det.h5object.attrs), 1)
            attr = det.attributes
            self.assertEqual(attr["NX_class"][...], "NXdetector")
            self.assertTrue(
                isinstance(attr, H5PYWriter.H5PYAttributeManager))
            self.assertEqual(det.is_valid, True)
            self.assertEqual(det.parent, ins)
            self.assertEqual(det.size, 6)
            self.assertEqual(det.exists("strimage"), True)
            self.assertEqual(det.exists("intvec"), True)
            self.assertEqual(det.exists("floatimage"), True)
            self.assertEqual(det.exists("floatvec"), True)
            self.assertEqual(det.exists("intimage"), True)
            self.assertEqual(det.exists("strvec"), True)
            self.assertEqual(det.exists("strument"), False)

            kids = set()
            for en in det:
                kids.add(en.name)
            print kids

            self.assertEqual(
                kids,
                set(['strimage', 'intvec', 'floatimage',
                     'floatvec', 'intimage', 'strvec']))



            self.assertTrue(isinstance(strscalar, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(strscalar.h5object, h5py.Dataset))
            self.assertEqual(strscalar.name, 'strscalar')
            self.assertEqual(strscalar.path, '/entry12345:NXentry/strscalar')
            self.assertEqual(strscalar.dtype, 'string')
            self.assertEqual(strscalar.shape, (1,))

            self.assertTrue(isinstance(floatscalar, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(floatscalar.h5object, h5py.Dataset))
            self.assertEqual(floatscalar.name, 'floatscalar')
            self.assertEqual(floatscalar.path, '/entry12345:NXentry/floatscalar')
            self.assertEqual(floatscalar.dtype, 'float64')
            self.assertEqual(floatscalar.shape, (1,))

            self.assertTrue(isinstance(intscalar, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(intscalar.h5object, h5py.Dataset))
            self.assertEqual(intscalar.name, 'intscalar')
            self.assertEqual(intscalar.path, '/entry12345:NXentry/intscalar')
            self.assertEqual(intscalar.dtype, 'uint64')
            self.assertEqual(intscalar.shape, (1,))

            self.assertTrue(isinstance(strspec, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(strspec.h5object, h5py.Dataset))
            self.assertEqual(strspec.name, 'strspec')
            self.assertEqual(strspec.path, '/entry12345:NXentry/instrument:NXinstrument/strspec')
            self.assertEqual(strspec.dtype, 'string')
            self.assertEqual(strspec.shape, (10,))

            self.assertTrue(isinstance(floatspec, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(floatspec.h5object, h5py.Dataset))
            self.assertEqual(floatspec.name, 'floatspec')
            self.assertEqual(floatspec.path, '/entry12345:NXentry/instrument:NXinstrument/floatspec')
            self.assertEqual(floatspec.dtype, 'float32')
            self.assertEqual(floatspec.shape, (20,))

            self.assertTrue(isinstance(intspec, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(intspec.h5object, h5py.Dataset))
            self.assertEqual(intspec.name, 'intspec')
            self.assertEqual(intspec.path, '/entry12345:NXentry/instrument:NXinstrument/intspec')
            self.assertEqual(intspec.dtype, 'int64')
            self.assertEqual(intspec.shape, (30,))


            self.assertTrue(isinstance(strimage, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(strimage.h5object, h5py.Dataset))
            self.assertEqual(strimage.name, 'strimage')
            self.assertEqual(strimage.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/strimage')
            self.assertEqual(strimage.dtype, 'string')
            self.assertEqual(strimage.shape, (2, 2))

            self.assertTrue(isinstance(floatimage, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(floatimage.h5object, h5py.Dataset))
            self.assertEqual(floatimage.name, 'floatimage')
            self.assertEqual(floatimage.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/floatimage')
            self.assertEqual(floatimage.dtype, 'float64')
            self.assertEqual(floatimage.shape, (20, 10))

            self.assertTrue(isinstance(intimage, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(intimage.h5object, h5py.Dataset))
            self.assertEqual(intimage.name, 'intimage')
            self.assertEqual(intimage.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/intimage')
            self.assertEqual(intimage.dtype, 'uint32')
            self.assertEqual(intimage.shape, (0, 30))





            self.assertTrue(isinstance(strvec, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(strvec.h5object, h5py.Dataset))
            self.assertEqual(strvec.name, 'strvec')
            self.assertEqual(strvec.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/strvec')
            self.assertEqual(strvec.dtype, 'string')
            self.assertEqual(strvec.shape, (0, 2, 2))

            self.assertTrue(isinstance(floatvec, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(floatvec.h5object, h5py.Dataset))
            self.assertEqual(floatvec.name, 'floatvec')
            self.assertEqual(floatvec.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/floatvec')
            self.assertEqual(floatvec.dtype, 'float64')
            self.assertEqual(floatvec.shape, (1, 20, 10))

            self.assertTrue(isinstance(intvec, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(intvec.h5object, h5py.Dataset))
            self.assertEqual(intvec.name, 'intvec')
            self.assertEqual(intvec.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/intvec')
            self.assertEqual(intvec.dtype, 'uint32')
            self.assertEqual(intvec.shape, (0, 2, 30))


            strscalar_op= entry.open("strscalar")
            floatscalar_op = entry.open("floatscalar")
            intscalar_op = entry.open("intscalar")
            strspec_op = ins.open("strspec")
            floatspec_op = ins.open("floatspec")
            intspec_op = ins.open("intspec")
            strimage_op = det.open("strimage")
            floatimage_op = det.open("floatimage")
            intimage_op = det.open("intimage")
            strvec_op = det.open("strvec")
            floatvec_op = det.open("floatvec")
            intvec_op = det.open("intvec")


            self.assertTrue(isinstance(strscalar_op, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(strscalar_op.h5object, h5py.Dataset))
            self.assertEqual(strscalar_op.name, 'strscalar')
            self.assertEqual(strscalar_op.path, '/entry12345:NXentry/strscalar')
            self.assertEqual(strscalar_op.dtype, 'string')
            self.assertEqual(strscalar_op.shape, (1,))

            self.assertTrue(isinstance(floatscalar_op, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(floatscalar_op.h5object, h5py.Dataset))
            self.assertEqual(floatscalar_op.name, 'floatscalar')
            self.assertEqual(floatscalar_op.path, '/entry12345:NXentry/floatscalar')
            self.assertEqual(floatscalar_op.dtype, 'float64')
            self.assertEqual(floatscalar_op.shape, (1,))

            self.assertTrue(isinstance(intscalar_op, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(intscalar_op.h5object, h5py.Dataset))
            self.assertEqual(intscalar_op.name, 'intscalar')
            self.assertEqual(intscalar_op.path, '/entry12345:NXentry/intscalar')
            self.assertEqual(intscalar_op.dtype, 'uint64')
            self.assertEqual(intscalar_op.shape, (1,))

            self.assertTrue(isinstance(strspec_op, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(strspec_op.h5object, h5py.Dataset))
            self.assertEqual(strspec_op.name, 'strspec')
            self.assertEqual(strspec_op.path, '/entry12345:NXentry/instrument:NXinstrument/strspec')
            self.assertEqual(strspec_op.dtype, 'string')
            self.assertEqual(strspec_op.shape, (10,))

            self.assertTrue(isinstance(floatspec_op, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(floatspec_op.h5object, h5py.Dataset))
            self.assertEqual(floatspec_op.name, 'floatspec')
            self.assertEqual(floatspec_op.path, '/entry12345:NXentry/instrument:NXinstrument/floatspec')
            self.assertEqual(floatspec_op.dtype, 'float32')
            self.assertEqual(floatspec_op.shape, (20,))

            self.assertTrue(isinstance(intspec_op, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(intspec_op.h5object, h5py.Dataset))
            self.assertEqual(intspec_op.name, 'intspec')
            self.assertEqual(intspec_op.path, '/entry12345:NXentry/instrument:NXinstrument/intspec')
            self.assertEqual(intspec_op.dtype, 'int64')
            self.assertEqual(intspec_op.shape, (30,))


            self.assertTrue(isinstance(strimage_op, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(strimage_op.h5object, h5py.Dataset))
            self.assertEqual(strimage_op.name, 'strimage')
            self.assertEqual(strimage_op.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/strimage')
            self.assertEqual(strimage_op.dtype, 'string')
            self.assertEqual(strimage_op.shape, (2, 2))

            self.assertTrue(isinstance(floatimage_op, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(floatimage_op.h5object, h5py.Dataset))
            self.assertEqual(floatimage_op.name, 'floatimage')
            self.assertEqual(floatimage_op.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/floatimage')
            self.assertEqual(floatimage_op.dtype, 'float64')
            self.assertEqual(floatimage_op.shape, (20, 10))

            self.assertTrue(isinstance(intimage_op, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(intimage_op.h5object, h5py.Dataset))
            self.assertEqual(intimage_op.name, 'intimage')
            self.assertEqual(intimage_op.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/intimage')
            self.assertEqual(intimage_op.dtype, 'uint32')
            self.assertEqual(intimage_op.shape, (0, 30))



            self.assertTrue(isinstance(strvec_op, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(strvec_op.h5object, h5py.Dataset))
            self.assertEqual(strvec_op.name, 'strvec')
            self.assertEqual(strvec_op.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/strvec')
            self.assertEqual(strvec_op.dtype, 'string')
            self.assertEqual(strvec_op.shape, (0, 2, 2))

            self.assertTrue(isinstance(floatvec_op, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(floatvec_op.h5object, h5py.Dataset))
            self.assertEqual(floatvec_op.name, 'floatvec')
            self.assertEqual(floatvec_op.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/floatvec')
            self.assertEqual(floatvec_op.dtype, 'float64')
            self.assertEqual(floatvec_op.shape, (1, 20, 10))

            self.assertTrue(isinstance(intvec_op, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(intvec_op.h5object, h5py.Dataset))
            self.assertEqual(intvec_op.name, 'intvec')
            self.assertEqual(intvec_op.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/intvec')
            self.assertEqual(intvec_op.dtype, 'uint32')
            self.assertEqual(intvec_op.shape, (0, 2, 30))
            self.assertEqual(intvec_op.parent, det)



            self.assertTrue(isinstance(lkintimage, H5PYWriter.H5PYLink))
            self.assertTrue(isinstance(lkintimage.h5object, h5py.SoftLink))
            self.assertTrue(lkintimage.target_path.endswith(
                "%s://entry12345/instrument/detector/intimage" % self._fname))
            self.assertEqual(
                lkintimage.path,
                "/entry12345:NXentry/data:NXdata/lkintimage")

            self.assertTrue(isinstance(lkfloatvec, H5PYWriter.H5PYLink))
            self.assertTrue(isinstance(lkfloatvec.h5object, h5py.SoftLink))
            self.assertTrue(lkfloatvec.target_path.endswith(
                "%s://entry12345/instrument/detector/floatvec" % self._fname))
            self.assertEqual(
                lkfloatvec.path,
                "/entry12345:NXentry/data:NXdata/lkfloatvec")

            self.assertTrue(isinstance(lkintspec, H5PYWriter.H5PYLink))
            self.assertTrue(isinstance(lkintspec.h5object, h5py.SoftLink))
            self.assertTrue(lkintspec.target_path.endswith(
                "%s://entry12345/instrument/intspec" % self._fname))
            self.assertEqual(
                lkintspec.path,
                "/entry12345:NXentry/data:NXdata/lkintspec")

            self.assertTrue(isinstance(lkdet, H5PYWriter.H5PYLink))
            self.assertTrue(isinstance(lkdet.h5object, h5py.SoftLink))
            self.assertTrue(lkdet.target_path.endswith(
                "%s://entry12345/instrument/detector" % self._fname))
            self.assertEqual(
                lkdet.path,
                "/entry12345:NXentry/data:NXdata/lkdet")

            self.assertTrue(isinstance(lkno, H5PYWriter.H5PYLink))
            self.assertTrue(isinstance(lkno.h5object, h5py.SoftLink))
            self.assertTrue(lkno.target_path.endswith(
                "%s://notype/unknown" % self._fname))
            self.assertEqual(
                lkno.path,
                "/entry12345:NXentry/data:NXdata/lkno")



            lkintimage_op = dt.open("lkintimage")
            lkfloatvec_op = dt.open("lkfloatvec")
            lkintspec_op = dt.open("lkintspec")
            lkdet_op = dt.open("lkdet")
            lkno_op = dt.open("lkno")



            self.assertTrue(isinstance(lkintimage_op, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(lkintimage_op.h5object, h5py.Dataset))
            self.assertEqual(lkintimage_op.name, 'lkintimage')
            self.assertEqual(
                lkintimage_op.path,
                '/entry12345:NXentry/data:NXdata/lkintimage')
            self.assertEqual(lkintimage_op.dtype, 'uint32')
            self.assertEqual(lkintimage_op.shape, (0, 30))


            self.assertTrue(isinstance(lkfloatvec_op, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(lkfloatvec_op.h5object, h5py.Dataset))
            self.assertEqual(lkfloatvec_op.name, 'lkfloatvec')
            self.assertEqual(lkfloatvec_op.path,
                             '/entry12345:NXentry/data:NXdata/lkfloatvec')
            self.assertEqual(lkfloatvec_op.dtype, 'float64')
            self.assertEqual(lkfloatvec_op.shape, (1, 20, 10))


            self.assertTrue(
                isinstance(lkintspec_op, H5PYWriter.H5PYField))
            self.assertTrue(
                isinstance(lkintspec_op.h5object, h5py.Dataset))
            self.assertEqual(lkintspec_op.name, 'lkintspec')
            self.assertEqual(lkintspec_op.path,
                             '/entry12345:NXentry/data:NXdata/lkintspec')
            self.assertEqual(lkintspec_op.dtype, 'int64')
            self.assertEqual(lkintspec_op.shape, (30,))

            self.assertTrue(isinstance(lkno_op, H5PYWriter.H5PYLink))
            self.assertTrue(isinstance(lkno_op.h5object, h5py.SoftLink))
            self.assertTrue(lkno_op.target_path.endswith(
                "%s://notype/unknown" % self._fname))
            self.assertEqual(
                lkno_op.path,
                "/entry12345:NXentry/data:NXdata/lkno")


            entry.close()
            self.assertEqual(rt.is_valid, True)
            self.assertEqual(entry.is_valid, False)
            self.assertEqual(dt.is_valid, False)


            entry.reopen()
            self.assertEqual(rt.is_valid, True)
            self.assertEqual(entry.is_valid, True)
            self.assertEqual(dt.is_valid, True)

            fl.reopen()
            self.assertEqual(fl.name, self._fname)
            self.assertEqual(fl.path, None)
            self.assertTrue(
                isinstance(fl.h5object, h5py.File))
            self.assertEqual(fl.parent, None)
            self.assertEqual(fl.readonly, False)

            fl.close()

            fl.reopen(True)
            self.assertEqual(fl.name, self._fname)
            self.assertEqual(fl.path, None)
            self.assertTrue(
                isinstance(fl.h5object, h5py.File))
            self.assertEqual(fl.parent, None)
            self.assertEqual(fl.readonly, True)

            fl.close()

            self.myAssertRaise(
                Exception, fl.reopen, True, True)
            self.myAssertRaise(
                Exception, fl.reopen, False, True)


            fl = H5PYWriter.open_file(self._fname, readonly=True)
            f = fl.root()
            self.assertEqual(6, len(f.attributes))
            atts = []
            for at in f.attributes:
                print at.name, at.read(), at.dtype
            self.assertEqual(
                f.attributes["file_name"][...],
                self._fname)
            self.assertTrue(
                f.attributes["NX_class"][...], "NXroot")
            self.assertEqual(f.size, 2)
            fl.close()

        finally:
            os.remove(self._fname)

if __name__ == '__main__':
    unittest.main()
