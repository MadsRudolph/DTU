---
course: "<% tp.system.prompt("Course code") %>"
course-name: "<% tp.system.prompt("Course name") %>"
type: lecture-note
week: <% tp.system.prompt("Week number") %>
date: <% tp.date.now("YYYY-MM-DD") %>
tags:
  - <% tp.system.prompt("Short tag") %>
  - lecture
---
# <% tp.file.title %>

> [!info] Lecture Information
> **Course:**
> **Date:** <% tp.date.now("YYYY-MM-DD") %>
> **Topic:**

---

## Key Concepts



---

## Notes



---

## Summary

> [!tldr] Key Takeaways
> -
