#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import re
import datastore


class BookProcessor(object):
    def __init__(self):
        """ Create book data store """
        self.ds = datastore.DataStore()

        """ Create custom stores """
        self.keyword = "truth"
        self.keywordCutoff = 2
        self.keywordMulti = []
        self.relYears = collections.Counter()
        self.meanRelYear = {"sum": 0, "num": 0}
        self.engVsNon = {"eng": 0, "non": 0}
        self.maxDialog = {"bookID": "", "num": 0}
        self.maxSize = {"bookID": "", "num": 0}

        """ precompile regex patterns """
        self.startPattern = re.compile('\s*\*\*\* ?START OF TH[EI]S? PROJECT GUTENBERG EBOOK .*')
        self.endPattern = re.compile('\s*\*\*\* ?END OF TH[EI]S? PROJECT GUTENBERG EBOOK .*')
        self.frontPattern = re.compile('.*: .*')
        self.datePattern = re.compile('(Released )?(on )?[A-Za-z]*\s?[0-9]?[0-9]?,? ?([0-9]{4}).*')
        self.startCount = 0

    def containsSeq(self, seq, aset):
        """
        :param seq: sequence of characters to count
        :param aset: iterable (such as a string) in which to count
        :return: number of occurrences of characters in seq found in aset
        Adapted to python3 syntax for fast containsAny from
        https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch01s09.html """
        return len(list(filter(seq.__contains__, aset)))

    def countQuotes(self, line):
        """
        :param line: string in which to count quotes
        :return: number of quotes found in string
        Returns number of unicode double quotation characters found in string
        Selection of unicode double quotation marks according to
        http://www.amp-what.com/unicode/search/quote """
        quotes = u'"“”„«»‟❝❞❠＂'
        return self.containsSeq(quotes, line)

    def trimSpecial(self, word):
        return "".join(list(filter(str.isalnum, word)))

    def countWord(self, word, line):
        """ Strip leading and trailing space and split on whitespace """
        lineList = line.strip().split()
        """ Normalize by removing non-alphanumeric characters and convert to lowercase """
        normalList = list(map(lambda token: self.trimSpecial(token).lower(), lineList))
        """ Extract list of words that equal the word to look for """
        wordList = list(filter(lambda token: token == word, normalList))
        return len(wordList)

    def extractFacts(self, bookID, keys):
        """
        :param keys: list of keys, main key first
        :return: retrieved fact or None
        Retrieves property from list of fact keys in descending order of priority.
        """
        for key in keys:
            if self.ds.factInBook(bookID, key):
                return self.ds.getBookFact(bookID, key)
        print("WARN: book {} has no facts from the list {}!".format(bookID, keys))
        return None

    def addAuthor(self, bookID):
        """
        :param bookID:
        :return:
        Adds book and author fact to data store
        """
        author = self.extractFacts(bookID, ["Author", "Editor"])
        print("Adding author {}".format(author))
        """ Overwrite author in case of editor """
        self.ds.addBookFact(bookID, "Author", author)
        self.ds.addBook(bookID, author)

    def addYear(self, bookID):
        """
        :param bookID:
        :return:
        Adds release year to data store and adds it to averaging tuple
        """
        relDate = self.extractFacts(bookID, ["Release Date", "Posting Date", "__nokey"])
        relYear = self.datePattern.search(relDate).group(3)
        print("Adding release year {}".format(relYear))
        self.ds.addBookFact(bookID, "Release Year", relYear)
        self.relYears[relYear] += 1
        try:
            ry = int(relYear)
            self.meanRelYear["sum"] += ry
            self.meanRelYear["num"] += 1
        except ValueError:
            print("WARN: release year {} does not convert to in for book {}".format(relYear, bookID))

    def addLang(self, bookID):
        """
        :param bookID:
        :return:
        Updates English vs Nonenglish tuple
        """
        language = self.extractFacts(bookID, ["Language"])
        if language is not None:
            if language == "English":
                self.engVsNon["eng"] += 1
            else:
                self.engVsNon["non"] += 1
        else:
            """ One book in the sample without a language tag is in English """
            self.engVsNon["eng"] += 1

    def ingestBook(self, bookID, text):
        """
        :param bookID: same as file name
        :param text: entire text content
        :return:
        Populates self.ds data store with parsed values
        """

        print("Parsing {}...".format(bookID))

        """ Use list as iterator to change context for front matter and full text """
        textIter = iter(text)
        """ Parse front matter """
        for line in textIter:
            if self.startPattern.match(line):
                break
            if self.frontPattern.match(line):
                """ Force pair by supplying maxsplit = 1 parameter """
                key, val = line.strip().split(": ", 1)
                self.ds.addBookFact(bookID, key, val)
            """ Release Date may be missing key """
            if self.datePattern.match(line):
                self.ds.addBookFact(bookID, "__nokey", line)

        self.addAuthor(bookID)
        self.addYear(bookID)
        self.addLang(bookID)

        """ initialize aggregates """
        keywordCount = 0
        paragraph = ""
        quotes = 0
        charSize = 0
        self.ds.addBookFact(bookID, "text", [])
        for line in textIter:
            if self.endPattern.match(line):
                break
            """ append non-empty lines to paragraph, empty lines end paragraph and cause saving it to fulltext """
            line = line.strip()
            if line != "":
                paragraph += line + '\n'
            else:
                if paragraph != "":
                    self.ds.books[bookID]["text"].append(paragraph)
                    paragraph = ""
                continue

            """ count occurrence of 'truth' """
            keywordCount += self.countWord(self.keyword, line)
            """ count quotation marks """
            quotes += self.countQuotes(line)
            """ increment book size """
            charSize += len(line)

        """ ignore end matter and store aggregates """
        if paragraph != "":
            self.ds.books[bookID]["text"].append(paragraph)
        self.ds.addBookFact(bookID, "Quotes", quotes)
        self.ds.addBookFact(bookID, "Size", charSize)
        if keywordCount > self.keywordCutoff:
            self.keywordMulti.append(bookID)
        if quotes > self.maxDialog["num"]:
            self.maxDialog = {"bookID": bookID, "num": quotes}
        if charSize > self.maxSize["num"]:
            self.maxSize = {"bookID": bookID, "num": charSize}

    def outputResults(self):
        """
        :return:
        Outputs results from data store
        """
        print("================================================================")
        outFacts = ["Title", "Author", "Release Year", "Language"]
        for bookID in self.ds.books:
            print("Book file: {}".format(bookID))
            for fact in outFacts:
                value = self.extractFacts(bookID, [fact])
                if value is not None:
                    print("{}: {}".format(fact, value))
            print("----------------------------------------------------------------")

        print("================================================================")
        print("Books with the word {} appearing more than {} times: {}".format(self.keyword, self.keywordCutoff, self.keywordMulti))
        print("Average release year: {:.2f}".format(self.meanRelYear["sum"]/self.meanRelYear["num"]))
        print("Most common release year: {}".format(self.relYears.most_common(1)))
        print("Ratio of English to Nonenglish books: {:.2f}".format(self.engVsNon["eng"]/self.engVsNon["non"]))
        bookID = self.maxDialog["bookID"]
        print("Book with most dialogue: {}, \"{}\" by {}".format(bookID, self.ds.books[bookID]["Title"], self.ds.books[bookID]["Author"]))
        bookID = self.maxSize["bookID"]
        print("Longest book: {}, \"{}\" by {}".format(bookID, self.ds.books[bookID]["Title"], self.ds.books[bookID]["Author"]))
        print("================================================================")



if __name__ == "__main__":
    import unittest


    class TestDataStore(unittest.TestCase):
        def setUp(self):
            self. pc = BookProcessor()

        def tearDown(self):
            del self.pc

        def testTrimSpecial(self):
            self.assertEqual(self.pc.trimSpecial('abc.!?"def'), 'abcdef')

        def testQuotes(self):
            self.assertEqual(self.pc.countQuotes('"hi" “there”'), 4)

        def testCountWord(self):
            self.assertEqual(self.pc.countWord('truth', 'Truth is the truth, no matter the "truth"!'), 3)

        def testAggregate(self):

            def testParse():
                self.pc.ingestBook("1014-0.txt", """
                    Title: The Lure of the Dim Trails
                    Author: by (AKA B. M. Sinclair) B. M. Bower
                    Release Date: August, 1997
                    Language: English
                    *** START OF THIS PROJECT GUTENBERG EBOOK THE LURE OF THE DIM TRAILS ***
                    one line
                    an "other"
                    
                    a paragraph                
                    *** END OF THIS PROJECT GUTENBERG EBOOK THE LURE OF THE DIM TRAILS ***
                    Release Date: August, 2097
                """.splitlines())
                self.assertEqual(self.pc.ds.authors, {'by (AKA B. M. Sinclair) B. M. Bower': ['1014-0.txt']})
                self.assertEqual(self.pc.ds.books, {'1014-0.txt': {'Title': 'The Lure of the Dim Trails', 'Author': 'by (AKA B. M. Sinclair) B. M. Bower',
                    'Release Date': 'August, 1997', 'Language': 'English', 'Release Year': '1997',
                    'text': ['one line\nan "other"\n', 'a paragraph\n'], 'Quotes': 2, 'Size': 29}})



            testParse()

            self.pc.ingestBook("1012-0.txt", """
                Title: La Divina Commedia di Dante
                Author: Dante Alighieri
                Release Date: August, 1997
                Language: Italian
                *** START OF THIS PROJECT GUTENBERG EBOOK LA DIVINA COMMEDIA DI DANTE ***
                a line
                a "quote"
                an "other"
                
                Truth is the truth, no matter the "truth"!
                *** END OF THIS PROJECT GUTENBERG EBOOK LA DIVINA COMMEDIA DI DANTE ***
                Author: Huckleberry Finn
            """.splitlines())

            self.assertEqual(self.pc.keywordMulti, ['1012-0.txt'])
            self.assertEqual(self.pc.relYears, collections.Counter({'1997': 2}))
            self.assertEqual(self.pc.meanRelYear, {'sum': 3994, 'num': 2})
            self.assertEqual(self.pc.engVsNon, {'eng': 1, 'non': 1})
            self.assertEqual(self.pc.maxDialog, {'bookID': '1012-0.txt', 'num': 6})
            self.assertEqual(self.pc.maxSize, {'bookID': '1012-0.txt', 'num': 67})

            self.pc.outputResults()


    print("Testing: {}...".format(__file__))
    unittest.main(exit=False)
