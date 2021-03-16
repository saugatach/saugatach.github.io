---
layout: post
title: "Using BeautifulSoup to scrape prices from grocery receipts"
date: 2021-03-15
background: '/img/bg-posts-black-blur.jpg'
---


# Demonstration of BeautifulSoup to scrape data
We show to how to convert Fry's HTML receipts into tables which can be saved as csv files. If you 
are one who likes to keep detailed records of their expenses, then this script is what you need. 
The idea is to scrape data from an HTML file using BeautifulSoup, then collect that into a pandas 
dataframe. But first, we need to grab the HTML receipt.

### Get HTML receipt
To grab the Fry's receipt go to Purchases, then click on **See order details**. 
After the receipt page loads, click on **View receipt**. After that page loads, save that page, 
and keep the default name which should be ```Fry’s Food Stores.html```. 
Copy this file to the same location as your script, and execute the following in a 
Jupyter notebook.

```python
pathofhtml = 'Fry’s Food Stores.html'

if os.path.exists(pathofhtml):
    print("File Exists")
else:
    print("File does not exist")
f = open(pathofhtml)
htmldata = f.read()
f.close()
```

Now, we convert the HTML data to a BeautifulSoup object. BeautifulSoup allows for a streamlined parsing of
HTML data from webpages. Earlier, we have saved the Fry's receipt as an HTML file, which we load 
as a BeautifulSoup object.

```python
pagesoup = bs(htmldata)
```

This command creates the BeautifulSoup object, which allows for simple search functions to extract
data with specific HTML tags or (as in our case) CSS tags. 

The trick is to match the data with the correct tag. We open the HTML file in a web browser, 
and then right-click on the table and select Inspect.

![drawing](/img/posts/frys-scrape-screenshot.png)

In the developer console, we see that each row of the data is contained within multiple CSS tags. 
```flex justify-between items-center px-8 -mx-4``` contains the rows, and 
```kds-Text--s kds-Text--bold``` contains the data from columns.

We first search for all HTML elements for ```flex justify-between items-center px-8 -mx-4```. That gives 
us the rows. We then iterate over the rows and scrape out the columns. There are only 2 columns per row.
So we use that knowledge to extract the item name and price.

```python
itemlist = []
pricelist = []
class_row = "flex justify-between items-center px-8 -mx-4"
class_col = "kds-Text--s kds-Text--bold"
for x in pagesoup.find_all(class_=class_row):
    data = x.find_all(class_=class_col)
    if len(data) > 0:
        it, price = data[0].text, data[1].text
        itemlist.append(it)
        pricelist.append(price)
df = pd.DataFrame({'item': itemlist, 'price': pricelist})
df
```



item |	price|
-----|-------|
Broccoli - Crowns, 1 ct |	1.29|
Banana, 1 ct |	1.05|
Potatoes - Sweet Yams - Red, 1 ct |	2.93|
Pear - Bosc, 1 ct |	1.31|
Pears - Red Anjou, 1 lb |	2.73|

We pack the items and the prices into separate lists; and at the end, combine the lists to 
generate a dataframe, which we export as a CSV file.

```python
df.to_csv('frys.csv', index=False)
```

### The full code

Here is the full code which does the trick. 

```python
import os
import re
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs

pathofhtml = 'Fry’s Food Stores.html'

if os.path.exists(pathofhtml):
    print("File Exists")
else:
    print("File does not exist")
    exit(-1)

f = open(pathofhtml)
htmldata = f.read()
f.close()

pagesoup = bs(htmldata)
itemlist = []
pricelist = []
class_row = "flex justify-between items-center px-8 -mx-4"
class_col = "kds-Text--s kds-Text--bold"
for x in pagesoup.find_all(class_=class_row):
    data = x.find_all(class_=class_col)
    if len(data) > 0:
        it, price = data[0].text, data[1].text
        itemlist.append(it)
        pricelist.append(price)
df = pd.DataFrame({'item': itemlist, 'price': pricelist})
df.to_csv('frys.csv', index=False)
```

This works as of Mar 15, 2021. If Fry's updates their CSS style files, then the code needs to be updated.
That is the cost of maintaining a scraping library; it needs to be updated often. Hopefully, only the
CSS class names (```class_row``` and ```class_col```) will change. 