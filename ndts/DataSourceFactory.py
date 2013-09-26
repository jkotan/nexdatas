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
## \file DataSourceFactory.py
# data-source types

import sys 

from . import Streams
from . import DataSources
from .Element import Element


## Data source creator
class DataSourceFactory(Element):        
    ## constructor
    # \param attrs dictionary with the tag attributes
    # \param last the last element on the stack
    def __init__(self, attrs, last):
        Element.__init__(self, "datasource", attrs, last)
        ## datasource pool
        self.__dsPool = None


    ## sets the used datasources
    # \param datasources pool to be set
    def setDataSources(self, datasources):
        self.__dsPool = datasources
        

    ## creates data source   
    # \param attrs dictionary with the tag attributes
    def __createDSource(self, attrs):
        if "type" in attrs.keys():
            if self.__dsPool and self.__dsPool.hasDataSource(attrs["type"]):
                self._last.source = self.__dsPool.get(attrs["type"])()
            else:
                print >> sys.stderr, \
                    "DataSourceFactory::__createDSource - Unknown data source"
                if Streams.log_error:
                    print >> Streams.log_error, \
                        "DataSourceFactory::__createDSource - "\
                        "Unknown data source"
                    
                self._last.source = DataSources.DataSource()
        else:
            print >> sys.stderr, \
                "DataSourceFactory::__createDSource - Typeless data source"
            if Streams.log_error:
                print >> Streams.log_error, \
                    "DataSourceFactory::__createDSource - Typeless data source"
            self._last.source = DataSources.DataSource()


    ##  sets the datasource form xml string
    # \param xml input parameter   
    # \param globalJSON global JSON string
    def store(self, xml = None, globalJSON = None):
        self.__createDSource(self._tagAttrs)
        jxml = "".join(xml)
        self._last.source.setup(jxml)
        if hasattr(self._last.source,"setJSON") and globalJSON:
            self._last.source.setJSON(globalJSON)
        if hasattr(self._last.source,"setDataSources"):
            self._last.source.setDataSources(self.__dsPool)
        if self._last and hasattr(self._last,"tagAttributes"):
            self._last.tagAttributes["nexdatas_source"] = ("NX_CHAR", jxml)


    ## sets the used decoders
    # \param decoders pool to be set
    def setDecoders(self, decoders):
        if self._last and self._last.source and self._last.source.isValid() \
                and hasattr(self._last.source,"setDecoders"):
            self._last.source.setDecoders(decoders)
            


