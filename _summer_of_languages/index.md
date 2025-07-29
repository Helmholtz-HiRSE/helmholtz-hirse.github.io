---
layout: sub_series
title: "Summer of Languages"
permalink: /series/summer_of_languages/
---

# Summer of Languages

All events of the Summer of Languages series are listed here.

<ul>
  {% for event in site.summer_of_languages %}
    {% unless event.name == "index.md" %}
      <li class="news">
        <span class="small">
          {{ event.date | date: "%B %d, %Y" }}
          {% if event.location %}
            &nbsp; ({{ event.location }})
          {% endif %}
        </span>
        <br>
        <strong><a href="{{ event.url }}">{{ event.title }}</a></strong>
        {% if event.excerpt %}
          <p>{{ event.excerpt }}</p>
        {% endif %}
      </li>
    {% endunless %}
  {% endfor %}
</ul>