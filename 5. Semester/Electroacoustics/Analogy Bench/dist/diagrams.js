/* Static circuit drawings placed into <div id="..."> slots in index.html. */
"use strict";

function diagSeriesRLC() {
  const root = document.getElementById("diag-series-rlc"); if (!root) return;
  const mk = (col, src, L, C, R, cap) => `<div class="circuit">${svgWrap(320, 170, [
    VSRC(40, 140, 40, 40, col, src, -1), CK.wire(40, 40, 80, 40), IND(80, 40, 160, 40, col, L), CAP(160, 40, 240, 40, col, C), CK.wire(240, 40, 280, 40), RES(280, 40, 280, 140, col, R, 1), CK.wire(280, 140, 40, 140), CK.gnd(160, 140),
  ].join(""))}<div class="cap">${cap}</div></div>`;
  root.innerHTML = `<div class="tri">${mk(DOMC.el, "v", "L", "C", "R", "v = (jωL + 1/jωC + R)·i")}${mk(DOMC.me, "f", "M<tspan font-size='9' dy='3'>M</tspan>", "C<tspan font-size='9' dy='3'>M</tspan>", "R<tspan font-size='9' dy='3'>M</tspan>", "f = (jωM_M + 1/jωC_M + R_M)·u")}${mk(DOMC.ac, "p", "M<tspan font-size='9' dy='3'>A</tspan>", "C<tspan font-size='9' dy='3'>A</tspan>", "R<tspan font-size='9' dy='3'>A</tspan>", "p = (jωM_A + 1/jωC_A + R_A)·U")}</div>`;
}

function diagTwoTubes() {
  const root = document.getElementById("diag-two-tubes"); if (!root) return;
  root.innerHTML = `<div class="circuit">${svgWrap(560, 190, [
    ISRC(40, 150, 40, 50, DOMC.ac, "U", -1), CK.wire(40, 50, 80, 50), IND(80, 50, 190, 50, DOMC.ac, "M_A1 wide tube (18.0)"), CK.dot(220, 50), CK.wire(190, 50, 260, 50),
    CAP(220, 50, 220, 150, DOMC.ac, "C_A box (1.65×10⁻⁷)", 1), IND(260, 50, 420, 50, DOMC.ac, "M_A2 narrow tube (1803)"), CK.wire(420, 50, 470, 50), CK.wire(470, 50, 470, 150), CK.wire(470, 150, 40, 150), CK.gnd(300, 150),
    CK.label(220, 36, "node p", DOMC.ink2, "middle", 11), CK.label(490, 100, "U₂ → out", DOMC.ink2, "start", 11),
    CK.note(280, 182, "Problem 2.3: driven from the wide tube — resonance (Z_in → 0) at 92.8 Hz, anti-resonance (p peaks) at 9.2 Hz"),
  ].join(""))}</div>`;
}

function diagChain() {
  const root = document.getElementById("diag-chain"); if (!root) return;
  const box = (x, col, title, a, b) => `<rect x="${x}" y="30" width="170" height="96" rx="6" fill="${col.replace(")", "-soft)")}" stroke="${col}" stroke-width="1.5"/><text x="${x + 85}" y="56" text-anchor="middle" font-family="var(--font-display)" font-size="17" font-weight="600" fill="${col}">${title}</text><text x="${x + 85}" y="80" text-anchor="middle" font-family="var(--font-mono)" font-size="12" fill="var(--ink)">across: ${a}</text><text x="${x + 85}" y="100" text-anchor="middle" font-family="var(--font-mono)" font-size="12" fill="var(--ink)">through: ${b}</text>`;
  const arrow = (x, top, bot) => `<path d="M${x} 62 h60" stroke="var(--ink-2)" stroke-width="1.5" fill="none"/><path d="M${x + 52} 56 l8 6 -8 6" fill="none" stroke="var(--ink-2)" stroke-width="1.5"/><path d="M${x + 60} 96 h-60" stroke="var(--ink-2)" stroke-width="1.5" fill="none"/><path d="M${x + 8} 90 l-8 6 8 6" fill="none" stroke="var(--ink-2)" stroke-width="1.5"/><text x="${x + 30}" y="52" text-anchor="middle" font-family="var(--font-mono)" font-size="11.5" fill="var(--ink)">${top}</text><text x="${x + 30}" y="112" text-anchor="middle" font-family="var(--font-mono)" font-size="11.5" fill="var(--ink)">${bot}</text>`;
  root.innerHTML = `<div class="circuit">${svgWrap(640, 150, [
    box(10, "var(--el)", "Electrical", "voltage v", "current i"), arrow(180, "f = Bl·i", "v = Bl·u"),
    box(240, "var(--me)", "Mechanical", "velocity u", "force f"), arrow(410, "U = S·u", "f = S·p"),
    box(470, "var(--ac)", "Acoustical", "pressure p", "vol. velocity U"),
    CK.note(320, 142, "a transducer is a pair of controlled sources — one per direction — with one constant: Bl for a voice coil, S for a diaphragm"),
  ].join(""))}</div>`;
}

function diagDynMic() {
  const root = document.getElementById("diag-dynmic"); if (!root) return;
  root.innerHTML = `<div class="circuit">${svgWrap(760, 210, [
    // acoustic loop (impedance analogy)
    VSRC(30, 160, 30, 50, DOMC.ac, "p_i", -1), CK.wire(30, 50, 60, 50), IND(60, 50, 140, 50, DOMC.ac, "M_A1"), CK.wire(140, 50, 160, 50),
    DEPI(160, 50, 240, 50, DOMC.ac, "U = S_D·u_D"), CK.wire(240, 50, 250, 50), RES(250, 50, 330, 50, DOMC.ac, "R_AF felt"), CK.wire(330, 50, 350, 50), CAP(350, 50, 350, 160, DOMC.ac, "C_AB", 1), CK.wire(350, 160, 30, 160), CK.gnd(190, 160),
    CK.label(150, 36, "p_f", DOMC.ink2, "middle", 11), CK.label(250, 36, "p_b", DOMC.ink2, "middle", 11),
    CK.note(190, 190, "acoustical — impedance analogy", DOMC.ac),
    // mechanical node (mobility)
    DEPI(400, 160, 400, 50, DOMC.me, "", -1), CK.label(376, 100, "f = S_D(p_f − p_b)", DOMC.me, "end", 11), CK.wire(400, 50, 590, 50),
    CAP(450, 50, 450, 160, DOMC.me, "M_MD", 1), IND(505, 50, 505, 160, DOMC.me, "C_MS", 1), RES(560, 50, 560, 160, DOMC.me, "1/R_MS", 1), CK.wire(400, 160, 590, 160), CK.gnd(480, 160),
    CK.dot(450, 50), CK.dot(505, 50), CK.dot(560, 50), CK.label(495, 36, "node u_D", DOMC.ink2, "middle", 11),
    CK.note(495, 190, "mechanical — mobility analogy", DOMC.me),
    // electrical
    DEPV(630, 160, 630, 50, DOMC.el, "", -1), CK.label(626, 100, "Bl·u_D", DOMC.el, "end", 11), CK.wire(630, 50, 650, 50), RES(650, 50, 720, 50, DOMC.el, "R_E"), CK.wire(720, 50, 740, 50), RES(740, 50, 740, 160, DOMC.el, "R_L", 1), CK.wire(740, 160, 630, 160), CK.gnd(685, 160), CK.dot(740, 50), CK.label(752, 42, "e", DOMC.el, "start", 12),
    CK.note(690, 190, "electrical", DOMC.el),
  ].join(""))}<div class="cap">the three domains of a dynamic pressure microphone, wired with the controlled sources of lecture 4 · the reaction Bl·i back on node u_D is drawn in the full model, dropped here for space</div></div>`;
}

function diagCondNorton() {
  const root = document.getElementById("diag-cond-norton"); if (!root) return;
  root.innerHTML = `<div class="two"><div class="circuit">${svgWrap(320, 170, [
    CAP(60, 140, 60, 40, DOMC.el, "C_E0", -1), CK.wire(60, 40, 200, 40), DEPI(200, 40, 200, 140, DOMC.el, "(E·C_E0/x₀)·u", 1), CK.wire(200, 140, 60, 140), CK.gnd(130, 140), CK.dot(60, 40), CK.label(130, 28, "e (electrical side)", DOMC.ink2, "middle", 11),
  ].join(""))}<div class="cap">e = i/(jωC_E0) + (E/jωx₀)·u  →  the 1/jω moved into C_E0</div></div><div class="circuit">${svgWrap(320, 170, [
    IND(60, 140, 60, 40, DOMC.me, "C_M", -1), CK.wire(60, 40, 200, 40), DEPI(200, 40, 200, 140, DOMC.me, "(E·C_M/x₀)·i", 1), CK.wire(200, 140, 60, 140), CK.gnd(130, 140), CK.dot(60, 40), CK.label(130, 28, "f (mechanical side, mobility)", DOMC.ink2, "middle", 11),
  ].join(""))}<div class="cap">f = −(E/jωx₀)·i − u/(jωC_M)  →  the 1/jω moved into C_M</div></div></div>`;
}

function diagMap() {
  const root = document.getElementById("diag-map"); if (!root) return;
  root.innerHTML = svgWrap(980, 250, [
    // spine
    `<path d="M40 125 H940" stroke="var(--rule-2)" stroke-width="2"/>`,
    ...[[70, "0", "The rules", "why circuits", "lecture 0"], [215, "1", "Analogies", "R · L · C in three worlds", "lecture 1"], [360, "2", "Mechanical", "mass, spring, damper", "lecture 2"], [505, "3", "Acoustic", "tube = mass, box = spring", "lecture 3"], [650, "4", "Transducers", "Bl and S join the worlds", "lecture 4"], [795, "5", "Microphones", "band-pass · low-pass · polar", "lecture 5"], [925, "→", "Loudspeakers", "next up", ""]].map(([x, n, t, s, e], i) => `
      <circle cx="${x}" cy="125" r="${i === 6 ? 14 : 20}" fill="var(--surface)" stroke="${i === 6 ? "var(--rule-2)" : "var(--ink)"}" stroke-width="2"/>
      <text x="${x}" y="130" text-anchor="middle" font-family="var(--font-mono)" font-size="14" fill="${i === 6 ? "var(--ink-3)" : "var(--ink)"}">${n}</text>
      <text x="${x}" y="${i % 2 ? 74 : 178}" text-anchor="middle" font-family="var(--font-display)" font-size="18" font-weight="600" fill="var(--ink)">${t}</text>
      <text x="${x}" y="${i % 2 ? 94 : 198}" text-anchor="middle" font-family="var(--font-body)" font-size="12.5" fill="var(--ink-2)">${s}</text>
      <line x1="${x}" y1="${i % 2 ? 100 : 150}" x2="${x}" y2="${i % 2 ? 105 : 145}" stroke="var(--rule-2)"/>`),
    // domain bands
    `<rect x="150" y="222" width="290" height="6" rx="3" fill="var(--el)"/><rect x="290" y="222" width="360" height="6" rx="3" fill="var(--me)" opacity="0.9"/><rect x="440" y="222" width="480" height="6" rx="3" fill="var(--ac)" opacity="0.85"/>`,
    `<text x="160" y="244" font-family="var(--font-mono)" font-size="11" fill="var(--el)">electrical</text><text x="420" y="244" font-family="var(--font-mono)" font-size="11" fill="var(--me)">mechanical</text><text x="720" y="244" font-family="var(--font-mono)" font-size="11" fill="var(--ac)">acoustical</text>`,
  ].join(""));
}

document.addEventListener("DOMContentLoaded", () => { diagMap(); diagSeriesRLC(); diagTwoTubes(); diagChain(); diagDynMic(); diagCondNorton(); });
