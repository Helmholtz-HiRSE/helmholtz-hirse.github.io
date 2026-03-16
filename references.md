---
layout: news
title: References
---

# References

This page lists RSE-related publications curated by the HiRSE community.
It covers research software engineering best practices, FAIR software principles, sustainable software development, and related topics.

You can download the full bibliography as a BibTeX file:
[Download .bib file](/assets/data/rse_publications.bib){: .btn .btn-outline-secondary .btn-sm}

---

{% assign refs = site.data.references %}
{% assign years = refs | map: "year" | uniq | sort | reverse %}
{% assign chart_years = years | reverse %}

## Publications by Year

<div class="mb-3">
{% for year in years %}<a href="#year-{{ year }}" class="btn btn-sm btn-outline-primary me-1 mb-1">{{ year }}</a>
{% endfor %}
</div>

<canvas id="pubsChart" style="max-height:260px;" aria-label="Publications per year bar chart" role="img"></canvas>

---

{% for year in years %}
<h3 id="year-{{ year }}">{{ year }}</h3>
{% assign year_refs = refs | where: "year", year %}
<ul class="list-unstyled">
{% for ref in year_refs %}
<li class="mb-3">
  <strong>{{ ref.title }}</strong><br>
  {% assign author_list = ref.authors | join: ", " %}
  {{ author_list }}<br>
  {% assign venue = "" %}
  {% if ref.journal %}{% assign venue = ref.journal %}{% elsif ref.booktitle %}{% assign venue = ref.booktitle %}{% endif %}
  {% if ref.volume %}{% assign venue = venue | append: ", " | append: ref.volume %}{% endif %}
  {% if ref.number %}{% assign venue = venue | append: "(" | append: ref.number | append: ")" %}{% endif %}
  {% if ref.pages %}{% assign venue = venue | append: ", pp. " | append: ref.pages %}{% endif %}
  <em>{% if venue != "" %}{{ venue }}, {% endif %}{{ ref.year }}</em>
  {% if ref.doi %}<br><a href="https://doi.org/{{ ref.doi }}" target="_blank" rel="noopener">DOI: {{ ref.doi }}</a>{% elsif ref.url %}<br><a href="{{ ref.url }}" target="_blank" rel="noopener">{{ ref.url }}</a>{% endif %}
</li>
{% endfor %}
</ul>
{% endfor %}

<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
<script>
(function () {
  var years = [{% for year in chart_years %}{{ year }}{% unless forloop.last %},{% endunless %}{% endfor %}];
  var counts = [{% for year in chart_years %}{% assign n = refs | where: "year", year | size %}{{ n }}{% unless forloop.last %},{% endunless %}{% endfor %}];
  var ctx = document.getElementById('pubsChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: years,
      datasets: [{
        label: 'Publications',
        data: counts,
        backgroundColor: 'rgba(141, 180, 39, 0.7)',
        borderColor: 'rgba(141, 180, 39, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Publications per Year' }
      },
      scales: {
        y: { beginAtZero: true, ticks: { stepSize: 1 } }
      }
    }
  });
}());
</script>
