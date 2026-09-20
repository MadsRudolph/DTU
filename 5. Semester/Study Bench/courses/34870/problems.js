/* The Analogy Bench — problem sets and solutions, one list per lecture.
   Sources: the in-lecture problem slides + the official "Problem Solving Lecture N
   – Solutions" decks (1–4A), the Problems 4 / 5 sheets with their 2026 solutions,
   the bonus mechanical problems, and the worked notes in the vault.
   Fields: id, title, tag (the answer in a few words), given, hint, sol (HTML;
   KaTeX in <span class="m">…</span> / <div class="M">…</div>), bench (+ benchLabel). */
"use strict";

window.PROBLEMS = {
  "1": [
    {
      id: "1.1", title: "Validate the duality of a DC circuit", tag: "same v₃ from mesh and from node analysis",
      given: `A source <span class="m">v_0</span> drives <span class="m">Z_1</span> in series with the parallel pair <span class="m">Z_2 \\parallel Z_3</span>. (1) Prove mathematically that mesh analysis of this circuit and node analysis of its <b>dual</b> (a current source <span class="m">i_0</span> into <span class="m">Y_1</span> in parallel with the series pair <span class="m">Y_2, Y_3</span>) give the same result. (2) Check both in LTspice.`,
      hint: `One mesh (M1) and one node (N1) are enough. Write <span class="m">v = Zi</span> with <span class="m">\\sum_{mesh} v = 0</span> for the original, <span class="m">i = Yv</span> with <span class="m">\\sum_{node} i = 0</span> for the dual, and solve both for the voltage across the parallel pair.`,
      sol: `<p><b>Original.</b> M1: <span class="m">v_0 = v_1 + v_3 = Z_1 i_1 + v_3</span>. N1: <span class="m">i_1 = i_2 + i_3 = v_3/Z_2 + v_3/Z_3</span>. Eliminate <span class="m">i_1</span>:</p>
<div class="M">v_3 = v_0\\,\\frac{Z_2 Z_3}{Z_1(Z_2+Z_3) + Z_2 Z_3}</div>
<p><b>Dual.</b> M1: <span class="m">i_0 = i_1 = i_2 + i_3 = Y_2 v_3 + Y_3 v_3</span>. N1: <span class="m">v_0 = v_1 + v_3 = i_1/Y_1 + v_3</span>. Hence</p>
<div class="M">v_3 = v_0\\,\\frac{Y_1}{Y_2 + Y_3 + Y_1} = \\frac{v_0}{Z_1(1/Z_2 + 1/Z_3) + 1}</div>
<p>which is the same expression. Every mesh became a node, every series pair a parallel pair, every <span class="m">Z</span> a <span class="m">Y</span>.</p>
<p class="small"><b>LTspice:</b> the simulator only knows impedances, so when you build the dual the component <em>values</em> change units (a 2 Ω resistor becomes a 0.5 Ω one, an inductor becomes a capacitor of the same numeric value). The two node voltages must overlap exactly.</p>`,
    },
    {
      id: "1.2", title: "Validate the duality of an AC circuit", tag: "V(n002) and I(C2) overlap in magnitude and phase",
      given: `Repeat 1.1 with reactive elements (L and C) and an AC sweep, so that magnitude <em>and</em> phase are compared.`,
      hint: `Same transform: <span class="m">L \\leftrightarrow C</span>, series <span class="m">\\leftrightarrow</span> parallel, voltage source <span class="m">\\leftrightarrow</span> current source. Plot the across variable of the original against the through variable of the dual.`,
      sol: `<p>The solution deck shows <span class="mono">V(n002)</span> of the original and <span class="mono">I(C2)</span> of the dual lying on top of each other from 100 Hz to 10 kHz, in dB and in phase (0° to 180°).</p>
<p class="small"><b>The trap the deck flags:</b> LTspice's inductor has a hidden <em>default series resistance</em> (1 mΩ). In the dual that resistance has no counterpart, so the two curves disagree slightly near resonance until you set it to 0 in the inductor's properties.</p>`,
    },
    {
      id: "1.3", title: "Series resonator, then the same resonator in mechanics and acoustics", tag: "f₀ = 1125 Hz · i = 100 mA · BW = 159 Hz",
      given: `<span class="m">R = 10\\ \\Omega</span>, <span class="m">L = 10\\ \\text{mH}</span>, <span class="m">C = 2\\ \\mu\\text{F}</span>, driven by 1 V. Set up the equation, find the resonance frequency, current and impedance, plot current and impedance (magnitude and phase). Then build a <b>mechanical</b> and an <b>acoustical</b> resonator with the same behaviour — which element values are needed?`,
      hint: `Resonance is where the imaginary parts cancel: <span class="m">\\omega_0 L = 1/(\\omega_0 C)</span>. At that frequency only R is left. The bandwidth of a series RLC is <span class="m">R/(2\\pi L)</span>.`,
      sol: `<div class="M">v = Ri + L\\frac{di}{dt} + \\frac{1}{C}\\int i\\,dt = i\\left(R + j\\omega L + \\frac{1}{j\\omega C}\\right) \\quad\\Rightarrow\\quad i = \\frac{v}{R + j\\omega L + 1/(j\\omega C)}</div>
<div class="M">\\omega_0 = \\frac{1}{\\sqrt{LC}} \\;\\Rightarrow\\; f_0 = 1125\\ \\text{Hz}, \\qquad i_{max} = \\frac{v}{R} = 100\\ \\text{mA}, \\qquad Z_{min} = R = 10\\ \\Omega, \\qquad BW = \\frac{R}{2\\pi L} = 159\\ \\text{Hz}\\ (Q \\approx 7.1)</div>
<p>Current peaks and impedance dips at <span class="m">f_0</span>; phase goes from −90° (capacitive, below) through 0° to +90° (inductive, above) for the impedance.</p>
<p><b>Same behaviour in the other domains</b> (impedance analogy, same numbers, new units):</p>
<div class="table-wrap"><table><tr><th></th><th class="el">electrical</th><th class="me">mechanical</th><th class="ac">acoustical</th></tr>
<tr><td>real</td><td class="el">R = 10 Ω</td><td class="me">R<sub>M</sub> = 10 kg/s</td><td class="ac">R<sub>A</sub> = 10 Pa·s/m³</td></tr>
<tr><td>jω</td><td class="el">L = 10 mH</td><td class="me">M<sub>M</sub> = 10 g</td><td class="ac">M<sub>A</sub> = 10 g/m⁴</td></tr>
<tr><td>1/jω</td><td class="el">C = 2 µF</td><td class="me">C<sub>M</sub> = 2 µm/N (k = 0.5 MN/m)</td><td class="ac">C<sub>A</sub> = 2 µm⁵/N = 0.2 dm⁵/N</td></tr></table></div>`,
      bench: "#bench-resonator", benchLabel: "the resonator bench draws exactly this curve (set M = 10 g, C = 0.002 mm/N is off its range, so use the shape)",
    },
  ],
  "2": [
    {
      id: "2.1", title: "Graphical conversion between the analogies", tag: "mesh → node, every element → its dual",
      given: `A three-mass chain in the impedance analogy: a velocity source <span class="mono">u₁ = 2 m/s</span> drives mass <span class="mono">M₁ = 10 g</span> on spring <span class="mono">C₁ = 1 mm/N</span> and damper <span class="mono">R₁ = 1 Ns/m</span>; <span class="mono">M₁</span> is joined to <span class="mono">M₂ = 25 g</span> by damper <span class="mono">R₂ = 2</span>, and <span class="mono">M₂</span> to <span class="mono">M₃ = 40 g</span> by spring <span class="mono">C₃ = 0.3 mm/N</span> ∥ damper <span class="mono">R₃ = 3</span>. a) Convert the circuit to the mobility analogy. b) Draw the mechanical sketch.`,
      hint: `Put a dot in every mesh and one outside (that outside dot is ground). Connect dots through the elements they share, replacing each element by its dual. A mass is always between a mesh and the outside dot.`,
      sol: `<p><b>a)</b> Rules, applied element by element:</p>
<div class="table-wrap"><table><tr><th>impedance analogy</th><th>mobility analogy</th></tr>
<tr><td>voltage source u₁ (series)</td><td>current source u₁ into node 1</td></tr>
<tr><td>L = M<sub>M</sub> in a mesh</td><td>C = M<sub>M</sub> from that node to ground</td></tr>
<tr><td>C = C<sub>M</sub> between two meshes</td><td>L = C<sub>M</sub> between the two nodes</td></tr>
<tr><td>R = R<sub>M</sub></td><td>R = 1/R<sub>M</sub>, same place</td></tr></table></div>
<p>Result: three velocity nodes u₁, u₂, u₃; <span class="mono">C{M₁}, L{C₁}, R{1/R₁}</span> from u₁ to ground; <span class="mono">R{1/R₂}</span> between u₁ and u₂; <span class="mono">C{M₂}</span> from u₂ to ground; <span class="mono">L{C₃} ∥ R{1/R₃}</span> between u₂ and u₃; <span class="mono">C{M₃}</span> from u₃ to ground. The solution deck's two LTspice sheets (impedance with L1/R1/C1…, mobility with C1x/L1x/R1x…) give identical node velocities.</p>
<p><b>b)</b> Sketch: the source pushes M₁, which sits on C₁ and R₁ against the wall; a damper R₂ links M₁ to M₂; a spring C₃ with damper R₃ links M₂ to M₃; all three masses are drawn against the fixed reference (ground).</p>`,
    },
    {
      id: "2.2", title: "Mass on a spring, force-driven and velocity-driven", tag: "f₀ = 35.6 Hz · u = 20 m/s per 10 N · f = 0.5 N per 1 m/s",
      given: `<span class="mono">M<sub>M</sub> = 20 g</span>, stiffness <span class="mono">k = 1000 N/m</span> (so <span class="m">C_M = 1/k = 1\\ \\text{mm/N}</span>), damping <span class="mono">R<sub>M</sub> = 0.5 Ns/m</span> — typical low-frequency loudspeaker values. b) Drive with a force of 10 N: plot the velocity. c) Drive with a velocity of 1 m/s: plot the force the source must supply, and explain the difference.`,
      hint: `Same impedance both times: <span class="m">Z_M = R_M + j\\omega M_M + 1/(j\\omega C_M)</span>. A force source asks for <span class="m">u = f/Z_M</span>; a velocity source asks for <span class="m">f = Z_M u</span>.`,
      sol: `<div class="M">\\omega_0 = \\frac{1}{\\sqrt{M_M C_M}} = 223.6\\ \\text{rad/s} \\;\\Rightarrow\\; f_0 = 35.6\\ \\text{Hz}, \\qquad Z_M(\\omega_0) = R_M = 0.5\\ \\text{kg/s}, \\qquad Y_M(\\omega_0) = 2\\ \\text{s/kg}</div>
<p><b>b)</b> <span class="m">u(\\omega_0) = 10\\ \\text{N} \\times 2\\ \\text{s/kg} = 20\\ \\text{m/s}</span> — a <b>peak</b>. Below f₀ the velocity rises with frequency (spring-controlled, +90°), above it falls at −6 dB/oct (mass-controlled, −90°).</p>
<p><b>c)</b> <span class="m">f(\\omega_0) = 0.5\\ \\text{N}</span> — a <b>dip</b>, the mirror image. Imposing the motion, the source only has to overcome the damper at resonance; away from it the spring (low f) or the mass (high f) demand force. Same f₀, same Q, the curve upside down: that is duality.</p>`,
      bench: "#bench-resonator", benchLabel: "the resonator bench starts with exactly these values; flip the source toggle",
    },
    {
      id: "2.3", title: "The driver as an equivalent source", tag: "u_No = f_Th / Z_M · u_Th = Y_M · f_No",
      given: `The driver of 2.2 is driven by a harmonic Lorentz force of 10 N. a) Impedance and admittance. b) The correct Norton/Thévenin form in each analogy. c) Convert the force source into a velocity source — what is the equivalent velocity at resonance?`,
      hint: `Thévenin ↔ Norton works as in electronics; the only question is which variable is "voltage" in the analogy you are drawing.`,
      sol: `<div class="M">Z_M = 0.5 + j\\left(\\omega\\cdot 0.02 - \\frac{10^3}{\\omega}\\right)\\ \\text{kg/s}, \\qquad Y_M = \\frac{1}{R_M} \\,\\Big\\|\\, j\\omega C_M \\,\\Big\\|\\, \\frac{1}{j\\omega M_M}</div>
<p><b>b)</b> Impedance analogy: force source <span class="m">f_{Th}</span> in series with <span class="m">Z_M</span> ⇔ velocity source <span class="m">u_{No} = f_{Th}/Z_M</span> in parallel with <span class="m">Z_M</span>. Mobility analogy: force source <span class="m">f_{No}</span> (a current) in parallel with <span class="m">Y_M</span> ⇔ velocity source <span class="m">u_{Th} = Y_M f_{No}</span> in series with <span class="m">Y_M</span>.</p>
<p><b>c)</b> At resonance <span class="m">Y_M = 2\\ \\text{s/kg}</span>, so <span class="m">u = 10\\ \\text{N} \\times 2 = 20\\ \\text{m/s}</span>: the same number as 2.2b, of course — it is the same physics with the source redrawn.</p>`,
    },
    {
      id: "2.4", title: "Two-mass system and its limiting cases", tag: "five limits, predicted then simulated",
      given: `Force <span class="mono">f = 1 N</span> on <span class="mono">M₁ = 1 g</span>; <span class="mono">M₁</span> is joined to a free mass <span class="mono">M₂ = 2 g</span> through <span class="mono">C₁ = 10 mm/N</span> in parallel with <span class="mono">R₁ = 0.3 Ns/m</span>. Model it, check <span class="mono">u₁</span> and <span class="mono">u₂</span> in LTspice, then predict and verify: <span class="m">M_1 \\to \\infty</span>, <span class="m">M_2 \\to \\infty</span>, <span class="m">C_1 \\to 0</span>, <span class="m">R_1 \\to \\infty</span>, <span class="m">R_1 \\to 0\\ \\&\\ C_1 \\to \\infty</span>.`,
      hint: `Each limit removes or rigidifies one element. An infinite mass is a wall; a zero compliance or infinite damper is a rigid rod; a zero damper with infinite compliance is no link at all.`,
      sol: `<div class="table-wrap"><table><tr><th>limit</th><th>u₁</th><th>u₂</th><th>why</th></tr>
<tr><td><span class="m">M_1 \\to \\infty</span></td><td>0</td><td>0</td><td>the driven mass is a wall; nothing moves</td></tr>
<tr><td><span class="m">M_2 \\to \\infty</span></td><td>&lt; reference at low f</td><td>0</td><td>M₂ is a wall, so M₁ now sits on C₁ against the wall: spring-controlled below the new resonance</td></tr>
<tr><td><span class="m">C_1 \\to 0</span></td><td>u₁ = u₂</td><td>u₁ = u₂</td><td>rigid rod: one 3 g body</td></tr>
<tr><td><span class="m">R_1 \\to \\infty</span></td><td>u₁ = u₂</td><td>u₁ = u₂</td><td>an infinitely stiff damper is also a rod</td></tr>
<tr><td><span class="m">R_1 \\to 0,\\ C_1 \\to \\infty</span></td><td>≥ reference</td><td>0</td><td>no link: M₁ alone (lighter, so faster), M₂ untouched</td></tr></table></div>
<p>Reference case: below the link resonance both masses move together as 3 g (<span class="m">u \\approx f/(j\\omega \\cdot 3\\,\\text{g})</span>); at the link resonance (reduced mass 0.67 g on 10 mm/N → ≈ 62 Hz) they swing against each other; above it M₂ decouples and u₂ falls 12 dB/oct faster.</p>`,
      bench: "#bench-twomass", benchLabel: "the two-mass bench has every limit as a chip",
    },
    {
      id: "Bonus 5", title: "Refrigerator with compressor", tag: "four feet = C/4 and 4R; the compressor mount goes in series",
      given: `A compressor exerts a force F on the rigid body of a refrigerator (mass <span class="mono">M<sub>mb</sub></span>) standing on four elastic feet (each <span class="mono">C<sub>mf</sub></span>, <span class="mono">R<sub>mf</sub></span>) on an infinitely hard floor. a) Mechanical sketch and equivalent circuit. b) The compressor (mass <span class="mono">M<sub>mc</sub></span>) is now mounted on its own elastic suspension <span class="mono">C<sub>ms</sub></span>, <span class="mono">R<sub>ms</sub></span>, and the force acts on the compressor mass. Extend both drawings.`,
      hint: `Four identical springs side by side share the load: stiffnesses add. Then ask, for each element, "does it share a velocity with its neighbour (mechanically parallel) or carry the same force (mechanically series)?"`,
      sol: `<p><b>a)</b> Masses always against ground. Four springs in parallel act as one spring of compliance <span class="m">C_{mf}/4</span>; four dampers in parallel as one damper <span class="m">4R_{mf}</span>. The body, the combined spring and the combined damper all share the body's velocity, so in the impedance analogy they are in series with the force source (mobility: in parallel off the one velocity node).</p>
<p><b>b)</b> The new suspension is <em>mechanically in series</em> with the circuit of a) (it carries the force between compressor and body), so it appears in parallel in the impedance analogy and in series in the mobility analogy. The compressor mass is mechanically in parallel with everything else (it shares the source velocity), so electrically it is in series (impedance) or in parallel (mobility) with the rest. Mobility drawing: source into node u<sub>c</sub>; <span class="mono">C{M_mc}</span> to ground; <span class="mono">L{C_ms} ∥ R{1/R_ms}</span> to node u<sub>b</sub>; <span class="mono">C{M_mb}, L{C_mf/4}, R{1/(4R_mf)}</span> to ground.</p>`,
    },
    {
      id: "Bonus 6", title: "Car suspension", tag: "a velocity source at the wheel; packers stiffen; tyre goes between",
      given: `One wheel of a car with perfect weight distribution (<span class="mono">M<sub>mc</sub>/4</span>). The wheel follows the road, i.e. it is driven at a given velocity. a) Equivalent circuit (wheel and suspension mass ignored). b) Racing cars insert hard rubber packers in the spring (compliance <span class="mono">C<sub>p</sub></span>) that engage on large displacements: sketch and circuit when both spring and packer are compressed. c) Include the wheel mass and the tyre's compliance and damping.`,
      hint: `Same system as Bonus 5a, but the source is now a <b>velocity</b> source at the wheel. Where does the road's velocity go — into moving the car, or into compressing the spring?`,
      sol: `<p><b>a)</b> The road velocity is used either to move the car mass or to compress the spring/damper: mass and spring–damper are two parallel branches (impedance) or one series path (mobility) fed by the velocity source.</p>
<p><b>b)</b> The packer is a spring in parallel with the suspension spring, so the two compliances appear in series (impedance) or in parallel (mobility): the combination is <em>smaller</em> than the smaller of the two — a stiffer suspension, as intended.</p>
<p><b>c)</b> The tyre (compliance + damping) and the wheel mass sit between the source and the old system, in the circuit as well: the road velocity now moves either the tyre spring/damper or the rest. Note the similarity with Bonus 5b — the wheel is the "compressor", the tyre its suspension.</p>`,
    },
  ],
  "3": [
    {
      id: "3.1 + 3.2", title: "Tube in a box: elements, assumptions, resonance", tag: "open tube = L, closed box = C to ground, f₀ = 1/(2π√(M_A C_A))",
      given: `An open tube is connected to a closed box and driven from outside by a volume velocity. a) Which lumped elements are the tube and the box? b) Which assumptions must hold? c) Draw the circuit. d) Find the resonance and choose values for <span class="mono">f₀ = 100 Hz</span>; verify in LTspice.`,
      hint: `The tube's air moves as one plug (inertia). The box's air compresses (spring) against still air outside — so the compliance is grounded.`,
      sol: `<p><b>a)</b> Open tube → acoustic mass → inductor. Closed box → acoustic compliance → capacitor, <b>grounded</b>.</p>
<p><b>b)</b> Real dimensions much smaller than the wavelength (the deck marks this one with a question mark — check it for your chosen geometry); homogeneous element properties ✓; idealised rigid walls ✓.</p>
<p><b>c)</b> Current source U → L (M<sub>A</sub>) → node p → C (C<sub>A</sub>) → ground: the Helmholtz resonator.</p>
<div class="M">Z_A = j\\omega M_A + \\frac{1}{j\\omega C_A} = 0 \\;\\Rightarrow\\; \\omega_0 = \\frac{1}{\\sqrt{M_A C_A}} \\;\\Rightarrow\\; M_A = \\frac{1}{(2\\pi\\cdot 100\\ \\text{Hz})^2 C_A}</div>
<p><b>d)</b> e.g. <span class="m">C_A = 2.53\\times10^{-8}\\ \\text{m}^5/\\text{N}</span> (a 3.5 L box) and <span class="m">M_A = 100\\ \\text{kg/m}^4</span> give 100 Hz. Any pair with the same product works; the vault's version uses a 1 cm neck and a 1.9 L box.</p>`,
      bench: "#bench-helmholtz", benchLabel: "the bottle bench: set it to 100 Hz and hear it",
    },
    {
      id: "3.3", title: "Tubes in a box", tag: "92.4 Hz resonance · 9.2 Hz anti-resonance · 92.8 Hz when driven from the wide tube",
      given: `<span class="mono">ρ = 1.18, c = 344</span>. Open tube, effective length 12 cm, diameter 10 cm, into a 23 L box, driven by U from outside. a) Elements at low frequency. b) Resonance. c) A second, narrower tube (diameter 1 cm, same length) is added: how is it connected? d) Where is the pressure measured, and what does it look like? e–f) Impedance seen from the wide tube, resonance; simulate. g) What changes when driven from the narrow tube?`,
      hint: `<span class="m">M_A = \\rho l^*/S</span>, <span class="m">C_A = V/(\\rho c^2)</span>. The narrow tube opens to the outside, where the pressure is ≈ 0: it goes to ground.`,
      sol: `<div class="M">M_{A1} = \\frac{\\rho l^*}{\\pi r^2} = 18.03\\ \\text{kg/m}^4, \\qquad C_A = \\frac{V}{\\rho c^2} = 1.65\\times10^{-7}\\ \\text{m}^5/\\text{N}, \\qquad f_A = \\frac{1}{2\\pi\\sqrt{M_{A1} C_A}} = 92.4\\ \\text{Hz}</div>
<p><b>c)</b> The narrow tube connects the cavity to the outside, where the pressure is much smaller than inside — connect it to ground (or to a radiation impedance). <span class="m">M_{A2} = 1803\\ \\text{kg/m}^4</span>, 100× the wide tube because <span class="m">S \\propto r^2</span>.</p>
<p><b>d)</b> The pressure is the node where box and both tubes meet. The cavity is now in parallel with the narrow tube: an <b>anti-resonance</b> at <span class="m">f_B = 1/(2\\pi\\sqrt{M_{A2} C_A}) = 9.2\\ \\text{Hz}</span>, where the impedance and therefore the box pressure become very large. The first mass is in series with the volume-velocity source, so it has no influence on the box pressure.</p>
<p><b>f)</b> Driven by a volume-velocity source, the acoustic impedance is the pressure the source must supply: its minimum is the resonance, 92.8 Hz, barely above 92.4 because the heavy narrow tube hardly loads the light wide one.</p>
<p><b>g)</b> Driven from the narrow tube the roles swap: the peak (anti-resonance) is now set by <span class="m">M_{A1} \\parallel C_A</span> and the minimum by <span class="m">M_{A2} + M_{A1}\\parallel C_A</span>, dominated by M<sub>A1</sub> — so resonance and anti-resonance land almost on top of each other.</p>`,
      bench: "#bench-helmholtz", benchLabel: "set neck 12 cm / 5 cm radius / 23 L on the bottle bench: 92 Hz",
    },
    {
      id: "3.4", title: "Dynamic microphone: the acoustic network behind the diaphragm", tag: "C_A1 to ground, R_A in series, C_A2 to ground: a low-pass",
      given: `The diaphragm (a volume-velocity source) feeds a small volume V₁ right behind it; a canal filled with porous material leads to a larger volume V₂. Draw the equivalent circuit.`,
      hint: `Two enclosed volumes and one loss element. Every enclosed volume goes to ground.`,
      sol: `<p>U → node 1 with <span class="m">C_{A1} = V_1/\\rho c^2</span> to ground → <span class="m">R_A</span> (the porous canal) → node 2 with <span class="m">C_{A2} = V_2/\\rho c^2</span> to ground. A C–R–C ladder: at high frequency C<sub>A1</sub> shunts the flow before it reaches V₂, so the pressure behind the diaphragm rolls off — this network returns as the dynamic microphone's back volume in lecture 4B and as the bandwidth tricks in Problems 4.</p>`,
    },
  ],
  "4": [
    {
      id: "4.1", title: "Bass-reflex box", tag: "Z_A,max = 995·10³ Pa·s/m³ (not 995 kΩ — watch the units)",
      given: `Vented box: vent l* = 12 cm, Ø 10 cm, V = 23 L (the box of 3.3). The driver is a baffled massless piston of the same diameter, vibrating with velocity u. a) Circuit. b) Add the radiation impedances. c) Acoustic impedance seen by the piston. d) Far-field pressure as a point source; plot |p| over distance for f = 1 kHz, u = 1 m/s.`,
      hint: `Front and back of the piston carry the same U = S·u. The box compliance and the vent are in parallel because ground is both the cavity reference and the far end of the radiation.`,
      sol: `<p><b>a+b)</b> The loudspeaker creates <span class="m">U = S u</span> and a pressure difference between front (outside) and back (inside). The back sees the cavity <span class="m">C_A</span> to ground in parallel with the vent mass <span class="m">M_A</span> in series with the vent's radiation impedance (internal end correction only). The front sees a radiation impedance <span class="m">Z_{Ar}</span>; both are the same here since piston and vent share a diameter.</p>
<div class="M">Z_A = \\frac{p_f - p_b}{U} = Z_{Ar} + \\frac{1}{j\\omega C_A} \\,\\Big\\|\\, \\left(j\\omega M_A + Z_{Ar}\\right), \\qquad Z_{Ar} = j\\omega M_{A1} \\,\\Big\\|\\, \\left[R_{A2} + \\left(R_{A1} \\parallel \\tfrac{1}{j\\omega C_{A1}}\\right)\\right]</div>
<p><b>c)</b> The maximum is <span class="m">Z_{A,max} = 995\\times10^{3}\\ \\text{Pa·s/m}^3</span> at the box–port anti-resonance. <em>Not</em> 995 kΩ — LTspice shows ohms, the physics is Pa·s/m³. The vault simulation puts that peak at 79 Hz rather than 92 Hz once the vent's radiation mass (6.4 kg/m⁴) is added to M<sub>Av</sub> = 18.</p>
<div class="M">\\text{d)}\\quad p(r,t) = \\frac{j\\omega\\rho U}{4\\pi r} e^{j(\\omega t - kr)} = \\frac{j f \\rho S u}{2r} e^{j(\\omega t - kr)} \\;\\Rightarrow\\; |p| \\propto \\frac{1}{r}</div>
<p>a straight −6 dB per doubling of distance, valid while <span class="m">kr \\gg 1</span> and the box is small against λ.</p>`,
    },
    {
      id: "4.2", title: "Piston in a baffle, then in a tube, then on a box", tag: "Z_m = jωM_mp + 2S²Z_ar · tube = ρd/S with geometric length · box = C_a with end correction",
      given: `A force f drives a massless-thickness piston of mass <span class="mono">M<sub>mp</sub></span>, area S, in an infinite baffle; radiation impedance <span class="mono">Z<sub>ar</sub></span> per side. a) Circuit with controlled sources. b) Total mechanical impedance. c) The baffle has thickness d: what changes, and when is d "small"? d) A closed box of volume V is put on the back. e) Insert the radiation network.`,
      hint: `p in the coupling is the pressure <em>difference</em> across the piston. Reflect an acoustic impedance into mechanics with S².`,
      sol: `<p><b>a)</b> Two controlled sources couple the domains; the total acoustic load is <span class="m">2Z_{ar}</span> (both sides), and the p in <span class="m">f = Sp</span> is the difference across the piston.</p>
<div class="M">\\text{b)}\\quad f = S p = 2S^2 Z_{ar}\\,u \\;\\Rightarrow\\; Z_m = \\frac{f_0}{u} = j\\omega M_{mp} + 2S^2 Z_{ar}</div>
<p><b>c)</b> With <span class="m">d \\ll \\lambda</span> (rule of thumb <span class="m">d &lt; \\lambda/10</span>) the air in the short tube moves as a unit: an acoustic mass <span class="m">M_a = \\rho d/S</span> using the <b>geometric</b> length, because the radiation impedance already contains the end correction.</p>
<p><b>d)</b> The back volume <span class="m">C_a = V/\\rho c^2</span> takes the place of the back radiation impedance; now the end correction <em>is</em> necessary on the tube: <span class="m">M_a^* = M_a + M_{a1}</span>. The piston feels an extra stiffness <span class="m">S^2/C_a</span> — the sealed-box resonance.</p>
<p><b>e)</b> Front <span class="m">Z_{ar} = M_{A1} \\parallel [R_{A2} + (R_{A1} \\parallel C_{A1})]</span> with the baffled-piston values of lecture 3.</p>`,
      bench: "#bench-pistonbox", benchLabel: "the piston-in-a-box bench is 4.2 d/e with the 4.4a numbers",
    },
    {
      id: "4.3", title: "Coil in a magnetic field on a suspension", tag: "Z_E = R_E + jωL_E + (Bl)² / Z_M — the impedance inversion",
      given: `Coil (length l, field B, mass <span class="mono">M<sub>mc</sub></span>, resistance <span class="mono">R<sub>E</sub></span>, inductance <span class="mono">L<sub>E</sub></span>) on a suspension <span class="mono">C<sub>ms</sub></span>, <span class="mono">R<sub>ms</sub></span>. a) Impedance-analogy circuit. b) Impedance at the electrical terminals. c) Mobility-analogy circuit. d) Compare. e) Velocity and the forces in coil and suspension versus the driving current.`,
      hint: `Two loops joined by two controlled sources: <span class="m">f = Bl\\,i</span> into the mechanical loop, <span class="m">v = Bl\\,u</span> back into the electrical one. Eliminate u.`,
      sol: `<div class="M">Z_E = R_E + j\\omega L_E + \\frac{Bl\\,u}{i} = R_E + j\\omega L_E + (Bl)^2\\frac{u}{f} = R_E + j\\omega L_E + \\frac{(Bl)^2}{j\\omega M_{mc} + R_{ms} + \\dfrac{1}{j\\omega C_{ms}}}</div>
<p><b>d)</b> The mobility circuit gives the same thing: compute the mechanical admittance, invert. That "(impedance inversion)" is why a mechanical series resonance is an electrical impedance <b>peak</b>.</p>
<p><b>e)</b> <span class="m">f = Bl\\,i</span>, <span class="m">u = Bl\\,i / Z_M</span>, and the force splits as <span class="m">f = f_{Mmc} + f_{Rms} + f_{Cms}</span>:</p>
<div class="M">f_{Mmc} = \\frac{Bl}{1 + \\dfrac{R_{ms}}{j\\omega M_{mc}} - \\dfrac{1}{\\omega^2 M_{mc} C_{ms}}}\\,i, \\qquad f_{Cms} = \\frac{Bl}{-\\omega^2 M_{mc} C_{ms} + j\\omega C_{ms} R_{ms} + 1}\\,i</div>
<p>Below resonance the spring takes the force, above it the mass; at resonance the two cancel and the whole <span class="m">Bl\\,i</span> goes into the damper.</p>`,
      bench: "#bench-speakerz", benchLabel: "the impedance-peak bench starts with the 4.4b values",
    },
    {
      id: "4.4", title: "LTspice: the piston, the coil, and the two together", tag: "20 Hz piston-on-box · 7.2 Ω at 50.3 Hz · 33 Hz combined",
      given: `a) 4.2 with S = 100 cm², M<sub>mp</sub> = 20 g, V = 40 L, d = 2 cm — both analogies must agree. b) 4.3 with l = 3 m, B = 0.7 T, M<sub>mc</sub> = 10 g, C<sub>ms</sub> = 1 mm/N, R<sub>ms</sub> = 2 Ns/m, R<sub>E</sub> = 5 Ω, L<sub>E</sub> = 0.3 mH. c) Coil rigidly attached to the piston.`,
      hint: `Plot f/u for a) and v/i for b). For c) the velocities are equal, so the masses add and the compliances combine as springs in parallel (stiffnesses add).`,
      sol: `<p><b>a)</b> Plot the mechanical impedance f/u. Air load per side <span class="m">S^2 M_{A1} = 0.57\\ \\text{g}</span>, tube <span class="m">0.24\\ \\text{g}</span>, box stiffness <span class="m">S^2/C_{AB} = 350\\ \\text{N/m}</span> (2.86 mm/N): about 21.4 g on 2.86 mm/N → <b>≈ 20 Hz</b>, damped only by the front radiation resistance, so a very sharp dip. The vault's KiCad sheet has both analogies side by side; they agree to 10⁻⁴.</p>
<p><b>b)</b> Plot the input voltage divided by the source current: <span class="m">f_0 = 50.3\\ \\text{Hz}</span>, motional resistance <span class="m">(Bl)^2/R_{ms} = 2.2\\ \\Omega</span>, so <span class="m">|Z_E|</span> peaks at <b>7.2 Ω</b>, then rises with <span class="m">\\omega L_E</span> above 2.65 kHz. Forces and velocities are read as the equivalent voltage drops and currents.</p>
<p><b>c)</b> Adapt the microphone exercise from the lecture: rigidly connected means the same velocity, so the masses add (31.4 g) and the suspensions act in parallel (0.74 mm/N) → <b>≈ 33 Hz</b>; the electrical impedance now shows that peak, broader because the radiation damping is added.</p>`,
      bench: "#bench-speakerz", benchLabel: "4.4b live",
    },
    {
      id: "Sheet 1", title: "Problems 4 · design a dynamic microphone", tag: "0.205 g · 0.168 mm/N · 10.8 cm³ · 3.56·10⁷ · 7.88 kHz · 125 Hz / 8.01 kHz",
      given: `<span class="mono">M<sub>MD</sub> = 0.2 g, R<sub>MS</sub> = 1 Ns/m, C<sub>MS</sub> = 0.21 mm/N</span>, diaphragm Ø 1 inch, <span class="mono">Bl = 20 T·m, R<sub>E</sub> = 200 Ω, R<sub>L</sub> = 47 kΩ</span>. a) Total mass and compliance with a 30 cm³ back volume. b) Back volume for f₀ = 1 kHz. c) R<sub>AF</sub> for 1 mV/Pa, and the bandwidth. d) The −3 dB frequencies.`,
      hint: `Everything reduces to <span class="m">M_{MT}, R_{MT}, C_{MT}</span>. The official solution takes the front air mass as a <b>piston in a tube</b>, <span class="m">M_{A1} = 0.6133\\rho/(\\pi a) = 18.1\\ \\text{kg/m}^4</span> (the "piston on a cylinder" of the 4B slide), not the baffled value 25.1.`,
      sol: `<div class="M">a = 12.7\\ \\text{mm},\\quad S_D = 5.07\\times10^{-4}\\ \\text{m}^2,\\quad M_{A1} = \\frac{0.6133\\rho}{\\pi a} = 18.1 \\;\\Rightarrow\\; M_{MT} = M_{MD} + S_D^2 M_{A1} = 0.2047\\ \\text{g}</div>
<div class="M">\\text{a)}\\quad C_{AB} = \\frac{30\\ \\text{cm}^3}{\\rho c^2} = 2.15\\times10^{-10}, \\qquad C_{MT} = \\left(\\frac{1}{C_{MS}} + \\frac{S_D^2}{C_{AB}}\\right)^{-1} = 0.168\\ \\text{mm/N}</div>
<div class="M">\\text{b)}\\quad C_{MT} = \\frac{1}{(2\\pi f_0)^2 M_{MT}} = 1.238\\times10^{-4} \\;\\Rightarrow\\; C_{AB} = \\frac{S_D^2}{1/C_{MT} - 1/C_{MS}} = 7.74\\times10^{-11} \\;\\Rightarrow\\; V_{AB} = C_{AB}\\rho c^2 = 10.8\\ \\text{cm}^3</div>
<div class="M">\\text{c)}\\quad R_{MT} = \\frac{Bl\\,S_D}{M} = 10.13\\ \\text{Ns/m}, \\qquad R_{AF} = \\frac{R_{MT} - R_{MS} - (Bl)^2/(R_E + R_L)}{S_D^2} = 3.56\\times10^{7}\\ \\text{Ns/m}^5, \\qquad Q = \\frac{2\\pi f_0 M_{MT}}{R_{MT}} = 0.127, \\qquad BW = \\frac{f_0}{Q} = 7.88\\ \\text{kHz}</div>
<div class="M">\\text{d)}\\quad f_a f_b = f_0^2,\\ f_b - f_a = BW \\;\\Rightarrow\\; f_a = 125\\ \\text{Hz},\\ f_b = 8.01\\ \\text{kHz}</div>
<p class="small">The vault's first pass used the baffled-piston air mass (25.1 kg/m⁴) and got 10.6 cm³ — the 2 % gap is that convention, not rounding. Both are defensible; the sheet's numbers assume the tube value.</p>`,
      bench: "#bench-dynmic", benchLabel: "the microphone designer starts on this design (tube-end air mass); read the readouts",
    },
    {
      id: "Sheet 2", title: "Problems 4 · the dynamic microphone in LTspice", tag: "−55.7 dB at 1.21 kHz · then flatten it from 100 Hz to 10 kHz",
      given: `a) Model the microphone with V = 5 cm³ and R<sub>AF</sub> = 2·10⁷ Ns/m⁵ (ignore the mic's effect on the field). b) Get 0.3 mV/Pa and 3 mV/Pa. c) Extend the high end with two back cavities joined by a damped tube. d) Extend the low end with a tube into the large cavity.`,
      hint: `Sensitivity is <span class="m">\\propto 1/R_{MT}</span>, and <span class="m">R_{MT}</span> is dominated by <span class="m">S_D^2 R_{AF}</span>. For c) the damping must sit in the tube, or you get a notch instead of a lift.`,
      sol: `<p><b>a)</b> Official sheet: acoustic loop with <span class="mono">Ma1 = 18.13</span>, <span class="mono">Raf</span>, <span class="mono">Cab = 77.5 pF</span> (the 10.8 cm³ of sheet 1), diaphragm as two dependent sources of gain S<sub>D</sub>, mechanical <span class="mono">Mmd 0.2m, Rms 1, Cms 0.21m</span>, coil <span class="mono">Bl = 20</span> as two dependent sources, <span class="mono">Re 200</span>, <span class="mono">RL 47k</span>. With V = 5 cm³ and R<sub>AF</sub> = 2·10⁷: peak −55.7 dB re 1 V/Pa (1.64 mV/Pa) at 1.21 kHz, Q = 0.26, band 291 Hz – 5.0 kHz.</p>
<p><b>b)</b> <span class="m">R_{AF} = 1.27\\times10^{8}</span> → 0.30 mV/Pa with a 57 Hz – 26 kHz band; <span class="m">9.2\\times10^{6}</span> → 3.0 mV/Pa but only 480 Hz – 3.1 kHz. Sensitivity and bandwidth trade one for one.</p>
<p><b>c)</b> Keep the felt right behind the diaphragm, then a tiny V₁ (the official sheet uses ≈ 0.04 cm³, 0.3 pF) in parallel with a damped tube into the large V₂. At low frequency the tube conducts and both volumes count; at high frequency the tube mass blocks V₂, the diaphragm sees only the stiff V₁, and a new resonance near 7 kHz lifts the top end. A working set from the vault: <span class="mono">M_At = 300 kg/m⁴, R_At = 3·10⁷</span>.</p>
<p><b>d)</b> A vent (mass + resistance) from the V₂ node to ground: a Helmholtz resonator with V₂ that boosts the response around its frequency and steepens the roll-off below. Vault set: <span class="mono">M_Av = 10⁴, R_Av = 1.5·10⁷</span> (f<sub>H</sub> ≈ 270 Hz). Result: flat ±2 dB from 100 Hz to 10 kHz at 0.67 mV/Pa — the red curve of the official solution versus the blue hump.</p>`,
      bench: "#bench-dynmic", benchLabel: "set V = 5 cm³, R_AF = 2·10⁷ on the designer for a), then play with b)",
    },
  ],
  "5": [
    {
      id: "5.1", title: "Condenser microphone: resonance, Q, sensitivity", tag: "10.6 kHz · Q = 2.36 · 9.8 mV/Pa",
      given: `<span class="mono">C<sub>MD</sub> = 4·10⁻⁶ m/N, M<sub>MD</sub> = 0.050 g, R<sub>MD</sub> = 1 Ns/m</span>, effective diaphragm radius 9 mm; back side <span class="mono">M<sub>AS</sub> = 100 kg/m⁴, R<sub>AS</sub> = 10⁷ Ns/m⁵, V<sub>AB2</sub> = 1 cm³</span> (the gap volume is &gt; 200× smaller and can be ignored); <span class="mono">E = 200 V, x₀ = 20 µm, R<sub>L</sub>′ = 500 MΩ</span>. a) Resonance. b) Q. c) Sensitivity below resonance with T(s) = 1.`,
      hint: `Same three totals as the dynamic mic, but no electrical damping term (R<sub>L</sub>′ is huge) and the sensitivity is <span class="m">E S_D C_{MT}/x_0</span>. The official MATLAB solution takes the front air mass as a piston in a tube, <span class="m">M_{A1} = 0.6133\\rho/(\\pi r) = 25.6\\ \\text{kg/m}^4</span>.`,
      sol: `<div class="M">S_D = \\pi r^2 = 2.545\\times10^{-4}\\ \\text{m}^2, \\qquad C_{E0} = \\frac{\\varepsilon_0 S_D}{x_0} = 112.6\\ \\text{pF}, \\qquad M_{A1} = \\frac{0.6133\\rho}{\\pi r} = 25.6\\ \\text{kg/m}^4</div>
<div class="M">M_{MT} = M_{MD} + S_D^2(M_{A1} + M_{AS}) = 5.81\\times10^{-5}\\ \\text{kg}, \\qquad C_{AB2} = \\frac{V}{\\rho c^2} = 7.16\\times10^{-12}, \\qquad C_{MT} = \\left(\\frac{1}{C_{MD}} + \\frac{S_D^2}{C_{AB2}}\\right)^{-1} = 3.86\\times10^{-6}\\ \\text{m/N}, \\qquad R_{MT} = R_{MD} + S_D^2 R_{AS} = 1.648</div>
<div class="M">\\text{a)}\\ f_0 = \\frac{1}{2\\pi\\sqrt{M_{MT}C_{MT}}} = 10.6\\ \\text{kHz} \\qquad \\text{b)}\\ Q = \\frac{2\\pi f_0 M_{MT}}{R_{MT}} = 2.36 \\qquad \\text{c)}\\ M = \\frac{E\\,C_{MT}\\,S_D}{x_0} = 9.8\\ \\text{mV/Pa}\\ (-40.2\\ \\text{dB re 1 V/Pa})</div>
<p class="small">With the baffled-piston air mass (35.4 kg/m⁴) you get 10.57 kHz and Q = 2.37 — same answer to the sheet's precision. The lesson is the bookkeeping: <span class="m">S_D^2 R_{AS} = 0.65</span> and <span class="m">S_D^2/C_{AB2} = 9040</span> look alike but are three orders of magnitude apart; a slip there turns Q = 2.4 into nonsense.</p>`,
      bench: "#bench-condenser", benchLabel: "the condenser designer starts on 5.1; switch the front air mass to see both conventions",
    },
    {
      id: "5.2", title: "Condenser microphone in LTspice (a–c; d–e in lecture 6)", tag: "three blocks, two G sources, one 1/jω trick",
      given: `a) Equivalent circuit of a 1-inch pressure condenser microphone (ignore T(s)). b) Test it with the values of 5.1. c) Adjust the response to be as flat as possible. Keep the circuit — Lab C and the next problems reuse it.`,
      hint: `The coupling constant <span class="m">E/x_0</span> carries a <span class="m">1/j\\omega</span> that Bl never had. Move it into the neighbouring capacitor: sense the voltage <em>across</em> C<sub>E0</sub> (already <span class="m">i/j\\omega C_{E0}</span>) and the current through the C<sub>MD</sub> branch, and the sources become frequency-independent.`,
      sol: `<p><b>a)</b> Electrical: bias through the large R₁, capsule <span class="m">C_{E0}</span> in series with the source <span class="m">(E/j\\omega x_0)\\,u_D</span>, load <span class="m">R_L'</span>. Mechanical (mobility): node u<sub>D</sub> with <span class="m">M_{MD}</span> as a capacitor, <span class="m">C_{MD}</span> as an inductor, <span class="m">R_{MD}</span> to ground, driven by <span class="m">S_D p_D</span> and by the electrostatic reaction <span class="m">-(E/j\\omega x_0)\\,i</span>. Acoustic (impedance): <span class="m">p_i \\to M_{A1} \\to</span> diaphragm <span class="m">\\to R_{AS} \\to M_{AS} \\to C_{AB2}</span> to ground, with the tiny C<sub>AB1</sub> at the diaphragm node.</p>
<p><b>b)</b> Flat-band 9.8 mV/Pa, peak 23.8 mV/Pa just below 10.6 kHz (Q = 2.4 &gt; 1/√2 so it peaks at <span class="m">f_0\\sqrt{1 - 1/2Q^2}</span>), then −12 dB/oct. The vault's KiCad sheet agrees with the 5.1 formula to 0.004 dB in band.</p>
<p><b>c)</b> The knob is the back-plate damping <span class="m">R_{AS}</span>: raise it until Q ≈ 0.7 and the peak is gone at the cost of a slightly earlier roll-off. The load resistor only matters at the bottom: <span class="m">1/(2\\pi R_L' C_{E0})</span> is 2.8 Hz at 500 MΩ, far below the band — drop R<sub>L</sub>′ to 1 MΩ and the bass droops. Parts d) and e) (the T(s) pressure build-up and the final optimisation) are lecture 6 material.</p>`,
      bench: "#bench-condenser", benchLabel: "raise R_AS on the condenser designer until the hump is gone",
    },
  ],
  "6": [
    {
      id: "Sheet 6 · 1", title: "Uncertainty of a condenser microphone's sensitivity (GUM)", tag: "∂M/∂C_MD = 2.370·10³ · u_c(M) = 0.948 mV/Pa",
      given: `a) Write the pressure sensitivity M from theory and find the GUM <b>sensitivity coefficients</b> for the diaphragm's mass, damping and compliance (<span class="mono">M<sub>MD</sub>, R<sub>MD</sub>, C<sub>MD</sub></span>); ignore other contributions. b) Numerical values for the Problems 5 microphone. c) Combined standard uncertainty with no correlation and standard deviations of 10 % of the given values. d) Comment on the hypotheses.`,
      hint: `<span class="m">M = E S_D C_{MT}/x_0</span> with <span class="m">1/C_{MT} = 1/C_{MD} + S_D^2/C_{AB}</span>. Which of the three quantities appear at all? Use the quotient rule on <span class="m">C_{MT}</span>.`,
      sol: `<div class="M">\\frac{\\partial M}{\\partial M_{MD}} = 0, \\qquad \\frac{\\partial M}{\\partial R_{MD}} = 0, \\qquad \\frac{\\partial M}{\\partial C_{MD}} = \\frac{\\partial M}{\\partial C_{MT}}\\frac{\\partial C_{MT}}{\\partial C_{MD}} = \\frac{E S_D}{x_0}\\cdot\\frac{1}{C_{MD}^2\\left(\\dfrac{1}{C_{MD}} + \\dfrac{S_D^2}{C_{AB}}\\right)^2}</div>
<p><b>b)</b> <span class="m">E S_D/x_0 = 2544.7</span>, <span class="m">1/C_{MD} + S_D^2/C_{AB} = 2.5904\\times10^5</span>:</p>
<div class="M">\\frac{\\partial M}{\\partial C_{MD}} = 2544.7 \\times \\frac{6.25\\times10^{10}}{6.710\\times10^{10}} = 2.370\\times10^{3}\\ \\frac{\\text{V/Pa}}{\\text{m/N}}</div>
<div class="M">\\text{c)}\\quad u_c(M) = \\sqrt{\\left[\\frac{\\partial M}{\\partial C_{MD}}\\,(0.1\\,C_{MD})\\right]^2} = 2370 \\times 4\\times10^{-7} = 0.948\\ \\text{mV/Pa}</div>
<p><b>d)</b> Too simplistic, valid only as an exercise. The condenser microphone is a highly coupled system: a change of <span class="m">C_{MD}</span> changes the static deflection and therefore <span class="m">x_0</span> — the two are correlated, and the neglected inputs (E, x₀, S_D, the static pressure in C_AB) are not negligible in a real budget.</p>`,
      bench: "#bench-uncertainty", benchLabel: "the budget bench starts on this case; add x₀ and a correlation to see 1d",
    },
    {
      id: "Sheet 6 · 2", title: "The same uncertainties in LTspice", tag: "M₂₅₀ = 9.6 mV/Pa · ±10 % C_MD → +0.922 / −0.929 mV/Pa",
      given: `Use the circuit of Problems 5 Q2b. a) Read M at 250 Hz with a cursor (linear axis). b) Get f₀ and Q from the simulated modulus and phase with the slide method; compare with theory. c) Vary <span class="mono">M<sub>MD</sub>, R<sub>MD</sub>, C<sub>MD</sub></span> by 10 % and watch M₂₅₀. d) What do those changes do to the overall response, and does the free-field generator Gpb matter?`,
      hint: `f₀ is where the phase has dropped 90° from its mid-band value; Q is the <em>linear</em> ratio of the response there to the flat band. For c) a <span class="mono">.step param</span> with 0.9 / 1 / 1.1 does all three runs at once.`,
      sol: `<p><b>a)</b> <span class="m">M_{250} = 9.6</span> mV/Pa, very close to the 9.8 predicted in Problems 5. <b>b)</b> Should reproduce 10.6 kHz and Q ≈ 2.4 if the circuit holds the same components.</p>
<p><b>c)</b> With Gpb deactivated, ±10 % on M<sub>MD</sub> and R<sub>MD</sub> changes M₂₅₀ negligibly; ±10 % on C<sub>MD</sub> gives <b>+0.922 and −0.929 mV/Pa</b>, matching the 0.948 of 1c (finite differences on a slightly curved function are asymmetric).</p>
<p><b>d)</b> With Gpb working the mid-band result is the same: the free-field correction only acts at high frequency and cannot reach down to 250 Hz. But the three parameters do matter elsewhere: <b>at and above resonance the response is governed by mass and damping, below it by compliance</b>.</p>`,
      bench: "#bench-freefield", benchLabel: "pressure vs free-field bench: the two curves coincide at 250 Hz",
    },
    {
      id: "Sheet 6 · 3", title: "Pistonphone and sound calibrator", tag: "U_i into C_A ∥ Z_A · large cavity · two resonances tuned to the calibration frequency",
      given: `A rigid piston oscillates at fixed frequency and amplitude at one end of a cylindrical cavity; a pressure microphone closes the other end. With the diaphragm blocked the cavity compliance is <span class="m">C_A = V/\\gamma p_s = V/\\rho c^2</span>. a) Equivalent impedance analogy. b) The ideal pistonphone gives the same pressure for any microphone and environment: what does that demand? c–d) A commercial calibrator: a piezo-driven diaphragm (pressure source p<sub>a</sub> with internal M<sub>a</sub>, R<sub>a</sub>, C<sub>a</sub>), a front volume at the microphone, and a long narrow tube to the volume behind the diaphragm. Sketch it and draw the analogy.`,
      hint: `Is a heavy cam-driven piston closer to a pressure source or a volume-velocity source? Then every enclosed volume is a capacitor to ground, every narrow tube an inductor.`,
      sol: `<p><b>a)</b> The pistonphone is a heavy, strong construction, so its volume velocity is independent of the load: a current source <span class="m">U_i</span> feeding <span class="m">C_A</span> in parallel with the microphone's <span class="m">Z_A</span>, both to ground.</p>
<div class="M">\\text{b)}\\quad p = \\left(\\frac{1}{j\\omega C_A} \\,\\Big\\|\\, Z_A\\right) U_i, \\qquad Z_A \\gg \\frac{1}{\\omega C_A} \;\\Rightarrow\; C_A \\gg \\frac{1}{Z_A\\,\\omega}</div>
<p>The larger the volume, the less the pressure depends on the microphone — but the cavity must stay sufficiently smaller than the wavelength.</p>
<p><b>c–d)</b> Series branch <span class="m">p_a</span> – <span class="m">M_{as}</span> – <span class="m">R_{as}</span> – <span class="m">C_{as}</span> into the front-volume node (compliance to ground, microphone <span class="m">Z_a</span> in parallel); from there the narrow tube <span class="m">M_{ah}</span> to the rear-volume node with <span class="m">C_{a3}</span> to ground. Two resonances: piston and suspension (<span class="m">M_{as}, C_{as}</span>) and the Helmholtz resonance (<span class="m">M_{ah}, C_{a3}</span>). Tuned to the calibration frequency, they make the calibrator's source impedance very small — the "low internal impedance" a level calibrator needs, achieved in a pocket-sized device.</p>`,
      bench: "#bench-pistonphone", benchLabel: "pistonphone bench: cavity volume vs microphone equivalent volume",
    },
  ],
};

/* ---------- renderer ---------- */
function renderProblems() {
  for (const [lec, list] of Object.entries(window.PROBLEMS || {})) {
    const root = document.getElementById(`problems-${lec}`);
    if (!root) continue;
    root.classList.add("problems");
    root.append(h("h3", {}, h("span", { class: "eyebrow" }, `Problems · ${/^\d+$/.test(lec) ? "lecture" : "lab"} ${lec}`), "Problems and solutions"));
    root.append(h("p", { class: "small" }, "Open a problem, try it, then open the hint before the solution. Answers in the header are the official ones."));
    for (const p of list) {
      const body = h("div", { class: "pbody" });
      body.append(h("div", { class: "pgiven", html: p.given }));
      if (p.hint) body.append(h("details", { class: "phint" }, h("summary", {}, "Hint"), h("div", { html: p.hint })));
      body.append(h("details", { class: "psol" }, h("summary", {}, "Solution"), h("div", { html: p.sol })));
      if (p.bench) body.append(h("a", { class: "pbench", href: p.bench }, `Try it on the bench → ${p.benchLabel || ""}`));
      const d = h("details", { class: "prob" }, h("summary", {}, h("span", { class: "pid" }, p.id), h("span", { class: "pt" }, p.title), h("span", { class: "pans" }, p.tag)), body);
      root.append(d);
    }
    renderMath(root);
  }
}
document.addEventListener("DOMContentLoaded", renderProblems);
