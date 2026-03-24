---
type: concept
aliases: []
tags:
  - concept
courses: []
---
# <% tp.file.title %>

## Definition



---

## Key Equations



---

## Where It Appears

```dataview
LIST
FROM "Courses" OR "Archive"
WHERE contains(file.outlinks, this.file.link) OR contains(tags, this.file.tags)
SORT file.folder ASC
```

---

## Related Concepts

