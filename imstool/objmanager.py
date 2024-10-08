# -*- coding: us-ascii -*-

""" ____________________________________________________________________
 
    This file is part of the imstool software package.

    Copyright (c) 2011 enPraxis, LLC
    http://enpraxis.net

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

__author__ = 'Brent Lambert'
__copyright__ = 'Copyright 2011, enPraxis LLC'

__license__ = 'GPLv2'
__version__ = '$ Revision 0.0 $'[11:-2]
__maintainer__ = 'Brent Lambert'
__email__ = 'brent@enpraxis.net'


class BaseObjManager:
    """ Base Object manager, override to integrate with your app. """

    def createObjects(self, objDict, zf):
        """ Create objects with a list of resources and the 
            ZipFile object. """

    
