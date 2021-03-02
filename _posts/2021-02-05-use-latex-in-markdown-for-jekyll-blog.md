---
layout: post
title: "Use Latex in markdown for Jekyll blog"
date: 2021-02-05
background: '/img/bg-posts-black-blur.jpg'
---
$$\LaTeX$$ is very convenient is writing complex equations. It is an indispensable tool for 
scientists. However, while publishing a static Jekyll blog it is difficult to enter Greek symbols.
This is because Jekyll doesn't come with native support to render $$\LaTeX$$. However, MathJax is 
widely available, and we can add math rendering support to our webpages using MathJax. To add 
MathJax support to our blog we will need to add the following code snippet to every HTML file in the 
`/_layouts` folder. The code goes before the HTML tags.

```html
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      skipTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
      inlineMath: [['$','$'], ['\\(','\\)']],
      processEscapes: true
    },
    TeX: {
      equationNumbers: {
        autoNumber: "AMS"
      }
    }
  });
</script>

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-AMS_CHTML">
</script>
```

See an example of the 
[usage](https://github.com/j3soon/minimal-mistakes-template/blob/master/_includes/scripts.html).

References:
1. [LaTeX Notes & MathJax in Jekyll](http://rangerway.com/way/latex-note-and-jekyll)