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
        
    ## float list tester
    def myAssertFloatList(self, list1, list2, error=0.0):
        
        self.assertEqual(len(list1), len(list2))
        for i, el in enumerate(list1):
            if abs(el-list2[i]) >= error:
                print "EL", el, list2[i], error
            self.assertTrue(abs(el-list2[i]) < error)
            
    ## float image tester
    def myAssertImage(self, image1, image2, error=None):
        
        self.assertEqual(len(image1), len(image2))
        for i in range(len(image1)):
            self.assertEqual(len(image1[i]), len(image2[i]))
            for j in range(len(image1[i])):
                if error is not None:
                    if abs(image1[i][j]-image2[i][j]) >= error:
                        print "EL", image1[i][j], image2[i][j], error
                    self.assertTrue(abs(image1[i][j]-image2[i][j]) < error)
                else:
                    self.assertEqual(image1[i][j], image2[i][j])

    ## float image tester
    def myAssertVector(self, image1, image2, error=None):
        
        self.assertEqual(len(image1), len(image2))
        for i in range(len(image1)):
            self.assertEqual(len(image1[i]), len(image2[i]))
            for j in range(len(image1[i])):
                self.assertEqual(len(image1[i][j]), len(image2[i][j]))
                for k in range(len(image1[i][j])):
                    if error is not None:
                        if abs(image1[i][j][k]-image2[i][j][k]) >= error:
                            print "EL", image1[i][j][k], image2[i][j][k], error
                        self.assertTrue(abs(image1[i][j][k]-image2[i][j][k]) < error)
                    else:
                        self.assertEqual(image1[i][j][k], image2[i][j][k])
            

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

    ## default createfile test
    # \brief It tests default settings
    def test_h5pyfield_scalar(self):
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



            self.assertTrue(isinstance(strscalar, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(strscalar.h5object, h5py.Dataset))
            self.assertEqual(strscalar.name, 'strscalar')
            self.assertEqual(strscalar.h5object.name, '/entry12345/strscalar')
            self.assertEqual(strscalar.path, '/entry12345:NXentry/strscalar')
            self.assertEqual(strscalar.dtype, 'string')
            self.assertEqual(strscalar.h5object.dtype.name, 'object')
            self.assertEqual(strscalar.shape, (1,))
            self.assertEqual(strscalar.h5object.shape, (1,))
            self.assertEqual(strscalar.is_valid, True)
            self.assertEqual(strscalar.shape, (1,))
            self.assertEqual(strscalar.h5object.shape, (1,))

            vl = ["1234", "Somethin to test 1234", "2342;23ml243",
                  "sd", "q234", "12 123 ", "aqds ", "Aasdas"]
            strscalar[...] = vl[0]
            self.assertEqual(strscalar.read(), vl[0])
            strscalar.write(vl[1])
            self.assertEqual(strscalar[0], vl[1])
            strscalar[0] = vl[2]
            self.assertEqual(strscalar[...], vl[2])
            strscalar[0] = vl[0]

            strscalar.grow()
            self.assertEqual(strscalar.shape, (2,))
            self.assertEqual(strscalar.h5object.shape, (2,))

            self.assertEqual(strscalar[0], vl[0])
            strscalar[1] =  vl[3]
            self.assertEqual(list(strscalar[...]), [vl[0], vl[3]])            

            strscalar.grow(ext=2)
            self.assertEqual(strscalar.shape, (4,))
            self.assertEqual(strscalar.h5object.shape, (4,))
            strscalar[1:4] =  vl[1:4]
            self.assertEqual(list(strscalar.read()), vl[0:4])            
            self.assertEqual(list(strscalar[0:2]), vl[0:2])            

            strscalar.grow(0, 3)
            self.assertEqual(strscalar.shape, (7,))
            self.assertEqual(strscalar.h5object.shape, (7,))
            strscalar.write(vl[0:7])
            self.assertEqual(list(strscalar.read()), vl[0:7])            
            self.assertEqual(list(strscalar[...]), vl[0:7])            

            attrs = strscalar.attributes
            self.assertTrue(isinstance(attrs, H5PYWriter.H5PYAttributeManager))
            print type(attrs.h5object)
            self.assertTrue(isinstance(attrs.h5object, h5py._hl.attrs.AttributeManager))
            self.assertEqual(attrs.parent, strscalar)
            self.assertEqual(len(attrs), 0)            
            
            
            
            self.assertTrue(isinstance(floatscalar, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(floatscalar.h5object, h5py.Dataset))
            self.assertEqual(floatscalar.name, 'floatscalar')
            self.assertEqual(floatscalar.h5object.name, '/entry12345/floatscalar')
            self.assertEqual(floatscalar.path, '/entry12345:NXentry/floatscalar')
            self.assertEqual(floatscalar.dtype, 'float64')
            self.assertEqual(floatscalar.h5object.dtype, 'float64')
            self.assertEqual(floatscalar.shape, (1,))
            self.assertEqual(floatscalar.h5object.shape, (1,))

            vl  = [1123.34, 3234.3 , 234.33, -4.4,34, 0.0, 4.3, 434.5, 23.0,0]

            floatscalar[...] = vl[0]
            self.assertEqual(floatscalar.read(), vl[0])
            floatscalar.write(vl[1])
            self.assertEqual(floatscalar[0], vl[1])
            floatscalar[0] = vl[2]
            self.assertEqual(floatscalar[...], vl[2])
            floatscalar[0] = vl[0]

            floatscalar.grow()
            self.assertEqual(floatscalar.shape, (2,))
            self.assertEqual(floatscalar.h5object.shape, (2,))

            self.assertEqual(floatscalar[0], vl[0])
            floatscalar[1] =  vl[3]
            self.assertEqual(list(floatscalar[...]), [vl[0], vl[3]])            

            floatscalar.grow(ext=2)
            self.assertEqual(floatscalar.shape, (4,))
            self.assertEqual(floatscalar.h5object.shape, (4,))
            floatscalar[1:4] =  vl[1:4]
            self.assertEqual(list(floatscalar.read()), vl[0:4])            
            self.assertEqual(list(floatscalar[0:2]), vl[0:2])            

            floatscalar.grow(0, 3)
            self.assertEqual(floatscalar.shape, (7,))
            self.assertEqual(floatscalar.h5object.shape, (7,))
            floatscalar.write(vl[0:7])
            self.assertEqual(list(floatscalar.read()), vl[0:7])            
            self.assertEqual(list(floatscalar[...]), vl[0:7])            

            attrs = floatscalar.attributes
            self.assertTrue(isinstance(attrs, H5PYWriter.H5PYAttributeManager))
            self.assertTrue(isinstance(attrs.h5object, h5py._hl.attrs.AttributeManager))
            self.assertEqual(attrs.parent, floatscalar)
            self.assertEqual(len(attrs), 0)            
            

            
            self.assertTrue(isinstance(intscalar, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(intscalar.h5object, h5py.Dataset))
            self.assertEqual(intscalar.name, 'intscalar')
            self.assertEqual(intscalar.h5object.name, '/entry12345/intscalar')
            self.assertEqual(intscalar.path, '/entry12345:NXentry/intscalar')
            self.assertEqual(intscalar.dtype, 'uint64')
            self.assertEqual(intscalar.h5object.dtype, 'uint64')
            self.assertEqual(intscalar.shape, (1,))
            self.assertEqual(intscalar.h5object.shape, (1,))



            vl  = [243 ,43 ,45, 34, 45 ,54, 23234]

            intscalar[...] = vl[0]
            self.assertEqual(intscalar.read(), vl[0])
            intscalar.write(vl[1])
            self.assertEqual(intscalar[0], vl[1])
            intscalar[0] = vl[2]
            self.assertEqual(intscalar[...], vl[2])
            intscalar[0] = vl[0]

            intscalar.grow()
            self.assertEqual(intscalar.shape, (2,))
            self.assertEqual(intscalar.h5object.shape, (2,))

            self.assertEqual(intscalar[0], vl[0])
            intscalar[1] =  vl[3]
            self.assertEqual(list(intscalar[...]), [vl[0], vl[3]])            

            intscalar.grow(ext=2)
            self.assertEqual(intscalar.shape, (4,))
            self.assertEqual(intscalar.h5object.shape, (4,))
            intscalar[1:4] =  vl[1:4]
            self.assertEqual(list(intscalar.read()), vl[0:4])            
            self.assertEqual(list(intscalar[0:2]), vl[0:2])            

            intscalar.grow(0, 3)
            self.assertEqual(intscalar.shape, (7,))
            self.assertEqual(intscalar.h5object.shape, (7,))
            intscalar.write(vl[0:7])
            self.assertEqual(list(intscalar.read()), vl[0:7])            
            self.assertEqual(list(intscalar[...]), vl[0:7])            

            attrs = intscalar.attributes
            self.assertTrue(isinstance(attrs, H5PYWriter.H5PYAttributeManager))
            self.assertTrue(isinstance(attrs.h5object, h5py._hl.attrs.AttributeManager))
            self.assertEqual(attrs.parent, intscalar)
            self.assertEqual(len(attrs), 0)
            
            intscalar.close()
            self.assertEqual(rt.is_valid, True)
            self.assertEqual(entry.is_valid, True)
            self.assertEqual(det.is_valid, True)
            self.assertEqual(intscalar.is_valid, False)
            self.assertEqual(attrs.is_valid, False)


            entry.reopen()
            self.assertEqual(rt.is_valid, True)
            self.assertEqual(entry.is_valid, True)
            self.assertEqual(dt.is_valid, True)
            self.assertEqual(det.is_valid, True)
            self.assertEqual(intscalar.is_valid, True)
            self.assertEqual(attrs.is_valid, True)
            
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


    ## default createfile test
    # \brief It tests default settings
    def test_h5pyfield_spectrum(self):
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

            
            self.assertTrue(isinstance(strspec, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(strspec.h5object, h5py.Dataset))
            self.assertEqual(strspec.name, 'strspec')
            self.assertEqual(strspec.h5object.name, '/entry12345/instrument/strspec')
            self.assertEqual(strspec.path, '/entry12345:NXentry/instrument:NXinstrument/strspec')
            self.assertEqual(strspec.dtype, 'string')
            self.assertEqual(strspec.h5object.dtype.name, 'object')
            self.assertEqual(strspec.shape, (10,))
            self.assertEqual(strspec.h5object.shape, (10,))

            chars = string.ascii_uppercase + string.digits
            vl = [
                ''.join(self.__rnd.choice(chars)
                        for _ in range(self.__rnd.randint(1, 10))) for _ in range(40)]
            

            strspec[...] = vl[0:10]
            self.assertEqual(list(strspec.read()), vl[0:10])
            strspec.write(vl[11:21])
            self.assertEqual(list(strspec[...]), vl[11:21])
            strspec[...] = vl[0:10]

            strspec.grow()
            self.assertEqual(strspec.shape, (11,))
            self.assertEqual(strspec.h5object.shape, (11,))

            self.assertEqual(list(strspec[0:10]), vl[0:10])
            strspec[10] =  vl[10]
            self.assertEqual(list(strspec[...]), vl[0:11])            

            strspec.grow(ext=2)
            self.assertEqual(strspec.shape, (13,))
            self.assertEqual(strspec.h5object.shape, (13,))
            strspec[1:13] =  vl[1:13]
            self.assertEqual(list(strspec.read()), vl[0:13])            
            self.assertEqual(list(strspec[0:2]), vl[0:2])            

            strspec.grow(0, 3)
            self.assertEqual(strspec.shape, (16,))
            self.assertEqual(strspec.h5object.shape, (16,))
            strspec.write(vl[0:16])
            self.assertEqual(list(strspec.read()), vl[0:16])            
            self.assertEqual(list(strspec[...]), vl[0:16])            

            attrs = strspec.attributes
            self.assertTrue(isinstance(attrs, H5PYWriter.H5PYAttributeManager))
            self.assertTrue(isinstance(attrs.h5object, h5py._hl.attrs.AttributeManager))
            self.assertEqual(attrs.parent, strspec)
            self.assertEqual(len(attrs), 0)            


            
            self.assertTrue(isinstance(floatspec, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(floatspec.h5object, h5py.Dataset))
            self.assertEqual(floatspec.name, 'floatspec')
            self.assertEqual(floatspec.h5object.name, '/entry12345/instrument/floatspec')
            self.assertEqual(floatspec.path, '/entry12345:NXentry/instrument:NXinstrument/floatspec')
            self.assertEqual(floatspec.dtype, 'float32')
            self.assertEqual(floatspec.h5object.dtype, 'float32')
            self.assertEqual(floatspec.shape, (20,))
            self.assertEqual(floatspec.h5object.shape, (20,))


            vl = [self.__rnd.uniform(-200.0, 200) for _ in range(80)]

            floatspec[...] = vl[0:20]
            self.myAssertFloatList(list(floatspec.read()), vl[0:20], 1e-4)
            floatspec.write(vl[21:41])
            self.myAssertFloatList(list(floatspec[...]), vl[21:41], 1e-4)
            floatspec[...] = vl[0:20]

            floatspec.grow()
            self.assertEqual(floatspec.shape, (21,))
            self.assertEqual(floatspec.h5object.shape, (21,))

            self.myAssertFloatList(list(floatspec[0:20]), vl[0:20], 1e-4)
            floatspec[20] =  vl[20]
            self.myAssertFloatList(list(floatspec[...]), vl[0:21], 1e-4)            

            floatspec.grow(ext=2)
            self.assertEqual(floatspec.shape, (23,))
            self.assertEqual(floatspec.h5object.shape, (23,))
            floatspec[1:23] =  vl[1:23]
            self.myAssertFloatList(list(floatspec.read()), vl[0:23], 1e-4)            
            self.myAssertFloatList(list(floatspec[0:2]), vl[0:2], 1e-4)            

            floatspec.grow(0, 3)
            self.assertEqual(floatspec.shape, (26,))
            self.assertEqual(floatspec.h5object.shape, (26,))
            floatspec.write(vl[0:26])
            self.myAssertFloatList(list(floatspec.read()), vl[0:26], 1e-4)            
            self.myAssertFloatList(list(floatspec[...]), vl[0:26], 1e-4)            

            attrs = floatspec.attributes
            self.assertTrue(isinstance(attrs, H5PYWriter.H5PYAttributeManager))
            self.assertTrue(isinstance(attrs.h5object, h5py._hl.attrs.AttributeManager))
            self.assertEqual(attrs.parent, floatspec)
            self.assertEqual(len(attrs), 0)            


            
            self.assertTrue(isinstance(intspec, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(intspec.h5object, h5py.Dataset))
            self.assertEqual(intspec.name, 'intspec')
            self.assertEqual(intspec.path, '/entry12345:NXentry/instrument:NXinstrument/intspec')
            self.assertEqual(intspec.dtype, 'int64')
            self.assertEqual(intspec.shape, (30,))
            self.assertEqual(intspec.h5object.name, '/entry12345/instrument/intspec')
            self.assertEqual(intspec.h5object.dtype, 'int64')
            self.assertEqual(intspec.h5object.shape, (30,))



            vl = [self.__rnd.randint(1, 16000)  for _ in range(100)]
            

            intspec[...] = vl[0:30]
            self.assertEqual(list(intspec.read()), vl[0:30])
            intspec.write(vl[31:61])
            self.assertEqual(list(intspec[...]), vl[31:61])
            intspec[...] = vl[0:30]

            intspec.grow()
            self.assertEqual(intspec.shape, (31,))
            self.assertEqual(intspec.h5object.shape, (31,))

            self.assertEqual(list(intspec[0:10]), vl[0:10])
            intspec[30] =  vl[30]
            self.assertEqual(list(intspec[...]), vl[0:31])            

            intspec.grow(ext=2)
            self.assertEqual(intspec.shape, (33,))
            self.assertEqual(intspec.h5object.shape, (33,))
            intspec[1:33] =  vl[1:33]
            self.assertEqual(list(intspec.read()), vl[0:33])            
            self.assertEqual(list(intspec[0:2]), vl[0:2])            

            intspec.grow(0, 3)
            self.assertEqual(intspec.shape, (36,))
            self.assertEqual(intspec.h5object.shape, (36,))
            intspec.write(vl[0:36])
            self.assertEqual(list(intspec.read()), vl[0:36])            
            self.assertEqual(list(intspec[...]), vl[0:36])            

            attrs = intspec.attributes
            self.assertTrue(isinstance(attrs, H5PYWriter.H5PYAttributeManager))
            self.assertTrue(isinstance(attrs.h5object, h5py._hl.attrs.AttributeManager))
            self.assertEqual(attrs.parent, intspec)
            self.assertEqual(len(attrs), 0)            


            
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


    ## default createfile test
    # \brief It tests default settings
    def test_h5pyfield_image(self):
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

            self.assertTrue(isinstance(strimage, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(strimage.h5object, h5py.Dataset))
            self.assertEqual(strimage.name, 'strimage')
            self.assertEqual(strimage.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/strimage')
            self.assertEqual(strimage.dtype, 'string')
            self.assertEqual(strimage.shape, (2, 2))
            self.assertEqual(strimage.h5object.name, '/entry12345/instrument/detector/strimage')
            self.assertEqual(strimage.h5object.dtype.name, 'object')
            self.assertEqual(strimage.h5object.shape, (2, 2))


            chars = string.ascii_uppercase + string.digits
            vl = [
                [''.join(self.__rnd.choice(chars)
                         for _ in range(self.__rnd.randint(1, 10)))
                 for _ in range(10)]
                for _ in range(30)]
            

            vv = [[vl[j][i] for i in range(2)] for j in range(2)]
            strimage[...] = vv
            self.myAssertImage(strimage.read(), vv)
            vv2 = [[vl[j+2][i+2] for i in range(2)] for j in range(2)]
            strimage.write(vv2)
            self.myAssertImage(list(strimage[...]), vv2)
            strimage[...] = vv

            strimage.grow()
            self.assertEqual(strimage.shape, (3,2))
            self.assertEqual(strimage.h5object.shape, (3,2))

            iv = [[strimage[j,i] for i in range(2)] for j in range(2)]
            self.myAssertImage(iv, vv)
            strimage[2,:] = [vl[2][0], vl[2][1]]
            vv3 = [[vl[j][i] for i in range(2)] for j in range(3)]
            self.myAssertImage(strimage[...], vv3)

            strimage.grow(ext=2)
            self.assertEqual(strimage.shape, (5,2))
            self.assertEqual(strimage.h5object.shape, (5,2))
            vv4 = [[vl[j+2][i] for i in range(2)] for j in range(3)]
            vv5 = [[vl[j][i] for i in range(2)] for j in range(5)]
            strimage[2:5,:] =  vv4
            self.myAssertImage(strimage[...], vv5)
            self.myAssertImage(strimage[0:3,:], vv3)

            strimage.grow(1, 4)
            self.assertEqual(strimage.shape, (5,6))
            self.assertEqual(strimage.h5object.shape, (5,6))

            vv6 = [[vl[j][i] for i in range(6)] for j in range(5)]
            strimage.write(vv6)
            self.myAssertImage(strimage[...], vv6)
            self.myAssertImage(strimage.read(), vv6)

            attrs = strimage.attributes
            self.assertTrue(isinstance(attrs, H5PYWriter.H5PYAttributeManager))
            self.assertTrue(isinstance(attrs.h5object, h5py._hl.attrs.AttributeManager))
            self.assertEqual(attrs.parent, strimage)
            self.assertEqual(len(attrs), 0)            

            

            self.assertTrue(isinstance(floatimage, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(floatimage.h5object, h5py.Dataset))
            self.assertEqual(floatimage.name, 'floatimage')
            self.assertEqual(floatimage.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/floatimage')
            self.assertEqual(floatimage.dtype, 'float64')
            self.assertEqual(floatimage.shape, (20, 10))
            self.assertEqual(floatimage.h5object.name, '/entry12345/instrument/detector/floatimage')
            self.assertEqual(floatimage.h5object.dtype, 'float64')
            self.assertEqual(floatimage.h5object.shape, (20, 10))


            vl = [
                [self.__rnd.uniform(-20000.0, 20000) for _ in range(50)]
                for _ in range(50)]
            

            vv = [[vl[j][i] for i in range(10)] for j in range(20)]
            floatimage[...] = vv
            self.myAssertImage(floatimage.read(), vv)
            vv2 = [[vl[j+20][i+10] for i in range(10)] for j in range(20)]
            floatimage.write(vv2)
            self.myAssertImage(list(floatimage[...]), vv2)
            floatimage[...] = vv

            floatimage.grow()
            self.assertEqual(floatimage.shape, (21,10))
            self.assertEqual(floatimage.h5object.shape, (21,10))

            iv = [[floatimage[j,i] for i in range(10)] for j in range(20)]
            self.myAssertImage(iv, vv)
            floatimage[20,:] = [vl[20][i] for i in range(10)]
            vv3 = [[vl[j][i] for i in range(10)] for j in range(21)]
            self.myAssertImage(floatimage[...], vv3)

            floatimage.grow(ext=2)
            self.assertEqual(floatimage.shape, (23,10))
            self.assertEqual(floatimage.h5object.shape, (23,10))
            vv4 = [[vl[j+2][i] for i in range(10)] for j in range(21)]
            vv5 = [[vl[j][i] for i in range(10)] for j in range(23)]
            floatimage[2:23,:] =  vv4
            self.myAssertImage(floatimage[...], vv5)
            self.myAssertImage(floatimage[0:21,:], vv3)

            floatimage.grow(1, 4)
            self.assertEqual(floatimage.shape, (23,14))
            self.assertEqual(floatimage.h5object.shape, (23,14))

            vv6 = [[vl[j][i] for i in range(14)] for j in range(23)]
            floatimage.write(vv6)
            self.myAssertImage(floatimage[...], vv6)
            self.myAssertImage(floatimage.read(), vv6)


            
            self.assertTrue(isinstance(intimage, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(intimage.h5object, h5py.Dataset))
            self.assertEqual(intimage.name, 'intimage')
            self.assertEqual(intimage.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/intimage')
            self.assertEqual(intimage.dtype, 'uint32')
            self.assertEqual(intimage.shape, (0, 30))
            self.assertEqual(intimage.h5object.name, '/entry12345/instrument/detector/intimage')
            self.assertEqual(intimage.h5object.dtype, 'uint32')
            self.assertEqual(intimage.h5object.shape, (0, 30))


            vl = [
                [self.__rnd.randint(1, 1600) for _ in range(80)]
                for _ in range(80)]
            
            intimage.grow(0, 20)
            vv = [[vl[j][i] for i in range(30)] for j in range(20)]
            intimage[...] = vv
            self.myAssertImage(intimage.read(), vv)
            vv2 = [[vl[j+20][i+10] for i in range(30)] for j in range(20)]
            intimage.write(vv2)
            self.myAssertImage(list(intimage[...]), vv2)
            intimage[...] = vv

            intimage.grow()
            self.assertEqual(intimage.shape, (21,30))
            self.assertEqual(intimage.h5object.shape, (21,30))

            iv = [[intimage[j,i] for i in range(30)] for j in range(20)]
            self.myAssertImage(iv, vv)
            intimage[20,:] = [vl[20][i] for i in range(30)]
            vv3 = [[vl[j][i] for i in range(30)] for j in range(21)]
            self.myAssertImage(intimage[...], vv3)

            intimage.grow(ext=2)
            self.assertEqual(intimage.shape, (23,30))
            self.assertEqual(intimage.h5object.shape, (23,30))
            vv4 = [[vl[j+2][i] for i in range(30)] for j in range(21)]
            vv5 = [[vl[j][i] for i in range(30)] for j in range(23)]
            intimage[2:23,:] =  vv4
            self.myAssertImage(intimage[...], vv5)
            self.myAssertImage(intimage[0:21,:], vv3)

            intimage.grow(1, 4)
            self.assertEqual(intimage.shape, (23,34))
            self.assertEqual(intimage.h5object.shape, (23,34))

            vv6 = [[vl[j][i] for i in range(34)] for j in range(23)]
            intimage.write(vv6)
            self.myAssertImage(intimage[...], vv6)
            self.myAssertImage(intimage.read(), vv6)


            
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



    ## default createfile test
    # \brief It tests default settings
    def test_h5pyfield_vec(self):
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


            self.assertTrue(isinstance(strvec, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(strvec.h5object, h5py.Dataset))
            self.assertEqual(strvec.name, 'strvec')
            self.assertEqual(strvec.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/strvec')
            self.assertEqual(strvec.dtype, 'string')
            self.assertEqual(strvec.shape, (0, 2, 2))
            self.assertEqual(strvec.h5object.name, '/entry12345/instrument/detector/strvec')
            self.assertEqual(strvec.h5object.dtype.name, 'object')
            self.assertEqual(strvec.h5object.shape, (0, 2, 2))

            chars = string.ascii_uppercase + string.digits
            vl = [[[''.join(self.__rnd.choice(chars)
                            for _ in range(self.__rnd.randint(1, 10)))
                    for _ in range(10)]
                   for _ in range(20)]
                  for _ in range(30)]
            
            strvec.grow(ext=3)
            vv = [[[vl[k][j][i] for i in range(2)] for j in range(2)] for k in range(3)]
            strvec[...] = vv
            self.myAssertVector(strvec.read(), vv)
            vv2 = [[[vl[k][j+2][i+2] for i in range(2)] for j in range(2)] for k in range(3)]
            strvec.write(vv2)
            self.myAssertVector(list(strvec[...]), vv2)
            strvec[...] = vv

            strvec.grow()
            self.assertEqual(strvec.shape, (4,2,2))
            self.assertEqual(strvec.h5object.shape, (4,2,2))

            iv = [[[strvec[k,j,i] for i in range(2)] for j in range(2)] for k in range(3)]
            self.myAssertVector(iv, vv)
            strvec[3,:,:] = [[vl[3][j][i] for i in range(2)] for j in range(2)]
            vv3 = [[[vl[k][j][i] for i in range(2)] for j in range(2)] for k in range(4)]
            self.myAssertVector(strvec[...], vv3)

            strvec.grow(2, 3)
            self.assertEqual(strvec.shape, (4,2,5))
            self.assertEqual(strvec.h5object.shape, (4,2,5))
            vv4 = [[[vl[k][j][i+2] for i in range(3)] for j in range(2)] for k in range(4)]
            vv5 = [[[vl[k][j][i] for i in range(5)] for j in range(2)] for k in range(4)]
            
            strvec[:,:,2:5] =  vv4
            self.myAssertVector(strvec[...], vv5)
            self.myAssertVector(strvec[:,:,0:2], vv3)

            strvec.grow(1, 4)
            self.assertEqual(strvec.shape, (4,6,5))
            self.assertEqual(strvec.h5object.shape, (4,6,5))

            vv6 = [[[vl[k][j][i] for i in range(5)] for j in range(6)] for k in range(4)]
            strvec.write(vv6)
            self.myAssertVector(strvec[...], vv6)
            self.myAssertVector(strvec.read(), vv6)

            attrs = strvec.attributes
            self.assertTrue(isinstance(attrs, H5PYWriter.H5PYAttributeManager))
            self.assertTrue(isinstance(attrs.h5object, h5py._hl.attrs.AttributeManager))
            self.assertEqual(attrs.parent, strvec)
            self.assertEqual(len(attrs), 0)            

            
            self.assertTrue(isinstance(floatvec, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(floatvec.h5object, h5py.Dataset))
            self.assertEqual(floatvec.name, 'floatvec')
            self.assertEqual(floatvec.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/floatvec')
            self.assertEqual(floatvec.dtype, 'float64')
            self.assertEqual(floatvec.shape, (1, 20, 10))
            self.assertEqual(floatvec.h5object.name, '/entry12345/instrument/detector/floatvec')
            self.assertEqual(floatvec.h5object.dtype, 'float64')
            self.assertEqual(floatvec.h5object.shape, (1, 20, 10))



            vl = [[[self.__rnd.uniform(-20000.0, 20000)
                    for _ in range(70)]
                   for _ in range(80)]
                  for _ in range(80)]
            
            vv = [[[vl[k][j][i] for i in range(10)] for j in range(20)] for k in range(1)]
            floatvec[...] = vv
            self.myAssertVector(floatvec.read(), vv)
            vv2 = [[[vl[k][j+2][i+2] for i in range(10)] for j in range(20)] for k in range(1)]
            floatvec.write(vv2)
            self.myAssertVector(floatvec.read(), vv2)
            
            ##!!! PNI self.myAssertVector([floatvec[...]], vv2)
            self.myAssertVector(floatvec[...], vv2)
            floatvec[...] = vv

            floatvec.grow()
            self.assertEqual(floatvec.shape, (2,20,10))
            self.assertEqual(floatvec.h5object.shape, (2,20,10))

            iv = [[[floatvec[k,j,i] for i in range(10)] for j in range(20)] for k in range(1)]
            self.myAssertVector(iv, vv)
            floatvec[1,:,:] = [[vl[1][j][i] for i in range(10)] for j in range(20)]
            vv3 = [[[vl[k][j][i] for i in range(10)] for j in range(20)] for k in range(2)]
            self.myAssertVector(floatvec[...], vv3)

            floatvec.grow(2, 3)
            self.assertEqual(floatvec.shape, (2,20,13))
            self.assertEqual(floatvec.h5object.shape, (2,20,13))
            vv4 = [[[vl[k][j][i+10] for i in range(3)] for j in range(20)] for k in range(2)]
            vv5 = [[[vl[k][j][i] for i in range(13)] for j in range(20)] for k in range(2)]
            
            floatvec[:,:,10:13] =  vv4
            self.myAssertVector(floatvec[...], vv5)
            self.myAssertVector(floatvec[:,:,0:10], vv3)

            floatvec.grow(1, 4)
            self.assertEqual(floatvec.shape, (2,24,13))
            self.assertEqual(floatvec.h5object.shape, (2,24,13))

            vv6 = [[[vl[k][j][i] for i in range(13)] for j in range(24)] for k in range(2)]
            floatvec.write(vv6)
            self.myAssertVector(floatvec[...], vv6)
            self.myAssertVector(floatvec.read(), vv6)

            attrs = floatvec.attributes
            self.assertTrue(isinstance(attrs, H5PYWriter.H5PYAttributeManager))
            self.assertTrue(isinstance(attrs.h5object, h5py._hl.attrs.AttributeManager))
            self.assertEqual(attrs.parent, floatvec)
            self.assertEqual(len(attrs), 0)            


            
            self.assertTrue(isinstance(intvec, H5PYWriter.H5PYField))
            self.assertTrue(isinstance(intvec.h5object, h5py.Dataset))
            self.assertEqual(intvec.name, 'intvec')
            self.assertEqual(intvec.path, '/entry12345:NXentry/instrument:NXinstrument/detector:NXdetector/intvec')
            self.assertEqual(intvec.dtype, 'uint32')
            self.assertEqual(intvec.shape, (0, 2, 30))
            self.assertEqual(intvec.h5object.name, '/entry12345/instrument/detector/intvec')
            self.assertEqual(intvec.h5object.dtype, 'uint32')
            self.assertEqual(intvec.h5object.shape, (0, 2, 30))


            vl = [[[self.__rnd.randint(1, 1600)
                    for _ in range(70)]
                   for _ in range(18)]
                  for _ in range(8)]
            
            intvec.grow()
            vv = [[[vl[k][j][i] for i in range(30)] for j in range(2)] for k in range(1)]
            
            intvec[...] = vv
            self.myAssertVector(intvec.read(), vv)
            vv2 = [[[vl[k][j+2][i+2] for i in range(30)] for j in range(2)] for k in range(1)]
            intvec.write(vv2)
            self.myAssertVector(intvec.read(), vv2)
            ## !!! PNI self.myAssertVector([intvec[...]], vv2)
            self.myAssertVector(intvec[...], vv2)
            intvec[...] = vv

            intvec.grow()
            self.assertEqual(intvec.shape, (2,2,30))
            self.assertEqual(intvec.h5object.shape, (2,2,30))

            iv = [[[intvec[k,j,i] for i in range(30)] for j in range(2)] for k in range(1)]
            self.myAssertVector(iv, vv)
            intvec[1,:,:] = [[vl[1][j][i] for i in range(30)] for j in range(2)]
            vv3 = [[[vl[k][j][i] for i in range(30)] for j in range(2)] for k in range(2)]
            self.myAssertVector(intvec[...], vv3)

            intvec.grow(2, 3)
            self.assertEqual(intvec.shape, (2,2,33))
            self.assertEqual(intvec.h5object.shape, (2,2,33))
            vv4 = [[[vl[k][j][i+30] for i in range(3)] for j in range(2)] for k in range(2)]
            vv5 = [[[vl[k][j][i] for i in range(33)] for j in range(2)] for k in range(2)]
            
            intvec[:,:,30:33] =  vv4
            self.myAssertVector(intvec[...], vv5)
            self.myAssertVector(intvec[:,:,0:30], vv3)

            intvec.grow(1, 4)
            self.assertEqual(intvec.shape, (2,6,33))
            self.assertEqual(intvec.h5object.shape, (2,6,33))

            vv6 = [[[vl[k][j][i] for i in range(33)] for j in range(6)] for k in range(2)]
            intvec.write(vv6)
            self.myAssertVector(intvec[...], vv6)
            self.myAssertVector(intvec.read(), vv6)

            attrs = intvec.attributes
            self.assertTrue(isinstance(attrs, H5PYWriter.H5PYAttributeManager))
            self.assertTrue(isinstance(attrs.h5object, h5py._hl.attrs.AttributeManager))
            self.assertEqual(attrs.parent, intvec)
            self.assertEqual(len(attrs), 0)            



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
