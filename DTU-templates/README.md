# DTU templates & brand assets

Reusable DTU corporate-identity assets for **any future report or poster**. Pulled from
the official DTU poster template (Overleaf project, see source below).

## Source
- **Overleaf project:** `https://www.overleaf.com/project` → git remote
  `https://git.overleaf.com/6a25b61d3d768ccc0ee43f99`
  (clone needs your personal Overleaf git token from Account Settings → Git integration)
- Original `dtuposter` class by Jorrit Wronski (DTU Mechanical Engineering), 2011–2014.

## What's here
| Path | Contents |
|------|----------|
| `external/dtucolours.tex` | **Official DTU colour definitions** (the source of truth) |
| `external/dtuposter.cls` | The DTU poster LaTeX class (CI-compliant posters) |
| `external/dtu_dep_logo/` | 90 department logos (PDF) — `_a`=stacked, `_b`=horizontal, `_uk`=English |
| `external/dtu_dep_name_logo/`, `external/dtu_logo/`, `external/dtu_frise/` | DTU wordmark / corporate logo / wave ("frise") logos |
| `external/dtu_background/` | DTU background patterns (fiber, nano, pink) |
| `poster-example.tex` | The dtuposter usage example |

## DTU colours (from `dtucolours.tex`)
Primary: **dtured `#990000`** (rgb 0.60/0/0) · **dtugrey `#999999`**
Poster background: **dtucoolgrey `#969491`** (rgb 0.59/0.58/0.57)
Secondary: dtuyellow `#FFCC00` · dtuorange `#FF9900` · dtulightred `#FF0000` ·
dtupurple `#CC3399` · dtuviolet `#660099` · dtudarkblue `#3366CC` ·
dtulightblue `#33CCFF` · dtulightgreen `#99CC33` · dtudarkgreen `#66CC00`

## Using these
- **LaTeX report/poster:** `\input` or copy `external/dtucolours.tex` for the colours;
  for posters use `dtuposter.cls` (see `poster-example.tex`).
- **Figma / other tools:** use the hex values above. The DTU Electrical Engineering
  logo we used on the 62768 poster is `external/dtu_dep_logo/tex_dtu_elektro_b_uk.pdf`
  (convert to PNG with `pdftocairo -png -transp -singlefile -r 600 <file>.pdf out`).

## Related project assets
- **62768 report skeleton (LaTeX):** `4. Semester/Electrical Energy Systems/team/report/`
- **62768 poster (Figma):** https://www.figma.com/design/hYpFMnofNsuwd1HV1WFXd0
