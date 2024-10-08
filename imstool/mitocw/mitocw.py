# -*- coding: us-ascii -*-

""" ____________________________________________________________________
 
    This file is part of the imstool software package.

    Copyright (c) 2011 enPraxis, LLC
    http://enpraxis.net

    Portions Copyright (c) 2004-2009 Utah State University
    Portions copyright 2009 Massachusetts Institute of Technology

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 2.8  

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA 
    _______________________________________________________________________
"""

from imstool.base import IMSReader, BaseWriter
from imstool.errors import ManifestError
from .mitreader import MITReader

__author__ = 'Brent Lambert, David Ray, Jon Thomas'
__copyright__ = 'Copyright 2011, enPraxis LLC'

__license__ = 'GPLv2'
__version__ = '$ Revision 0.0 $'[11:-2]
__maintainer__ = 'Brent Lambert'
__email__ = 'brent@enpraxis.net'


class IMSMITReader(IMSReader):
    """ Reader class for MIT OCW files """

    def __init__(self):
        self.zf = None
        self.objManager = None

    def readPackage(self, zf, objManager):
        """ Read the package """
        self.zf = zf
        self.objManager = objManager
        objDict = {}
        mitreader = MITReader()
        manifest = self.readManifest(zf)
        if not manifest:
            raise ManifestError('Could not locate manifest file.')
        doc = mitreader.parseManifest(manifest)
        base = mitreader.readManifestBase(doc)
        objDict['package'] = mitreader.readPackageMetadata(doc)
        orgs = mitreader.readOrganizations(doc)
        resources = mitreader.readResources(doc)

        for x in resources:
            resid, restype, reshref = mitreader.readResourceAttributes(x)
            #A link to external file.
            if reshref.find('http') == 0:
                continue
            location = mitreader.readLocation(x)
            if location:
                dataxml = self.readManifest(zf, manifestfile='%s%s' %(base,location))
                resdata = mitreader.parseDataFile(dataxml)
                metadata = mitreader.readMetadata(resdata)
            else:
                metadata = {}
            files = mitreader.readFiles(base, x)

            if not files and reshref:
                files = ['%s%s' %(base,reshref),]
            for y in files:
                hash = resid + y
                # If there is only one file, or it matches the reshref
                # add the metadata to it if it exists
                if y == reshref or len(files) == 1:
                    objDict[hash] = metadata
                    # If it is listed in the org section
                    if resid in orgs:
                        numval, navval = orgs[resid]
                        if numval:
                            objDict[hash]['position'] = numval
                            objDict[hash]['excludeFromNav'] = False
                        else:
                            objDict[hash]['excludeFromNav'] = True
                        if navval:
                            # Use 'and' as opposed to 'or' to avoid KeyError
                            if not ('title' in objDict[hash] and objDict[hash]['title']):
                                objDict[hash]['title'] = orgs[resid][1]
                    else:
                        objDict[hash]['excludeFromNav'] = True
                    objDict[hash]['type'] = self.determineType(objDict[hash], y)
                    if objDict[hash]['type'] == 'Document':
                        file = self.readFile(zf, y)
                        if file:
                            objDict[hash]['text'] = mitreader.runFilters(file, ['stripchrome'])
                    else:
                        objDict[hash]['file'] =  y
                # If it is just a lowly file
                else:
                    objDict[hash] = {}
                    objDict[hash]['excludeFromNav'] = True
                    objDict[hash]['type'] = self.determineType(objDict[hash], y)
                    if objDict[hash]['type'] == 'Document':
                        file = self.readFile(zf, y)
                        if file:
                            objDict[hash]['text'] = mitreader.runFilters(file, ['stripchrome'])
                    else:
                        objDict[hash]['file'] =  y

                # Add to all files
                id = self.createIdFromFile(y)
                objDict[hash]['id'] = id
                if not ('title' in objDict[hash] and objDict[hash]['title']):
                    objDict[hash]['title'] = id
                objDict[hash]['path'] = self.createPathFromFile(y)

        if self.objManager:
            self.objManager.createObjects(objDict, zf)

    def readFile(self, zf, fn):
        """ Read a file out of the zip archive """
        f = zf.open(fn, 'r')
        data = f.read()
        f.close()
        return data



class IMSMITWriter(BaseWriter):
    """ MIT OCW writer """
	
