---
layout: post
title: "Python script to generate blog post filenames from titles"
date: 2021-02-05
background: '/img/bg-posts-black-blur.jpg'
---

Jekyll makes it easy to publish posts. The url for the post is automatically generated from the file name. 
The date and time is extracted too. We, however, need to provide a filename for the markdown file which 
becomes its URL. 
The following set of python commands will generate the filename from the post title and save us the 
trouble of typing the long filename. We are running the commands in an interpreter but this can be 
automated into a script.

```python
Python 3.8.5 (default, Jul 28 2020, 12:59:40) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import re
>>> import os
>>> os.listdir()
['index.html', '.jekyll-cache', 'jekyll-theme-clean-blog.gemspec', '.idea', 'README.md', 'screenshot.png', 'gulpfile.js', 'about.md', '_sass', 'assets', '_config.yml', '_includes', '_layouts', '.gitignore', 'Gemfile.lock', 'posts', '_site', 'LICENSE', '.git', '_posts', 'bin', 'contact.html', 'img', 'Gemfile', 'package-lock.json', '.travis.yml', 'package.json']
>>> os.chdir('_posts')
>>> os.listdir()
['2020-01-26-dinosaurs.html', '2021-02-05-post1.md', '.ipynb_checkpoints', '2020-02-04-getting-attendance-from-ringcentral-chat-messages.md', 'renameposts.ipynb']
>>> os.listdir()[1]
'2021-02-05-post1.md'
>>> f = open(os.listdir()[1])
>>> while True:
...     line = f.readline()
...     title = re.findall('title: \"(.*?)\"', line)
...     if len(title) > 0:
...             print(re.sub(' ', '-', title[0].lower()))
...             break
... 
python-script-to-read-generate-blog-post-filenames-from-titles
>>> f.close()
```

## Explanation 
```python
import os
os.chdir('_posts')
```
changes to the directory containing the posts.
```python
os.listdir()
```
lists the file name so that we can select the correct markdown file containing the post.
```python
f = open(os.listdir()[1])
```
opens the file. In this case we chose the file `2021-02-05-post1.md` which doesn't have proper name yet.
```python
while True:
```
will keep looping till we find the lines containing the data for `title` and `date` and then it will `break`.
```python
line = f.readline()
```
reads the next line into a variable `line`.
```python
title = re.findall('title: \"(.*?)\"', line)
```
Here, we use the regex pattern match using the `re` library. 
`re.findall()` searches for the regular expression (regex) pattern `'title: \"(.*?)\"'` and every time it 
finds `title: "<your title>"` it extracts `<your title>`. If re() doesn't find anything, it returns an empty list. 
```python
if len(title) > 0:
```
if the list returned by `re.findall()` is empty then the line does not contain the `title` and we move on.
```python
print(re.sub(' ', '-', title[0].lower()))
```
if the list returned by `re.findall()` is not empty, then we have the title in the first element of 
the `title` variable, `title[0]`. 
We first convert it to lowercase `title[0].lower()` and then substitute the spaces in the title with 
hyphens using `re.sub()`. `re.sub()` performs substitution of regex pattern using the format 
`re.sub(pattern to replace, replace pattern, string)`.
Once we found the title and extracted it, we break out of the loop. 


## The full script
The following script gets the full blog title from both the date and the title.

```python
#!/bin/env python
import re
import sys

fname = sys.argv[1]
f = open(fname)

while True:
    line = f.readline()
    title = re.findall('title: \"(.*?)\"', line)
    if len(title) > 0:
        title = re.sub(' ', '-', title[0].lower())
        break

while True:
    line = f.readline()
    postdate = re.findall('date: (\d\d\d\d-\d\d-\d\d)', line)
    if len(postdate) > 0:
        postdate = re.sub(' ', '-', postdate[0].lower())
        break
    
fullfilename = postdate+'-'+title+'.md'
print(fullfilename)
f.close()
```

Running the script on our sample markdown file with the following content
```markdown
---
layout: post
title: "Python script to read generate blog post filenames from titles"
date: 2020-02-05
background: '/img/posts/01.jpg'
---
```

will generate the following filename.
```bash
2020-02-05-python-script-to-read-generate-blog-post-filenames-from-titles.md
```


You can modify this script to accept the current filename as an argument (using argparse for example).
We leave that as an exercise for the reader.