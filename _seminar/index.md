---
layout: sub_series
title: "Seminar"
permalink: /series/seminar/
---

# Seminar Series

All events of the Seminar series are listed here.

<ul>
  {% for event in site.seminar %}
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