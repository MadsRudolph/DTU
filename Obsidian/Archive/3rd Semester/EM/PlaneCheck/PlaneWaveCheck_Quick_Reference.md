# PlaneWaveCheck - Quick Reference Card

> 📋 **One-page cheat sheet for exams**

**Navigation:** [Master Index](PlaneWaveCheck_MASTER_INDEX.md) · [Quick Start](PlaneWaveCheck_Quick_Start.md) · [Complete Guide](PlaneWaveCheck_Complete_Guide.md) · [Troubleshooting](PlaneWaveCheck_Troubleshooting.md) · [Exam Examples](PlaneWaveCheck_Exam_Examples.md)

---

## Which Mode?

| Problem Has | Use Mode | Command |
|-------------|----------|---------|
| γ = [j...; ...] explicit | **Maxwell** | `PlaneWaveCheck('maxwell', E0, H0, gamma)` |
| exp(-j(ax+by+cz)) term | **Full** | `PlaneWaveCheck('full', E, H, k)` |

⚠️ **Basic mode CANNOT confirm plane wave - only rule out!**

---

## Full Mode Syntax

```matlab
% Format B: exp(-j...) problems
PlaneWaveCheck('full', E, H, k)         % η = 377 Ω (free space)
PlaneWaveCheck('full', E, H, k, eta)    % custom η
```

## Maxwell Mode Syntax

```matlab
% Format A: γ given explicitly
PlaneWaveCheck('maxwell', E0, H0, gamma)
```

---

## The 4 Conditions

| # | Check | Pass If |
|---|-------|---------|
| 1a | k · E | = 0 |
| 1b | k · H | = 0 |
| 1c | E · H | = 0 |
| 3 | H = (1/η)(k̂ × E) | match |
| 4 | (E × H) · k | > 0 |

**All must pass → Plane wave**  
**Any fails → NOT plane wave**

---

## Extract k from exp term

```
exp(-j(20x + 0y + 10z))
         ↓    ↓    ↓
k = [   20;   0;  10]
```

---

## Common Input Patterns

| Symbol | Meaning | MATLAB |
|--------|---------|--------|
| x̂, î | x unit vector | `[1;0;0]` |
| ŷ, ĵ | y unit vector | `[0;1;0]` |
| ẑ, k̂ | z unit vector | `[0;0;1]` |
| j | √(-1) | `1j` |

**⚠️ ĵ (j-hat) ≠ j (imaginary)**

---

## Quick Examples

### Format B → Full Mode
```matlab
% E = 5ŷ·exp(-j(20x+10z))
E = [0; 5; 0];
H = [0; 0; 1/(120*pi)];
k = [20; 0; 10];
PlaneWaveCheck('full', E, H, k)
```

### Format A → Maxwell Mode
```matlab
% E₀ = [2;0;0], H₀ = [0;-5.3e-3;0], γ = [0;0;j3]
E0 = [2; 0; 0];
H0 = [0; -5.309e-3; 0];
gamma = [0; 0; 1j*3];
PlaneWaveCheck('maxwell', E0, H0, gamma)
```

---

## Output Fields

### Full Mode
```matlab
result.is_plane_wave     % true/false (definitive)
result.cond1_pass        % k·E = 0?
result.cond2_pass        % k·H = 0?
result.cond3_pass        % E·H = 0?
result.cond4_pass        % H = (1/η)(k̂×E)?
result.cond5_pass        % (E×H)·k > 0?
```

### Maxwell Mode
```matlab
result.is_plane_wave     % true/false (definitive)
result.omega_eps         % ωε values (must be >0)
result.omega_mu          % ωμ values (must be >0)
result.eps_pos_ok        % ωε positive?
result.mu_pos_ok         % ωμ positive?
```

### Basic Mode ⚠️
```matlab
result.is_plane_wave     % EMPTY (cannot determine!)
result.orthogonality_pass % true/false
% → Use 'full' mode for definitive answer
```

---

## Common Traps

| Trap | Example | Fix |
|------|---------|-----|
| ĵ = direction | ĵ5 = 5ŷ | `[0;5;0]` not `1j*5` |
| Basic mode | "Says valid" | Use `'full'` for exam |
| Orthogonal but invalid | Q1 type | Use `'maxwell'` mode |
| Forgot k·H | E⊥H but k·H≠0 | Check all 3 dots |

---

## Mode Decision Summary

```
γ given? ───Yes──► 'maxwell'
    │
    No
    │
    ▼
exp term? ──Yes──► 'full'
    │
    No
    │
    ▼
Quick check ────► basic (but CANNOT confirm!)
```

---

**Navigation:** [Master Index](PlaneWaveCheck_MASTER_INDEX.md) · [Quick Start](PlaneWaveCheck_Quick_Start.md) · [Complete Guide](PlaneWaveCheck_Complete_Guide.md) · [Troubleshooting](PlaneWaveCheck_Troubleshooting.md) · [Exam Examples](PlaneWaveCheck_Exam_Examples.md)
