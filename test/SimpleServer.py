#	"$Name:  $";
#	"$Header:  $";
#=============================================================================
#
# file :        SimpleServer.py
#
# description : Python source for the SimpleServer and its commands. 
#                The class is derived from Device. It represents the
#                CORBA servant object which will be accessed from the
#                network. All commands which can be executed on the
#                SimpleServer are implemented in this file.
#
# project :     TANGO Device Server
#
# $Author:  $
#
# $Revision:  $
#
# $Log:  $
#
# copyleft :    European Synchrotron Radiation Facility
#               BP 220, Grenoble 38043
#               FRANCE
#
#=============================================================================
#  		This file is generated by POGO
#	(Program Obviously used to Generate tango Object)
#
#         (c) - Software Engineering Group - ESRF
#=============================================================================
#


import PyTango
import sys
import numpy
import struct

#==================================================================
#   SimpleServer Class Description:
#
#         My Simple Server
#
#==================================================================
# 	Device States Description:
#
#   DevState.ON :  Server On
#==================================================================


class SimpleServer(PyTango.Device_4Impl):

#--------- Add you global variables here --------------------------

#------------------------------------------------------------------
#	Device constructor
#------------------------------------------------------------------
	def __init__(self,cl, name):
		PyTango.Device_4Impl.__init__(self,cl,name)
		SimpleServer.init_device(self)

#------------------------------------------------------------------
#	Device destructor
#------------------------------------------------------------------
	def delete_device(self):
		print "[Device delete_device method] for device",self.get_name()


#------------------------------------------------------------------
#	Device initialization
#------------------------------------------------------------------
	def init_device(self):
		print "In ", self.get_name(), "::init_device()"
		self.set_state(PyTango.DevState.ON)
		self.get_device_properties(self.get_device_class())

		self.attr_ScalarBoolean=True
		self.attr_ScalarUChar=12
		self.attr_ScalarShort=12
		self.attr_ScalarUShort=12
		self.attr_ScalarLong=123
		self.attr_ScalarULong=123
		self.attr_ScalarLong64=123
		self.attr_ScalarULong64=123
		self.attr_ScalarFloat=-1.23
		self.attr_ScalarDouble=1.233
		self.attr_ScalarString="Hello!"
		self.attr_ScalarEncoded="UTF8","Hello UTF8! Pr\xc3\xb3ba \xe6\xb5\x8b"


		self.attr_SpectrumBoolean = [True, False]
		self.attr_SpectrumUChar = [1,2]
		self.attr_SpectrumShort = [1,-3,4]
		self.attr_SpectrumUShort = [1,4,5,6]
		self.attr_SpectrumLong = [1123,-435,35,-6345]
		self.attr_SpectrumULong = [2341,2344,45,345]
		self.attr_SpectrumLong64 = [1123,-435,35,-6345]
		self.attr_SpectrumULong64 = [1123,23435,35,3345]
		self.attr_SpectrumFloat = [11.23,-4.35,3.5,-634.5]
		self.attr_SpectrumDouble = [1.123,23.435,3.5,3.345]
		self.attr_SpectrumString = ["Hello","Word","!" ,"!!"]
		self.attr_SpectrumEncoded=["INT32","\x00\x01\x03\x04\x20\x31\x43\x54\x10\x11\x13\x14"]
		
		self.attr_ImageBoolean = numpy.array([[True]],dtype='int16')
		self.attr_ImageUChar = numpy.array([[2,5],[3,4]],dtype='uint8')
		self.attr_ImageShort = numpy.array([[2,5],[3,4]],dtype='int16')
		self.attr_ImageUShort = numpy.array([[2,5],[3,4]],dtype='uint16')
		self.attr_ImageLong = numpy.array([[2,5],[3,4]],dtype='int32')
		self.attr_ImageULong = numpy.array([[2,5],[3,4]],dtype='uint32')
		self.attr_ImageLong64 = numpy.array([[2,5],[3,4]],dtype='int64')
		self.attr_ImageULong64 = numpy.array([[2,5],[3,4]],dtype='uint64')
		self.attr_ImageFloat = numpy.array([[2.,5.],[3.,4.]],dtype='float32')
		self.attr_ImageDouble = numpy.array([[2.4,5.45],[3.4,4.45]],dtype='double')
		self.attr_ImageString = [['True']]
		self.attr_ImageEncoded=self.encodeImage()

	def encodeImage(self):
		format = 'VIDEO_IMAGE'
		# uint8 B
		mode = 0
		# uint16 H
#		mode = 1
		height, width = 20, 33
		version = 1
		endian = ord(struct.pack('=H', 1)[-1])
		hsize = struct.calcsize('!IHHqiiHHHH')
		header = struct.pack(
			'!IHHqiiHHHH', 0x5644454f, version, mode, -1, 
			width,  height, endian, hsize, 0, 0)
		image = numpy.array(
			[[(i*j % 256) for i in range(width)] for j in range(height) ], dtype = 'uint8')
		fimage = image.flatten()
		ibuffer = struct.pack('H'*fimage.size, *fimage)
		return format, header+ibuffer
		

  

#------------------------------------------------------------------
#	Always excuted hook method
#------------------------------------------------------------------
	def always_executed_hook(self):
		print "In ", self.get_name(), "::always_excuted_hook()"

#==================================================================
#
#	SimpleServer read/write attribute methods
#
#==================================================================
#------------------------------------------------------------------
#	Read Attribute Hardware
#------------------------------------------------------------------
	def read_attr_hardware(self,data):
		print "In ", self.get_name(), "::read_attr_hardware()"



#------------------------------------------------------------------
#	Read ScalarLong attribute
#------------------------------------------------------------------
	def read_ScalarLong(self, attr):
		print "In ", self.get_name(), "::read_ScalarLong()"
		
		#	Add your own code here		
		attr.set_value(self.attr_ScalarLong)


#------------------------------------------------------------------
#	Write ScalarLong attribute
#------------------------------------------------------------------
	def write_ScalarLong(self, attr):
		print "In ", self.get_name(), "::write_ScalarLong()"

		#	Add your own code here
#		self.attr_ScalarLong = []
#		attr.get_write_value(self.attr_ScalarLong)
		self.attr_ScalarLong = attr.get_write_value()
		print "Attribute value = ", self.attr_ScalarLong


#------------------------------------------------------------------
#	Read ScalarBoolean attribute
#------------------------------------------------------------------
	def read_ScalarBoolean(self, attr):
		print "In ", self.get_name(), "::read_ScalarBoolean()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_ScalarBoolean)


#------------------------------------------------------------------
#	Write ScalarBoolean attribute
#------------------------------------------------------------------
	def write_ScalarBoolean(self, attr):
		print "In ", self.get_name(), "::write_ScalarBoolean()"

		#	Add your own code here
		self.attr_ScalarBoolean = attr.get_write_value()
		print "Attribute value = ", self.attr_ScalarBoolean


#------------------------------------------------------------------
#	Read ScalarShort attribute
#------------------------------------------------------------------
	def read_ScalarShort(self, attr):
		print "In ", self.get_name(), "::read_ScalarShort()"
		
		#	Add your own code here
		attr.set_value(self.attr_ScalarShort)


#------------------------------------------------------------------
#	Write ScalarShort attribute
#------------------------------------------------------------------
	def write_ScalarShort(self, attr):
		print "In ", self.get_name(), "::write_ScalarShort()"

		#	Add your own code here
		self.attr_ScalarShort = attr.get_write_value()
		print "Attribute value = ", self.attr_ScalarShort


#------------------------------------------------------------------
#	Read ScalarUShort attribute
#------------------------------------------------------------------
	def read_ScalarUShort(self, attr):
		print "In ", self.get_name(), "::read_ScalarUShort()"
		
		#	Add your own code here
		attr.set_value(self.attr_ScalarUShort)


#------------------------------------------------------------------
#	Write ScalarUShort attribute
#------------------------------------------------------------------
	def write_ScalarUShort(self, attr):
		print "In ", self.get_name(), "::write_ScalarUShort()"

		#	Add your own code here
		self.attr_ScalarUShort = attr.get_write_value()
		print "Attribute value = ", self.attr_ScalarUShort


#------------------------------------------------------------------
#	Read ScalarULong attribute
#------------------------------------------------------------------
	def read_ScalarULong(self, attr):
		print "In ", self.get_name(), "::read_ScalarULong()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_ScalarULong)


#------------------------------------------------------------------
#	Write ScalarULong attribute
#------------------------------------------------------------------
	def write_ScalarULong(self, attr):
		print "In ", self.get_name(), "::write_ScalarULong()"

		#	Add your own code here
		self.attr_ScalarULong = attr.get_write_value()
		print "Attribute value = ", self.attr_ScalarULong


#------------------------------------------------------------------
#	Read ScalarLong64 attribute
#------------------------------------------------------------------
	def read_ScalarLong64(self, attr):
		print "In ", self.get_name(), "::read_ScalarLong64()"
		
		#	Add your own code here
		attr.set_value(self.attr_ScalarLong64)


#------------------------------------------------------------------
#	Write ScalarLong64 attribute
#------------------------------------------------------------------
	def write_ScalarLong64(self, attr):
		print "In ", self.get_name(), "::write_ScalarLong64()"

		#	Add your own code here
		self.attr_ScalarLong64 = attr.get_write_value()
		print "Attribute value = ", self.attr_ScalarLong64


#------------------------------------------------------------------
#	Read ScalarULong64 attribute
#------------------------------------------------------------------
	def read_ScalarULong64(self, attr):
		print "In ", self.get_name(), "::read_ScalarULong64()"
		
		#	Add your own code here
		attr.set_value(self.attr_ScalarULong64)
		# Do not work as well


#------------------------------------------------------------------
#	Write ScalarULong64 attribute
#------------------------------------------------------------------
	def write_ScalarULong64(self, attr):
		print "In ", self.get_name(), "::write_ScalarULong64()"

		#	Add your own code here
		self.attr_ScalarULong64 = attr.get_write_value()
		print "Attribute value = ", self.attr_ScalarULong64


#------------------------------------------------------------------
#	Read ScalarFloat attribute
#------------------------------------------------------------------
	def read_ScalarFloat(self, attr):
		print "In ", self.get_name(), "::read_ScalarFloat()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_ScalarFloat)


#------------------------------------------------------------------
#	Write ScalarFloat attribute
#------------------------------------------------------------------
	def write_ScalarFloat(self, attr):
		print "In ", self.get_name(), "::write_ScalarFloat()"

		#	Add your own code here
		self.attr_ScalarFloat = attr.get_write_value()
		print "Attribute value = ", self.attr_ScalarFloat


#------------------------------------------------------------------
#	Read ScalarDouble attribute
#------------------------------------------------------------------
	def read_ScalarDouble(self, attr):
		print "In ", self.get_name(), "::read_ScalarDouble()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_ScalarDouble)


#------------------------------------------------------------------
#	Write ScalarDouble attribute
#------------------------------------------------------------------
	def write_ScalarDouble(self, attr):
		print "In ", self.get_name(), "::write_ScalarDouble()"

		#	Add your own code here
		self.attr_ScalarDouble = attr.get_write_value()
		print "Attribute value = ", self.attr_ScalarDouble


#------------------------------------------------------------------
#	Read ScalarString attribute
#------------------------------------------------------------------
	def read_ScalarString(self, attr):
		print "In ", self.get_name(), "::read_ScalarString()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_ScalarString)


#------------------------------------------------------------------
#	Write ScalarString attribute
#------------------------------------------------------------------
	def write_ScalarString(self, attr):
		print "In ", self.get_name(), "::write_ScalarString()"

		#	Add your own code here
		self.attr_ScalarString = attr.get_write_value()
		print "Attribute value = ", self.attr_ScalarString


#------------------------------------------------------------------
#	Read ScalarEncoded attribute
#------------------------------------------------------------------
	def read_ScalarEncoded(self, attr):
		print "In ", self.get_name(), "::read_ScalarEncoded()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_ScalarEncoded[0], self.attr_ScalarEncoded[1])


#------------------------------------------------------------------
#	Write ScalarEncoded attribute
#------------------------------------------------------------------
	def write_ScalarEncoded(self, attr):
		print "In ", self.get_name(), "::write_ScalarEncoded()"

		#	Add your own code here

		# writing encoded attributes not supported for PyTango 7.2.3
#		self.attr_Scalar = []
		attr.get_write_value(self.attr_ScalarEncoded)
		self.attr_ScalarEncoded = attr.get_write_value()
		print "Attribute value = ", self.attr_ScalarEncoded


#------------------------------------------------------------------
#	Read ScalarUChar attribute
#------------------------------------------------------------------
	def read_ScalarUChar(self, attr):
		print "In ", self.get_name(), "::read_ScalarUChar()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_ScalarUChar)


#------------------------------------------------------------------
#	Write ScalarUChar attribute
#------------------------------------------------------------------
	def write_ScalarUChar(self, attr):
		print "In ", self.get_name(), "::write_ScalarUChar()"
		#	Add your own code here
		self.attr_ScalarUChar = attr.get_write_value()
		print "Attribute value = ", self.attr_ScalarUChar


#------------------------------------------------------------------
#	Read SpectrumEncoded attribute
#------------------------------------------------------------------
	def read_SpectrumEncoded(self, attr):
		print "In ", self.get_name(), "::read_SpectrumEncoded()"
		
		#	Add your own code here
		attr.set_value(self.attr_SpectrumEncoded[0], self.attr_SpectrumEncoded[1])


#------------------------------------------------------------------
#	Write SpectrumEncoded attribute
#------------------------------------------------------------------
	def write_SpectrumEncoded(self, attr):
		print "In ", self.get_name(), "::write_SpectrumEncoded()"

		#	Add your own code here
		self.attr_SpectrumEncoded = attr.get_write_value()
		print "Attribute value = ", self.attr_SpectrumEncoded


#------------------------------------------------------------------
#	Read ImageEncoded attribute
#------------------------------------------------------------------
	def read_ImageEncoded(self, attr):
		print "In ", self.get_name(), "::read_ImageEncoded()"
		
		#	Add your own code here
		attr.set_value(self.attr_ImageEncoded[0], self.attr_ImageEncoded[1])


#------------------------------------------------------------------
#	Write ImageEncoded attribute
#------------------------------------------------------------------
	def write_ImageEncoded(self, attr):
		print "In ", self.get_name(), "::write_ImageEncoded()"

		#	Add your own code here
		self.attr_ImageEncoded = attr.get_write_value()
		print "Attribute value = ", self.attr_ImageEncoded


#------------------------------------------------------------------
#	Read SpectrumBoolean attribute
#------------------------------------------------------------------
	def read_SpectrumBoolean(self, attr):
		print "In ", self.get_name(), "::read_SpectrumBoolean()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_SpectrumBoolean)
		print self.attr_SpectrumBoolean


#------------------------------------------------------------------
#	Write SpectrumBoolean attribute
#------------------------------------------------------------------
	def write_SpectrumBoolean(self, attr):
		print "In ", self.get_name(), "::write_SpectrumBoolean()"

		#	Add your own code here
		self.attr_SpectrumBoolean = attr.get_write_value()
		print "Attribute value = ", self.attr_SpectrumBoolean


#------------------------------------------------------------------
#	Read SpectrumUChar attribute
#------------------------------------------------------------------
	def read_SpectrumUChar(self, attr):
		print "In ", self.get_name(), "::read_SpectrumUChar()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_SpectrumUChar)
		print self.attr_SpectrumUChar


#------------------------------------------------------------------
#	Write SpectrumUChar attribute
#------------------------------------------------------------------
	def write_SpectrumUChar(self, attr):
		print "In ", self.get_name(), "::write_SpectrumUChar()"

		#	Add your own code here
		self.attr_SpectrumUChar = attr.get_write_value()
		print "Attribute value = ", self.attr_SpectrumUChar


#------------------------------------------------------------------
#	Read SpectrumShort attribute
#------------------------------------------------------------------
	def read_SpectrumShort(self, attr):
		print "In ", self.get_name(), "::read_SpectrumShort()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_SpectrumShort)
		print self.attr_SpectrumShort


#------------------------------------------------------------------
#	Write SpectrumShort attribute
#------------------------------------------------------------------
	def write_SpectrumShort(self, attr):
		print "In ", self.get_name(), "::write_SpectrumShort()"

		#	Add your own code here
		self.attr_SpectrumShort = attr.get_write_value()
		print "Attribute value = ", self.attr_SpectrumShort


#------------------------------------------------------------------
#	Read SpectrumUShort attribute
#------------------------------------------------------------------
	def read_SpectrumUShort(self, attr):
		print "In ", self.get_name(), "::read_SpectrumUShort()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_SpectrumUShort)
		print self.attr_SpectrumUShort


#------------------------------------------------------------------
#	Write SpectrumUShort attribute
#------------------------------------------------------------------
	def write_SpectrumUShort(self, attr):
		print "In ", self.get_name(), "::write_SpectrumUShort()"

		#	Add your own code here
		self.attr_SpectrumUShort = attr.get_write_value()
		print "Attribute value = ", self.attr_SpectrumUShort


#------------------------------------------------------------------
#	Read SpectrumLong attribute
#------------------------------------------------------------------
	def read_SpectrumLong(self, attr):
		print "In ", self.get_name(), "::read_SpectrumLong()"
		
		#	Add your own code here
		attr.set_value(self.attr_SpectrumLong)
		print self.attr_SpectrumLong


#------------------------------------------------------------------
#	Write SpectrumLong attribute
#------------------------------------------------------------------
	def write_SpectrumLong(self, attr):
		print "In ", self.get_name(), "::write_SpectrumLong()"

		#	Add your own code here
		self.attr_SpectrumLong = attr.get_write_value()
		print "Attribute value = ", self.attr_SpectrumLong


#------------------------------------------------------------------
#	Read SpectrumULong attribute
#------------------------------------------------------------------
	def read_SpectrumULong(self, attr):
		print "In ", self.get_name(), "::read_SpectrumULong()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_SpectrumULong)
		print self.attr_SpectrumULong


#------------------------------------------------------------------
#	Write SpectrumULong attribute
#------------------------------------------------------------------
	def write_SpectrumULong(self, attr):
		print "In ", self.get_name(), "::write_SpectrumULong()"

		#	Add your own code here
		self.attr_SpectrumULong = attr.get_write_value()
		print "Attribute value = ", self.attr_SpectrumULong


#------------------------------------------------------------------
#	Read SpectrumLong64 attribute
#------------------------------------------------------------------
	def read_SpectrumLong64(self, attr):
		print "In ", self.get_name(), "::read_SpectrumLong64()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_SpectrumLong64)
		print self.attr_SpectrumLong64


#------------------------------------------------------------------
#	Write SpectrumLong64 attribute
#------------------------------------------------------------------
	def write_SpectrumLong64(self, attr):
		print "In ", self.get_name(), "::write_SpectrumLong64()"

		#	Add your own code here
		self.attr_SpectrumLong64 = attr.get_write_value()
		print "Attribute value = ", self.attr_SpectrumLong64


#------------------------------------------------------------------
#	Read SpectrumULong64 attribute
#------------------------------------------------------------------
	def read_SpectrumULong64(self, attr):
		print "In ", self.get_name(), "::read_SpectrumULong64()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_SpectrumULong64)
		print self.attr_SpectrumULong64


#------------------------------------------------------------------
#	Write SpectrumULong64 attribute
#------------------------------------------------------------------
	def write_SpectrumULong64(self, attr):
		print "In ", self.get_name(), "::write_SpectrumULong64()"

		#	Add your own code here
		self.attr_SpectrumULong64 = attr.get_write_value()
		print "Attribute value = ", self.attr_SpectrumULong64


#------------------------------------------------------------------
#	Read SpectrumFloat attribute
#------------------------------------------------------------------
	def read_SpectrumFloat(self, attr):
		print "In ", self.get_name(), "::read_SpectrumFloat()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_SpectrumFloat)
		print self.attr_SpectrumFloat


#------------------------------------------------------------------
#	Write SpectrumFloat attribute
#------------------------------------------------------------------
	def write_SpectrumFloat(self, attr):
		print "In ", self.get_name(), "::write_SpectrumFloat()"

		#	Add your own code here
		self.attr_SpectrumFloat = attr.get_write_value()
		print "Attribute value = ", self.attr_SpectrumFloat


#------------------------------------------------------------------
#	Read SpectrumDouble attribute
#------------------------------------------------------------------
	def read_SpectrumDouble(self, attr):
		print "In ", self.get_name(), "::read_SpectrumDouble()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_SpectrumDouble)
		print self.attr_SpectrumDouble


#------------------------------------------------------------------
#	Write SpectrumDouble attribute
#------------------------------------------------------------------
	def write_SpectrumDouble(self, attr):
		print "In ", self.get_name(), "::write_SpectrumDouble()"

		#	Add your own code here
		self.attr_SpectrumDouble = attr.get_write_value()
		print "Attribute value = ", self.attr_SpectrumDouble


#------------------------------------------------------------------
#	Read SpectrumString attribute
#------------------------------------------------------------------
	def read_SpectrumString(self, attr):
		print "In ", self.get_name(), "::read_SpectrumString()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_SpectrumString)
		print self.attr_SpectrumString


#------------------------------------------------------------------
#	Write SpectrumString attribute
#------------------------------------------------------------------
	def write_SpectrumString(self, attr):
		print "In ", self.get_name(), "::write_SpectrumString()"

		#	Add your own code here
		self.attr_SpectrumString = attr.get_write_value()
		print "Attribute value = ", self.attr_SpectrumString


#------------------------------------------------------------------
#	Read ImageBoolean attribute
#------------------------------------------------------------------
	def read_ImageBoolean(self, attr):
		print "In ", self.get_name(), "::read_ImageBoolean()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_ImageBoolean) 
		print self.attr_ImageBoolean


#------------------------------------------------------------------
#	Write ImageBoolean attribute
#------------------------------------------------------------------
	def write_ImageBoolean(self, attr):
		print "In ", self.get_name(), "::write_ImageBoolean()"
		#	Add your own code here
		self.attr_ImageBoolean = attr.get_write_value()
		print "Attribute value = ", self.attr_ImageBoolean


#------------------------------------------------------------------
#	Read ImageUChar attribute
#------------------------------------------------------------------
	def read_ImageUChar(self, attr):
		print "In ", self.get_name(), "::read_ImageUChar()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_ImageUChar) 
		print self.attr_ImageUChar


#------------------------------------------------------------------
#	Write ImageUChar attribute
#------------------------------------------------------------------
	def write_ImageUChar(self, attr):
		print "In ", self.get_name(), "::write_ImageUChar()"
		self.attr_ImageUChar = attr.get_write_value()
		print "Attribute value = ", self.attr_ImageUChar

		#	Add your own code here


#------------------------------------------------------------------
#	Read ImageShort attribute
#------------------------------------------------------------------
	def read_ImageShort(self, attr):
		print "In ", self.get_name(), "::read_ImageShort()"
		
		#	Add your own code here
		attr.set_value(self.attr_ImageShort) 
		print self.attr_ImageShort



#------------------------------------------------------------------
#	Write ImageShort attribute
#------------------------------------------------------------------
	def write_ImageShort(self, attr):
		print "In ", self.get_name(), "::write_ImageShort()"
		#	Add your own code here
		self.attr_ImageShort = attr.get_write_value()
		print "Attribute value = ", self.attr_ImageShort

#------------------------------------------------------------------
#	Read ImageUShort attribute
#------------------------------------------------------------------
	def read_ImageUShort(self, attr):
		print "In ", self.get_name(), "::read_ImageUShort()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_ImageUShort) 
		print self.attr_ImageUShort


#------------------------------------------------------------------
#	Write ImageUShort attribute
#------------------------------------------------------------------
	def write_ImageUShort(self, attr):
		print "In ", self.get_name(), "::write_ImageUShort()"

		#	Add your own code here
		self.attr_ImageUShort = attr.get_write_value()
		print "Attribute value = ", self.attr_ImageUShort


#------------------------------------------------------------------
#	Read ImageLong attribute
#------------------------------------------------------------------
	def read_ImageLong(self, attr):
		print "In ", self.get_name(), "::read_ImageLong()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_ImageLong) 
		print self.attr_ImageLong


#------------------------------------------------------------------
#	Write ImageLong attribute
#------------------------------------------------------------------
	def write_ImageLong(self, attr):
		print "In ", self.get_name(), "::write_ImageLong()"

		#	Add your own code here
		self.attr_ImageLong = attr.get_write_value()
		print "Attribute value = ", self.attr_ImageLong


#------------------------------------------------------------------
#	Read ImageULong attribute
#------------------------------------------------------------------
	def read_ImageULong(self, attr):
		print "In ", self.get_name(), "::read_ImageULong()"
		
		#	Add your own code here
		
		attr.set_value(self.attr_ImageULong) 
		print self.attr_ImageULong


#------------------------------------------------------------------
#	Write ImageULong attribute
#------------------------------------------------------------------
	def write_ImageULong(self, attr):
		print "In ", self.get_name(), "::write_ImageULong()"

		#	Add your own code here
		self.attr_ImageULong = attr.get_write_value()
		print "Attribute value = ", self.attr_ImageULong


#------------------------------------------------------------------
#	Read ImageLong64 attribute
#------------------------------------------------------------------
	def read_ImageLong64(self, attr):
		print "In ", self.get_name(), "::read_ImageLong64()"
		
		#	Add your own code here
		attr.set_value(self.attr_ImageLong64) 
		print self.attr_ImageLong64
		


#------------------------------------------------------------------
#	Write ImageLong64 attribute
#------------------------------------------------------------------
	def write_ImageLong64(self, attr):
		print "In ", self.get_name(), "::write_ImageLong64()"
		#	Add your own code here
		self.attr_ImageLong64 = attr.get_write_value()
		print "Attribute value = ", self.attr_ImageLong64


#------------------------------------------------------------------
#	Read ImageULong64 attribute
#------------------------------------------------------------------
	def read_ImageULong64(self, attr):
		print "In ", self.get_name(), "::read_ImageULong64()"
		
		#	Add your own code here
		attr.set_value(self.attr_ImageULong64)
		print self.attr_ImageULong64
		


#------------------------------------------------------------------
#	Write ImageULong64 attribute
#------------------------------------------------------------------
	def write_ImageULong64(self, attr):
		print "In ", self.get_name(), "::write_ImageULong64()"

		#	Add your own code here
		self.attr_ImageULong64 = attr.get_write_value()
		print "Attribute value = ", self.attr_ImageULong64


#------------------------------------------------------------------
#	Read ImageFloat attribute
#------------------------------------------------------------------
	def read_ImageFloat(self, attr):
		print "In ", self.get_name(), "::read_ImageFloat()"
		
		#	Add your own code here
		attr.set_value(self.attr_ImageFloat)
		print self.attr_ImageFloat
		


#------------------------------------------------------------------
#	Write ImageFloat attribute
#------------------------------------------------------------------
	def write_ImageFloat(self, attr):
		print "In ", self.get_name(), "::write_ImageFloat()"

		#	Add your own code here
		self.attr_ImageFloat = attr.get_write_value()
		print "Attribute value = ", self.attr_ImageFloat


#------------------------------------------------------------------
#	Read ImageDouble attribute
#------------------------------------------------------------------
	def read_ImageDouble(self, attr):
		print "In ", self.get_name(), "::read_ImageDouble()"
		
		#	Add your own code here
		attr.set_value(self.attr_ImageDouble)
		print self.attr_ImageDouble
		


#------------------------------------------------------------------
#	Write ImageDouble attribute
#------------------------------------------------------------------
	def write_ImageDouble(self, attr):
		print "In ", self.get_name(), "::write_ImageDouble()"

		#	Add your own code here
		self.attr_ImageDouble = attr.get_write_value()
		print "Attribute value = ", self.attr_ImageDouble


#------------------------------------------------------------------
#	Read ImageString attribute
#------------------------------------------------------------------
	def read_ImageString(self, attr):
		print "In ", self.get_name(), "::read_ImageString()"
		
		#	Add your own code here
		attr.set_value(self.attr_ImageString)
		print self.attr_ImageString
		


#------------------------------------------------------------------
#	Write ImageString attribute
#------------------------------------------------------------------
	def write_ImageString(self, attr):
		print "In ", self.get_name(), "::write_ImageString()"

		#	Add your own code here
		self.attr_ImageString = attr.get_write_value()
		print "Attribute value = ", self.attr_ImageString



#==================================================================
#
#	SimpleServer command methods
#
#==================================================================

#==================================================================
#
#	SimpleServerClass class definition
#
#==================================================================
class SimpleServerClass(PyTango.DeviceClass):

	#	Class Properties
	class_property_list = {
		}


	#	Device Properties
	device_property_list = {
		}


	#	Command definitions
	cmd_list = {
		}


	#	Attribute definitions
	attr_list = {
		'ScalarLong':
			[[PyTango.DevLong,
			PyTango.SCALAR,
			PyTango.READ_WRITE],
			{
				'description':"test long scalar attribute",
			} ],
		'ScalarBoolean':
			[[PyTango.DevBoolean,
			PyTango.SCALAR,
			PyTango.READ_WRITE],
			{
				'description':"test scalar bool attribute",
			} ],
		'ScalarShort':
			[[PyTango.DevShort,
			PyTango.SCALAR,
			PyTango.READ_WRITE],
			{
				'description':"Scalar Short attribute",
			} ],
		'ScalarUShort':
			[[PyTango.DevUShort,
			PyTango.SCALAR,
			PyTango.READ_WRITE],
			{
				'description':"ScalarUShort attribute",
			} ],
		'ScalarULong':
			[[PyTango.DevULong,
			PyTango.SCALAR,
			PyTango.READ_WRITE],
			{
				'description':"ScalarULong attribute",
			} ],
		'ScalarLong64':
			[[PyTango.DevLong64,
			PyTango.SCALAR,
			PyTango.READ_WRITE],
			{
				'description':"ScalarLong64 attribute",
			} ],
		'ScalarULong64':
			[[PyTango.DevULong64,
			PyTango.SCALAR,
			PyTango.READ_WRITE],
			{
				'description':"ScalarULong64 attribute",
			} ],
		'ScalarFloat':
			[[PyTango.DevFloat,
			PyTango.SCALAR,
			PyTango.READ_WRITE],
			{
				'description':"ScalarFloat attribute",
			} ],
		'ScalarDouble':
			[[PyTango.DevDouble,
			PyTango.SCALAR,
			PyTango.READ_WRITE],
			{
				'description':"ScalarDouble attribute",
			} ],
		'ScalarString':
			[[PyTango.DevString,
			PyTango.SCALAR,
			PyTango.READ_WRITE],
			{
				'description':"ScalarString attribute",
			} ],
		'ScalarEncoded':
			[[PyTango.DevEncoded,
			PyTango.SCALAR,
			PyTango.READ_WRITE],
			{
				'description':"ScalarEncoded attribute",
			} ],
		'ScalarUChar':
			[[PyTango.DevUChar,
			PyTango.SCALAR,
			PyTango.READ_WRITE],
			{
				'description':"ScalarUChar attribute",
			} ],
		'SpectrumEncoded':
			[[PyTango.DevEncoded,
			PyTango.SCALAR,
			PyTango.READ_WRITE],
			{
				'description':"SpectrumEncoded attribute",
			} ],
		'ImageEncoded':
			[[PyTango.DevEncoded,
			PyTango.SCALAR,
			PyTango.READ_WRITE],
			{
				'description':"ImageEncoded attribute",
			} ],
		'SpectrumBoolean':
			[[PyTango.DevBoolean,
			PyTango.SPECTRUM,
			PyTango.READ_WRITE, 4096],
			{
				'description':"SpectrumBoolean attribute",
			} ],
		'SpectrumUChar':
			[[PyTango.DevUChar,
			PyTango.SPECTRUM,
			PyTango.READ_WRITE, 4096],
			{
				'description':"SpectrumUChar attribute",
			} ],
		'SpectrumShort':
			[[PyTango.DevShort,
			PyTango.SPECTRUM,
			PyTango.READ_WRITE, 4096],
			{
				'description':"SpectrumShort attribute",
			} ],
		'SpectrumUShort':
			[[PyTango.DevUShort,
			PyTango.SPECTRUM,
			PyTango.READ_WRITE, 4096],
			{
				'description':"SpectrumUShort",
			} ],
		'SpectrumLong':
			[[PyTango.DevLong,
			PyTango.SPECTRUM,
			PyTango.WRITE, 4096],
			{
				'description':"SpectrumLong attribute",
			} ],
		'SpectrumULong':
			[[PyTango.DevULong,
			PyTango.SPECTRUM,
			PyTango.READ_WRITE, 4096],
			{
				'description':"SpectrumULong attribute",
			} ],
		'SpectrumLong64':
			[[PyTango.DevLong64,
			PyTango.SPECTRUM,
			PyTango.READ_WRITE, 4096],
			{
				'description':"SpectrumLong64 attribute",
			} ],
		'SpectrumULong64':
			[[PyTango.DevULong64,
			PyTango.SPECTRUM,
			PyTango.READ_WRITE, 4096],
			{
				'description':"SpectrumULong64 attribute",
			} ],
		'SpectrumFloat':
			[[PyTango.DevFloat,
			PyTango.SPECTRUM,
			PyTango.READ_WRITE, 4096],
			{
				'description':"SpectrumFloat attribute",
			} ],
		'SpectrumDouble':
			[[PyTango.DevDouble,
			PyTango.SPECTRUM,
			PyTango.READ_WRITE, 4096],
			{
				'description':"SpectrumDouble attribute",
			} ],
		'SpectrumString':
			[[PyTango.DevString,
			PyTango.SPECTRUM,
			PyTango.READ_WRITE, 4096],
			{
				'description':"SpectrumString attribute",
			} ],
		'ImageBoolean':
			[[PyTango.DevBoolean,
			PyTango.IMAGE,
			PyTango.READ_WRITE, 4096, 4096],
			{
				'description':"ImageBoolean attribute",
			} ],
		'ImageUChar':
			[[PyTango.DevUChar,
			PyTango.IMAGE,
			PyTango.READ_WRITE, 4096, 4096],
			{
				'description':"ImageUChar attribute",
			} ],
		'ImageShort':
			[[PyTango.DevShort,
			PyTango.IMAGE,
			PyTango.READ_WRITE, 4096, 4096],
			{
				'description':"ImageShort attribute",
			} ],
		'ImageUShort':
			[[PyTango.DevUShort,
			PyTango.IMAGE,
			PyTango.READ_WRITE, 4096, 4096],
			{
				'description':"ImageUShort attribute",
			} ],
		'ImageLong':
			[[PyTango.DevLong,
			PyTango.IMAGE,
			PyTango.READ_WRITE, 4096, 4096],
			{
				'description':"ImageLong attribute",
			} ],
		'ImageULong':
			[[PyTango.DevULong,
			PyTango.IMAGE,
			PyTango.READ_WRITE, 4096, 4096],
			{
				'description':"ImageULong attribute",
			} ],
		'ImageLong64':
			[[PyTango.DevLong64,
			PyTango.IMAGE,
			PyTango.READ_WRITE, 4096, 4096],
			{
				'description':"ImageLong64 attribute",
			} ],
		'ImageULong64':
			[[PyTango.DevULong64,
			PyTango.IMAGE,
			PyTango.READ_WRITE, 4096, 4096],
			{
				'description':"ImageULong64 attribute",
			} ],
		'ImageFloat':
			[[PyTango.DevFloat,
			PyTango.IMAGE,
			PyTango.READ_WRITE, 4096, 4096],
			{
				'description':"ImageFloat attribute",
			} ],
		'ImageDouble':
			[[PyTango.DevDouble,
			PyTango.IMAGE,
			PyTango.READ_WRITE, 4096, 4096],
			{
				'description':"ImageDouble attribute",
			} ],
		'ImageString':
			[[PyTango.DevString,
			PyTango.IMAGE,
			PyTango.READ_WRITE, 4096, 4096],
			{
				'description':"ImageString attribute",
			} ],
		}


#------------------------------------------------------------------
#	SimpleServerClass Constructor
#------------------------------------------------------------------
	def __init__(self, name):
		PyTango.DeviceClass.__init__(self, name)
		self.set_type(name);
		print "In SimpleServerClass  constructor"

#==================================================================
#
#	SimpleServer class main method
#
#==================================================================
if __name__ == '__main__':
	try:
		py = PyTango.Util(sys.argv)
		py.add_TgClass(SimpleServerClass,SimpleServer,'SimpleServer')

		U = PyTango.Util.instance()
		U.server_init()
		U.server_run()

	except PyTango.DevFailed,e:
		print '-------> Received a DevFailed exception:',e
	except Exception,e:
		print '-------> An unforeseen exception occured....',e
