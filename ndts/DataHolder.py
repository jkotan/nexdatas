#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012-2013 DESY, Jan Kotanski <jkotan@mail.desy.de>
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
## \package ndts nexdatas
## \file DataHolder.py
# holder for data
                         
from Types import NTP

import numpy

## Holder for passing data 
class DataHolder(object):

    ## constructor
    # \param format format of the data, i.e. SCALAR, SPECTRUM, IMAGE
    # \param value value of the data. It may be also 1D and 2D array
    # \param tangoDType type of the data
    # \param shape shape of the data
    # \param encoding encoding type of Tango DevEncoded varibles
    # \param decoders poll with decoding classes
    def __init__(self, format, value, tangoDType, shape, encoding = None, decoders = None):

        ## data format
        self.format = format
        ## data value
        self.value = value
        ## data type
        self.tangoDType = tangoDType
        ## data shape
        self.shape = shape 
        ## encoding type of Tango DevEncoded varibles
        self.encoding = str(encoding) if encoding else None
        ## pool with decoding algorithm
        self.decoders = decoders

        if str(self.tangoDType) == 'DevEncoded':
            self.__setupEncoded()


    def __setupEncoded(self):    
        self.shape = None
        if self.encoding and self.decoders and \
                self.decoders.hasDecoder(self.encoding):
            decoder = self.decoders.get(self.encoding)
            decoder.load(self.value)
            self.shape = decoder.shape()
            if self.shape:
                self.value = decoder.decode()
                rank = NTP().arrayRank(self.value)
                if rank > 2 :
                    raise ValueError, "Unsupported variables format"
                self.format = ["SCALAR","SPECTRUM","IMAGE"][rank]
                
            tp =  decoder.dtype
            if tp in NTP.npTt.keys():

                self.tangoDType = NTP.npTt[tp]
                
        if self.value is None:        
            raise ValueError, "Encoding of DevEncoded variables not defined"

        if self.shape is None:
            raise ValueError, "Encoding  or Shape not defined"


    ## casts the data into given type
    # \param tp given type of data
    # \returns numpy array of defined type or list for strings or value for SCALAR
    def cast(self, tp):
        if str(self.format).split('.')[-1] == "SCALAR":
            if tp in NTP.npTt.keys() and NTP.npTt[tp] == str(self.tangoDType):
                return self.value
            else:
                if self.value == "" and tp != 'string':
                    return NTP.convert[tp](0)
                else:
                    return NTP.convert[tp](self.value)
            
        else:
#            if str(self.tangoDType) == 'DevEncoded':
#                raise ValueError, "Array of DevEncoded variables not supported"

            if tp in NTP.npTt.keys() and NTP.npTt[tp] == str(self.tangoDType) and tp != "string":
                    return numpy.array(self.value, dtype=tp)
            else:    
                if str(self.format).split('.')[-1] == "SPECTRUM":
                    if tp == "string":
                        return [ NTP.convert[tp](el) for el in self.value]
                    else:
                        return numpy.array([ NTP.convert[tp](el) for el in self.value], dtype=tp)
                
                if str(self.format).split('.')[-1] == "IMAGE":
                    if tp == "string":
                        return [ [ NTP.convert[tp](self.value[j][i]) \
                                       for i in range(len(self.value[j])) ] \
                                     for j in range(len(self.value)) ]
                    else:
                        
                        return numpy.array([ [ NTP.convert[tp](self.value[j][i]) \
                                                   for i in range(len(self.value[j])) ] \
                                                 for j in range(len(self.value)) ], dtype=tp)

        

