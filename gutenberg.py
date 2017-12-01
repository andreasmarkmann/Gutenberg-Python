#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textzip
import processbook


if __name__ == "__main__":
    pc = processbook.BookProcessor()
    gz = textzip.TextZip('gutenberg.zip')

    count = 0
    for bookID, text in gz.iterFiles:
        pc.ingestBook(bookID, text)

    pc.outputResults()
