---
title: "{{ replace (substr .File.ContentBaseName 11) "-" " " | title }}"
date: {{ .Date }}
slug: "{{ substr .File.ContentBaseName 11 }}"
categories: ["daily"]
draft: true

# TODO(Samarthya): decide what a "trophy" daily entry records.
# Add 3-6 front-matter fields below. Ideas to choose from or replace:
#   kind: ""          # learned | built | read | fitness | travel | hobby ...
#   mood: ""          # a word or emoji
#   effort: ""        # e.g. "30m", "2h"
#   links: []         # repo / article / photo album
#   tags: []          # reuse tech tags (golang, k8s) so entries link to related posts
---

<!-- What did I do today, and why does it count? -->
