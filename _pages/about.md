---
permalink: /
title: "About"
excerpt: "About me"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

I am a Ph.D. student at KAIST School of Computing, advised by [Alice Oh](https://aliceoh9.github.io/).

## Recent Publications

{% for post in site.publications reversed limit:5 %}
{% include archive-short.html %}
{% endfor %}

## Education

- M.S. in School of Computing, *KAIST*, 2019.08
- B.S. in School of Computing, *KAIST*, 2018.02

## Teaching Experiences

- *CS206 Data Structure*, KAIST  
  Teaching Assistant (Spring 2018)  
  Head Teaching Assistant (Fall 2018)
- *CS492C Machine Learning and Natural Language Processing*, KAIST  
  Head Teaching Assistant (Fall 2019)
