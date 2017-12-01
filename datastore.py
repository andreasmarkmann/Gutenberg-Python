#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections


class DataStore(object):
    def __init__(self):
        """
        Relational schema for books and authors:
        For books, use text file name as key, with a dictionary as a value. In value dict, store metadata and text.
        For authors, use author name as key, with list of book file names (keys in the books dict) as value.
        """
        self.books = collections.defaultdict(dict)
        self.authors = collections.defaultdict(list)

    def addBook(self, bookID, author):
        self.authors[author].append(bookID)

    def addBookFact(self, bookID, factKey, factVal):
        self.books[bookID][factKey] = factVal

    def factInBook(self, bookID, factKey):
        return factKey in self.books[bookID]

    def getBookFact(self, bookID, factKey):
        return self.books[bookID][factKey]

    def __str__(self):
        return str(self.authors) + '\n' + str(self.books)


if __name__ == "__main__":
    import unittest


    class TestDataStore(unittest.TestCase):
        def setUp(self):
            self.ds = DataStore()

        def tearDown(self):
            del self.ds

        def testAddBook(self):
            author = "A.N. Author"
            bookID = "123-0.txt"
            self.ds.addBook(bookID, author)
            self.assertEqual(self.ds.authors, {author: [bookID]})

        def testAddFact(self):
            bookID = "123-0.txt"
            factKey = "Language"
            factVal = "Italian"
            self.ds.addBookFact(bookID, factKey, factVal)
            self.assertEqual(self.ds.books, {bookID: {factKey: factVal} })

    print("Testing: {}...".format(__file__))
    unittest.main(exit=False)
