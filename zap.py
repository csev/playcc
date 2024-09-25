from imstool import BaseObjectManager
from imstool import importPackage
from imstool import readers

class MyObjectManager(BaseObjectManager):
    """ Read object metadata and file info and create new objects. """

    def createObject(self, objDict, zf):
        """ Step through object metadata and create objects. """

        for oid in objDict:
            data = objDict[oid]
            if 'package' == oid:
                pass # This is package metadata
            elif 'Document' == data['type']:
                pass # Object is a document
            elif 'File' == data['type']:
                pass # Object is a File
            elif 'Image' == data['type']:
                pass # Object is an Image
            elif 'Quiz' == data['type']:
                pass # Object is a quiz/test
            else:
                pass # Unknown type


nom = MyObjectManager()
format = readers[0]
try:
    za = ZipFile(StringIO(package), 'r')
except BadZipfile as e:
    result = e
else:
    result = importPackage(za, format, nom)



