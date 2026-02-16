---
course: "62711"
course-name: "Digital Systems Design"
type: workflow
tags: [DSD, workflow]
---
# Team Repo Workflow

The shared team repo lives at `team/` as a git submodule pointing to:
https://github.com/gigurd/Design-of-digital-systems-62711

## First-Time Setup (after cloning DTU repo)

```
git submodule update --init
```

## Day-to-Day Workflow

### Pull team changes

```bash
cd "4. Semester/Digital Systems Design/team"
git pull
cd ../../..
git add "4. Semester/Digital Systems Design/team"
git commit -m "Update team submodule"
```

### Make changes to team code

```bash
cd "4. Semester/Digital Systems Design/team"
# edit files...
git add -A
git commit -m "Your message"
git push
```

Then update the submodule pointer in DTU repo:

```bash
cd ../../..
git add "4. Semester/Digital Systems Design/team"
git commit -m "Update team submodule"
git push
```

## Repo Structure

```
team/
└── PWA/                         <- Vivado project (PWA - ALU/DataPath)
    ├── Nexys_4_DDR_Master.xdc   <- Board constraint file
    ├── PWA.xpr                  <- Vivado 2025.2 project file
    └── PWA.srcs/sources_1/new/
        └── TOP_MODUL.vhd       <- Top-level entity (skeleton)
```

## Vivado Project

- **Board:** Nexys 4 DDR (Artix-7 xc7a100t)
- **Vivado:** 2025.2
- **Top module:** TOP_MODUL

Open the project in Vivado:

```
File → Open Project → team/PWA/PWA.xpr
```

---

> [!nav]
> &nbsp;
>
> [[62711 Digital Systems Design|62711 Home]]
>
> &nbsp;
