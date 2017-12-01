#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zipfile
import re


class TextZip(object):
    def __init__(self, fileName):
        """
        :param fileName: name of zip file containing texts
        Opens zip file and stores filenames of texts therein in self.textNames
        """
        self.zf = zipfile.ZipFile(fileName, 'r')
        namePattern = re.compile('^(?!__MACOS).+\.txt')
        self.textNames = [name for name in self.zf.namelist() if namePattern.match(name)]

    def replaceCEquot(self, line):
        """
        :param line: line of text to replace Windows characters in
        :return: same line with "\x93" and "\x94" replaced by ordinary quotation mark
        Translates Windows Central European quotation marks to simple quotes according to
        https://www.cl.cam.ac.uk/~mgk25/ucs/quotes.html """
        return b"".join(map(lambda char: bytes([char]) if char not in b"\x93\x94" else b'"', line))

    @property
    def iterFiles(self):
        """
        :return: generates tuple of fileName, fileUTF8, where fileUTF8 is array of UTF8 encoded strings representing lines in text
        Reads files, split text into lines, convert Windows quotation marks, and decodes unicode
        """
        for fileName in self.textNames:
            """ Check extracted file size, as it is possible to create small zip files extracting to very large strings """
            fileInfo = self.zf.getinfo(fileName)
            """ Test for max size of 10MiB and negative size in case of integer overflow """
            if fileInfo.file_size < 0 or fileInfo.file_size > 10<<20:
                print("ERROR: Zipped text file {} exceeds size limit, aborting.".format(fileName))
            fileContent = self.zf.read(fileName).splitlines()
            fileFromCE = list(map(lambda line: self.replaceCEquot(line), fileContent))
            """ decode to unicode, ignoring characters we are not interested in """
            fileUTF8 = list(map(lambda line: line.decode('utf-8', 'ignore'), fileFromCE))
            yield fileName, fileUTF8


if __name__ == "__main__":
    import unittest


    class TestGuten(unittest.TestCase):
        def setUp(self):
            self.gz = TextZip('gutenberg.zip')

        def tearDown(self):
            del self.gz

        def testFileNum(self):
            self.assertEqual(len(self.gz.textNames), 761)

        def testFileName(self):
            self.assertEqual(self.gz.textNames[0], "1012-0.txt")
            self.assertEqual(self.gz.textNames[len(self.gz.textNames) - 1], "993-0.txt")

        def testFileLines(self):
            lineLen = [len(text) for fileName, text in self.gz.iterFiles]
            self.assertEqual(lineLen[0], 20023)
            self.assertEqual(lineLen[len(lineLen) - 1], 5405)


    print("Testing: {}...".format(__file__))
    unittest.main(exit=False)
