This is a readme file for the project.
The project was coded in python version 3.7
The report is stored in REPORT.pdf file. Please have a look at it.

Run instructions:
To test the code:
1) Open UI.py file.
2) Run this file (Note: If the new window doesn't open up, run this file again).
3) In the text box type your query.
4) Click on "Search UIC".
5) To view more results, click on "Show more results".

There are 5 python files that implement the search engine,i.e. UI.py, tfidf.py, tfidf_doc.py, Web.py and Pagerank.py.

If you want to run the scraper:
- Open the web file.
- Change the file location to your choice.(This is specified by a comment in the code)
- Set the number of pages you want to scrape.
- Run the file.

If you want to see the tfidf calculation:
- Open tfidf_doc.py.
- Change the file location to where data folder is.(This is specified by a comment in the code)
- Run the file.
Note: This file may take 7-10 minutes to run.

Functionality of each .py file:
Web.py: This will scrape the web. 3500 pages in 1 and a half hour.
tfidf_doc.py: This will calculate the tfidf score for the scraped pages.
tfidf.py: This will calculate the tfidf score for the query.
Pagerank.py: This will implement the pagerank algorithm.
UI.py: This will launch the User interface to test the code.
