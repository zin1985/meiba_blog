---
layout: default
title: 名馬一覧
---

<h1>名馬ブログへようこそ</h1>
<p>このサイトでは実在した名馬たちの魅力を毎日1頭ずつ紹介しています。</p>

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ site.baseurl }}{{ post.url }}">{{ post.date | date: "%Y年%m月%d日" }} - {{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
