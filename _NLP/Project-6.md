---
title: "Project-6 Web Crawler"
excerpt: "Web Scrawler that scrapes and analyzes company data related to ukraine"
classes: wide
number: 7
last_modified_at: 2023-03-10T16:20:02-05:00
toc: true
toc_label: ""
---

# Project 6 Report

## Top 10 Terms

From the top terms using the term frequency algorithm the most common terms that are relevant to the data being scraped are as follows:

1. Russia 
2. Ukraine
3. Global
4. Conflict
5. Company
6. War
7. Media
8. US
9. Support
10. International

## Knowledge base  

I built the knowledge base around being easily importable as a dataframe with each individual company having their own row and associated data.  

Since there are currently 1,600 companies in the CSV scraping each source URL would've taken an extremely long time so I limited the urls to the top 19 websites that had good usable data.  

As shown below the file has the companies names, summary, comments, dates, sources, donations, source URLs, and for the 19 sites their most and least important words in a 1x2 list format.  

![Unfiltered](https://github.com/Myakubek/myakubek.github.io/blob/master/Documents/ScraperKnowledgeBase.png)

![Filtered](https://github.com/Myakubek/myakubek.github.io/blob/master/Documents/ScraperKnowledgeBaseCondensed.png)
