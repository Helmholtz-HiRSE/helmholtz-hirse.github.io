---
layout: sub_series
title: "Summer of Testing"
permalink: /series/summer_of_testing/
---


# Summer of Testing

All events of the Summer of Testing series are listed here.

<ul>
  {% for event in site.summer_of_testing %}
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