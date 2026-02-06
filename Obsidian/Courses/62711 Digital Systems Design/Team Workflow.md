# Team Repo Workflow

The shared team repo lives at `team/` as a git submodule pointing to:
https://github.com/MadsRudolph/digital-systems-design

## First-Time Setup (after cloning DTU repo)

```bash
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

### Add a collaborator

```bash
gh repo edit MadsRudolph/digital-systems-design --add-collaborator <github-username>
```

## Repo Structure

```
team/
├── Adder_Test/          <- Vivado projects (source + TCL scripts only)
│   ├── create_project.tcl
│   ├── src/
│   └── sim/
└── VHDL/
    ├── Sources/         <- Shared VHDL source files
    └── Constraints/     <- Board constraint files (.xdc)
```

## Vivado Projects

Vivado generated files (`.xpr`, `.cache/`, `.sim/`, `.runs/`) are gitignored.
To open a project, source its TCL script in the Vivado Tcl Console:

```tcl
source {C:/Users/Mads2/digital-systems-design/Adder_Test/create_project.tcl}
```
