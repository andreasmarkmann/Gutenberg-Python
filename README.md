# Gutenberg Text Aggregation

## Goals

- In which books does the word “truth” appear more than twice?
- What is the average release date? (The year the book was released on project Gutenberg)
- What is the most common release date?
- What is the ratio of English books to non English books?
- Which book has the most dialogue between characters?
- Which book is the longest?
- Design relational schema to house the following information:
    * Information about a book, such as title, author, language, and raw text delineated by paragraph
    * Information about an author such as name, and what books they’ve written

## Goals, Defined

- The question of "most dialogue in a book" may be defined as excluding inner monologue and counting interrupted utterances such as
"There", she said, "it is."
only once. In the interest of time, only the number of quotation characters is counted.
- The number of characters is used to define the longest book.
- Not all books have an author, using editor instead if no author given.
- Release date accepted in the forms "Release Date: <date>", "Release on <date>", "Released <date>".
- Not all books have a release date, using "Posting Date" if no release date given.

## Design Decisions

- In the interest of creating code in a short time, the project is executed as a single-threaded Python code with data stored in memory.
- In a real-world application, most data can be stored in an external database and aggregates evaluated from parallelized data as a streaming job with asynchronous, multi-threaded execution.

Relational schema for books and authors:
For books, use text file name as key, with a dictionary as a value. In value dict, store metadata and text.
For authors, use author name as key, with list of book file names (keys in the books dict) as value.

- To collect aggregates, a complete data store is not needed, so the code is organized as a streaming processor.
- Texts are loaded directly from the zip file to memory to reduce I/O load.
- As it is possible to create synthetic zip files that extract to very large files, text size is checked to prevent buffer overflow.
- Test-driven design was used to implement modules quickly.
- Module `datastore.py` implements storage for authors and books.
- Module `textzip.py` implements loading of books from zip file as unicode, with conversion of Windows characters of interest (double quotes).
- Module `processbook.py` implements ingestion of texts into datastore and computation and output of goal aggregates.
- `gutenberg.py` is the main program.

## Implementation Details

- Some texts use Windows Central European quotation marks which had to be translated to simple quotes according to
        https://www.cl.cam.ac.uk/~mgk25/ucs/quotes.html

## Goals Output by Code, from SampleOutput.txt

```
================================================================
Books with the word truth appearing more than 2 times: ['1014-0.txt', '1015-0.txt', '102-0.txt', '1022-0.txt', '1024-0.txt', '1026-0.txt', '1027-0.txt', '1028-0.txt', '1029-0.txt', '1030-0.txt', '1036-0.txt', '1038-0.txt', '1042-0.txt', '1046-0.txt', '1047-0.txt', '1048-0.txt', '1053-0.txt', '1054-0.txt', '1055-0.txt', '1057-0.txt', '1058-0.txt', '1059-0.txt', '1066-0.txt', '1069-0.txt', '1074-0.txt', '1075-0.txt', '1076-0.txt', '1077-0.txt', '1078-0.txt', '108-0.txt', '1081-0.txt', '1083-0.txt', '1088-0.txt', '1089-0.txt', '1092-0.txt', '1095-0.txt', '1097-0.txt', '1098-0.txt', '1099-0.txt', '111-0.txt', '1138-0.txt', '1145-0.txt', '1147-0.txt', '1148-0.txt', '1154-0.txt', '1155-0.txt', '1156-0.txt', '1157-0.txt', '1158-0.txt', '1159-0.txt', '1164-0.txt', '1167-0.txt', '1168-0.txt', '1182-0.txt', '1183-0.txt', '1184-0.txt', '119-0.txt', '1192-0.txt', '1193-0.txt', '1197-0.txt', '1198-0.txt', '1200-0.txt', '1203-0.txt', '1204-0.txt', '1206-0.txt', '1207-0.txt', '121-0.txt', '1212-0.txt', '1214-0.txt', '1217-0.txt', '1218-0.txt', '122-0.txt', '1223-0.txt', '1231-0.txt', '1235-0.txt', '1236-0.txt', '1237-0.txt', '1244-0.txt', '1245-0.txt', '125-0.txt', '1257-0.txt', '1259-0.txt', '1262-0.txt', '1263-0.txt', '1264-0.txt', '1267-0.txt', '1268-0.txt', '1269-0.txt', '1274-0.txt', '1275-0.txt', '1279-0.txt', '1282-0.txt', '1288-0.txt', '1289-0.txt', '1290-0.txt', '1292-0.txt', '1294-0.txt', '1297-0.txt', '1298-0.txt', '1299-0.txt', '1300-0.txt', '1303-0.txt', '1307-0.txt', '1310-0.txt', '1312-0.txt', '1313-0.txt', '1314-0.txt', '1316-0.txt', '1320-0.txt', '1327-0.txt', '1329-0.txt', '133-0.txt', '1334-0.txt', '134-0.txt', '1342-0.txt', '1343-0.txt', '1344-0.txt', '1348-0.txt', '135-0.txt', '1350-0.txt', '1352-0.txt', '1353-0.txt', '1354-0.txt', '1355-0.txt', '1366-0.txt', '1368-0.txt', '1369-0.txt', '1371-0.txt', '1374-0.txt', '1375-0.txt', '1376-0.txt', '1377-0.txt', '1378-0.txt', '1379-0.txt', '1380-0.txt', '1381-0.txt', '1382-0.txt', '1383-0.txt', '1385-0.txt', '1386-0.txt', '1389-0.txt', '1390-0.txt', '1391-0.txt', '1396-0.txt', '1399-0.txt', '140-0.txt', '1400-0.txt', '1402-0.txt', '1403-0.txt', '1405-0.txt', '141-0.txt', '1410-0.txt', '1417-0.txt', '142-0.txt', '1424-0.txt', '1429-0.txt', '143-0.txt', '1430-0.txt', '1431-0.txt', '1432-0.txt', '1437-0.txt', '1438-0.txt', '1439-0.txt', '144-0.txt', '1440-0.txt', '1441-0.txt', '1442-0.txt', '1443-0.txt', '1447-0.txt', '1449-0.txt', '1453-0.txt', '1454-0.txt', '1457-0.txt', '1460-0.txt', '1461-0.txt', '1467-0.txt', '147-0.txt', '1471-0.txt', '1472-0.txt', '1477-0.txt', '1480-0.txt', '1481-0.txt', '1482-0.txt', '1484-0.txt', '1491-0.txt', '1492-0.txt', '1495-0.txt', '1519-0.txt', '1537-0.txt', '155-0.txt', '1553-0.txt', '1554-0.txt', '1556-0.txt', '1557-0.txt', '1559-0.txt', '1560-0.txt', '1563-0.txt', '1568-0.txt', '1569-0.txt', '1573-0.txt', '1574-0.txt', '158-0.txt', '1585-0.txt', '1586-0.txt', '1587-0.txt', '1588-0.txt', '1597-0.txt', '16-0.txt', '160-0.txt', '1601-0.txt', '1602-0.txt', '1603-0.txt', '1604-0.txt', '1605-0.txt', '1606-0.txt', '1608-0.txt', '1611-0.txt', '1613-0.txt', '1614-0.txt', '1615-0.txt', '1620-0.txt', '1621-0.txt', '1622-0.txt', '1623-0.txt', '1624-0.txt', '1625-0.txt', '1626-0.txt', '1627-0.txt', '1628-0.txt', '1629-0.txt', '1630-0.txt', '1634-0.txt', '1637-0.txt', '1639-0.txt', '1640-0.txt', '1641-0.txt', '1644-0.txt', '1649-0.txt', '165-0.txt', '1652-0.txt', '1654-0.txt', '166-0.txt', '1660-0.txt', '1665-0.txt', '1667-0.txt', '1668-0.txt', '1671-0.txt', '1678-0.txt', '1679-0.txt', '1683-0.txt', '1685-0.txt', '1686-0.txt', '1690-0.txt', '1692-0.txt', '1693-0.txt', '1695-0.txt', '1696-0.txt', '1699-0.txt', '1701-0.txt', '1703-0.txt', '1704-0.txt', '1709-0.txt', '171-0.txt', '1711-0.txt', '1712-0.txt', '1715-0.txt', '1716-0.txt', '1717-0.txt', '1721-0.txt', '1723-0.txt', '1729-0.txt', '1732-0.txt', '1733-0.txt', '1734-0.txt', '1740-0.txt', '1741-0.txt', '1743-0.txt', '1747-0.txt', '1748-0.txt', '1749-0.txt', '1751-0.txt', '1752-0.txt', '176-0.txt', '177-0.txt', '178-0.txt', '1803-0.txt', '1804-0.txt', '1809-0.txt', '1810-0.txt', '1811-0.txt', '1812-0.txt', '1814-0.txt', '1817-0.txt', '1818-0.txt', '1828-0.txt', '1829-0.txt', '1832-0.txt', '1833-0.txt', '1834-0.txt', '1835-0.txt', '1836-0.txt', '1837-0.txt', '1839-0.txt', '1840-0.txt', '1842-0.txt', '1843-0.txt', '1845-0.txt', '1846-0.txt', '1848-0.txt', '1849-0.txt', '1851-0.txt', '1853-0.txt', '1854-0.txt', '1855-0.txt', '1856-0.txt', '1857-0.txt', '1858-0.txt', '1860-0.txt', '1862-0.txt', '1868-0.txt', '1869-0.txt', '1871-0.txt', '1872-0.txt', '1873-0.txt', '1874-0.txt', '1876-0.txt', '1877-0.txt', '1878-0.txt', '1880-0.txt', '1881-0.txt', '1882-0.txt', '1883-0.txt', '1888-0.txt', '1895-0.txt', '1896-0.txt', '1897-0.txt', '1898-0.txt', '1899-0.txt', '1900-0.txt', '1904-0.txt', '1905-0.txt', '1907-0.txt', '1908-0.txt', '1912-0.txt', '1913-0.txt', '1915-0.txt', '1916-0.txt', '1917-0.txt', '1921-0.txt', '1926-0.txt', '1930-0.txt', '1931-0.txt', '1937-0.txt', '1938-0.txt', '1939-0.txt', '1942-0.txt', '1944-0.txt', '1947-0.txt', '1950-0.txt', '1951-0.txt', '1954-0.txt', '1955-0.txt', '1956-0.txt', '1957-0.txt', '1960-0.txt', '1961-0.txt', '1962-0.txt', '1965-0.txt', '1966-0.txt', '1967-0.txt', '1969-0.txt', '1970-0.txt', '1975-0.txt', '1976-0.txt', '1980-0.txt', '1983-0.txt', '1985-0.txt', '1986-0.txt', '1990-0.txt', '1991-0.txt', '1992-0.txt', '1998-0.txt', '1999-0.txt', '202-0.txt', '203-0.txt', '204-0.txt', '205-0.txt', '208-0.txt', '209-0.txt', '21-0.txt', '211-0.txt', '217-0.txt', '219-0.txt', '221-0.txt', '223-0.txt', '224-0.txt', '225-0.txt', '233-0.txt', '236-0.txt', '243-0.txt', '244-0.txt', '245-0.txt', '247-0.txt', '248-0.txt', '260-0.txt', '267-0.txt', '268-0.txt', '269-0.txt', '270-0.txt', '282-0.txt', '283-0.txt', '285-0.txt', '287-0.txt', '290-0.txt', '291-0.txt', '292-0.txt', '293-0.txt', '294-0.txt', '295-0.txt', '298-0.txt', '299-0.txt', '305-0.txt', '306-0.txt', '308-0.txt', '311-0.txt', '316-0.txt', '319-0.txt', '32-0.txt', '322-0.txt', '323-0.txt', '325-0.txt', '329-0.txt', '331-0.txt', '332-0.txt', '336-0.txt', '337-0.txt', '339-0.txt', '340-0.txt', '341-0.txt', '342-0.txt', '346-0.txt', '349-0.txt', '350-0.txt', '356-0.txt', '359-0.txt', '361-0.txt', '362-0.txt', '363-0.txt', '367-0.txt', '368-0.txt', '369-0.txt', '372-0.txt', '373-0.txt', '380-0.txt', '381-0.txt', '386-0.txt', '387-0.txt', '388-0.txt', '394-0.txt', '395-0.txt', '399-0.txt', '402-0.txt', '415-0.txt', '421-0.txt', '425-0.txt', '426-0.txt', '43-0.txt', '44-0.txt', '441-0.txt', '45-0.txt', '451-0.txt', '462-0.txt', '464-0.txt', '469-0.txt', '47-0.txt', '471-0.txt', '479-0.txt', '492-0.txt', '493-0.txt', '496-0.txt', '497-0.txt', '500-0.txt', '501-0.txt', '503-0.txt', '506-0.txt', '507-0.txt', '51-0.txt', '524-0.txt', '527-0.txt', '528-0.txt', '530-0.txt', '539-0.txt', '540-0.txt', '543-0.txt', '547-0.txt', '555-0.txt', '556-0.txt', '564-0.txt', '570-0.txt', '580-0.txt', '581-0.txt', '588-0.txt', '589-0.txt', '60-0.txt', '614-0.txt', '620-0.txt', '621-0.txt', '627-0.txt', '638-0.txt', '640-0.txt', '641-0.txt', '642-0.txt', '644-0.txt', '645-0.txt', '647-0.txt', '648-0.txt', '649-0.txt', '650-0.txt', '651-0.txt', '652-0.txt', '653-0.txt', '654-0.txt', '659-0.txt', '671-0.txt', '675-0.txt', '677-0.txt', '678-0.txt', '687-0.txt', '689-0.txt', '693-0.txt', '695-0.txt', '696-0.txt', '698-0.txt', '70-0.txt', '700-0.txt', '705-0.txt', '711-0.txt', '718-0.txt', '719-0.txt', '74-0.txt', '751-0.txt', '752-0.txt', '76-0.txt', '764-0.txt', '766-0.txt', '767-0.txt', '770-0.txt', '773-0.txt', '774-0.txt', '775-0.txt', '780-0.txt', '782-0.txt', '783-0.txt', '786-0.txt', '787-0.txt', '788-0.txt', '789-0.txt', '790-0.txt', '794-0.txt', '804-0.txt', '805-0.txt', '807-0.txt', '809-0.txt', '818-0.txt', '82-0.txt', '821-0.txt', '824-0.txt', '829-0.txt', '832-0.txt', '834-0.txt', '836-0.txt', '837-0.txt', '839-0.txt', '840-0.txt', '854-0.txt', '859-0.txt', '86-0.txt', '860-0.txt', '863-0.txt', '864-0.txt', '865-0.txt', '872-0.txt', '873-0.txt', '876-0.txt', '882-0.txt', '883-0.txt', '885-0.txt', '886-0.txt', '887-0.txt', '897-0.txt', '899-0.txt', '903-0.txt', '904-0.txt', '905-0.txt', '912-0.txt', '913-0.txt', '914-0.txt', '916-0.txt', '917-0.txt', '918-0.txt', '935-0.txt', '938-0.txt', '940-0.txt', '942-0.txt', '945-0.txt', '95-0.txt', '963-0.txt', '965-0.txt', '966-0.txt', '967-0.txt', '968-0.txt', '969-0.txt', '974-0.txt', '977-0.txt', '98-0.txt', '980-0.txt', '985-0.txt', '993-0.txt']
Average release year: 2003.54
Most common release year: [('1999', 138)]
Ratio of English to Nonenglish books: 125.83
Book with most dialogue: 1184-0.txt, "The Count of Monte Cristo" by Alexandre Dumas, père
Longest book: 135-0.txt, "Les Misérables" by Victor Hugo
================================================================
```
