---
course: "34315"
course-name: "Internet of Things"
type: home
cssclass: course-home
tags: [IoT, home]
---
# 34315 Internet of Things

> [!info] Course Information
> **Course:** 34315 Internet of Things - Application and Infrastructure Implementation
> **Semester:** Spring 2026 (4th semester)
> **Lecturers:** Sarah Ruepp (responsible), Henrik, Anas, Erik + TAs (Reza, Oscar, Laurits, Ahmed)
> **ECTS:** 5
> **Exam:** Project presentation (mandatory) + report hand-in
> **Teaching:** Lectures (Wed 9:10-12:00) + exercises + project work
> **Prerequisites:** Basic programming, electronics fundamentals

> [!tip] Quick Links
> - [DTU Course Page](https://kurser.dtu.dk/course/34315)
> - [LPWAN Book](https://findit.dtu.dk/en/catalog/2525550498)
> - [Arduino Book](https://findit.dtu.dk/en/catalog/5cd73c9d5eee4800231e3959)
> - [[DTU Study Path#4.3 34315 -- Internet of Things - Application and Infrastructure Implementation|Study path context]]

---

## Roadmap

| Wk | Date | Lec | Topic | Reading | Done |
|---|---|---|---|---|---|
| 6 | 05.02 | 1 | Introduction, IoT intro & microcontrollers | LPWAN Ch. 1-2, Arduino Ch. 1-2 | x |
| 7 | 12.02 | 2 | IoT Communication background | Arduino Ch. 3-4, Data Comm Networks 4.5 & 5.5 | x |
| 8 | 19.02 | 3 | Basic electronics | Arduino Ch. 5-6, Electronics lecture | |
| 9 | 26.02 | 4 | Exercises (cont.) | Arduino Ch. 7-8-9-10 | |
| 10 | 05.03 | 5 | IoT security | Security paper | |
| 11 | 12.03 | 6 | LP-WAN communication & IoT clouds | LPWAN Ch. 3, 4, 6, 7 | |
| 12 | 19.03 | 7 | Telia guest lecture + 3D design workshop | Workshop guidelines | |
| 13 | 26.03 | 8 | Introduction to project work | Project guidelines | |
| | 02.04 | | *EASTER BREAK* | | |
| 14 | 09.04 | 9 | Project work (guest lecture NTT Data) | | |
| 15 | 16.04 | 10 | Project work | | |
| 16 | 23.04 | 11 | Project work | | |
| 17 | 30.04 | 12 | Project work | | |
| 18 | 07.05 | 13 | **Project presentation** (8:00-13:00, mandatory) | | |
| | 17.05 | | **Report hand-in** | | |

> [!warning] Deadlines
> - **Ex. 8** -- Hand-in Wednesday 25 Feb
> - **Ex. 13** -- Hand-in Wednesday 11 March
> - **Project presentation** -- 07 May (mandatory attendance)
> - **Project report** -- 17 May

---

## Why This Course

> [!abstract] Relevance to Audio Profile
> This course bridges hardware and software for connected audio products:
> - Embedded systems for amplifier control
> - IoT protocols for smart speakers and multi-room audio
> - Integration with Home Assistant and similar platforms
> - Complements analog (34655) and power (34620) courses

---

## Lecture Notes

```dataview
TABLE date AS "Date", week AS "Week"
FROM "Courses/34315 Internet of Things/Lecture Notes"
WHERE type = "lecture-note"
SORT week ASC
```

---

## Exercises

```dataview
TABLE type AS "Type", date AS "Date"
FROM "Courses/34315 Internet of Things/Exercises"
WHERE type = "exercise" OR type = "quiz"
SORT date ASC
```

> [!tip] Exercise Sheets & Solutions
> - [[34315_Exercise 1.pdf|Exercise 1 -- Morse Code (Arduino)]]
> - [[34315_Intro to Ex 2-7.pdf|Exercises 2-7 -- Communication & WiFi]]
> - [[Ex 2_4 Solution.pdf|Solution Ex 2-4]]
> - [[Ex 5_7 Solution.pdf|Solution Ex 5-7]]
> - [[34315_Intro to Ex 8.pdf|Exercise 8 -- Basic Electronics]]
> - [[34315 Simons game specifications.pdf|Simon's Game Specifications]]

> [!tip] Code Examples (Exercise 1)
> Arduino sketches in `4. Semester/Internet of Things/Arduino/`:
> - `exercise1MorseCodeSimple.ino` -- Simple morse code
> - `exercise1MorseCodeForLoop.ino` -- Morse code with for-loops
> - `exercise1MorseCodeFunctions.ino` -- Morse code with functions

---

## Slides

- [[Course intro_iot_microcontrollers.pdf|Lecture 1 -- Course Intro, IoT & Microcontrollers]]
- [[260211 Wireless lecture.pdf|Lecture 2 -- Wireless Communication]]
- [[34365- Basic-Electronics-IoT.pdf|Lecture 3 -- Basic Electronics for IoT]]

---

## Literature & Resources

### Course Materials
- [[34315_Lecture plan_2026_v1.pdf|Lecture Plan 2026]]
- [LPWAN Book](https://findit.dtu.dk/en/catalog/2525550498)
- [Arduino Book](https://findit.dtu.dk/en/catalog/5cd73c9d5eee4800231e3959)
- [Data Communication Networks](https://findit.dtu.dk/en/catalog/5d30955ad9001d01772b3078) (Ch. 4.5 & 5.5)
- [IoT Security Paper](https://www.sciencedirect.com/science/article/pii/S2214212617302934)

### Guides
- [[Beginner_c_For_Arduino.pdf|Beginner C for Arduino]]

---

## Quick Reference

> [!tip] Useful Commands
> ```
> // Arduino IDE: compile & upload
> Ctrl+R  -- Verify/Compile
> Ctrl+U  -- Upload to board
> Ctrl+Shift+M -- Serial Monitor
> ```
