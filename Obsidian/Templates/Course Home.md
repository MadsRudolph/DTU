---
course: "<% tp.system.prompt("Course code (e.g. 34315)") %>"
course-name: "<% tp.system.prompt("Course name") %>"
type: home
cssclass: course-home
tags:
  - <% tp.system.prompt("Short tag (e.g. IoT, PE, LCD)") %>
  - home
---
# <% tp.file.title %>

> [!info] Course Information
> **Course:**
> **Semester:**
> **Lecturers:**
> **Textbook:**
> **Exam:**
> **Teaching:**

> [!tip] Quick Links
> - [DTU Course Page]()

---

## Roadmap

| Wk | Date | Lec | Topic | Reading | Done |
|---|---|---|---|---|---|
| | | | | | - [ ] |

---

## Lecture Notes

```dataview
TABLE date AS "Date", week AS "Week"
FROM "<% tp.file.folder(true) %>/Lecture Notes"
WHERE type = "lecture-note"
SORT week ASC
```

---

## Exercises & Quizzes

```dataview
TABLE type AS "Type", date AS "Date"
FROM "<% tp.file.folder(true) %>/Exercises"
WHERE type = "exercise" OR type = "quiz"
SORT date ASC
```

---

## Formula Sheets & References

```dataview
TABLE date AS "Date"
FROM "<% tp.file.folder(true) %>"
WHERE type = "formula"
SORT file.name ASC
```

---

## Literature & Resources



---

## Quick Reference


