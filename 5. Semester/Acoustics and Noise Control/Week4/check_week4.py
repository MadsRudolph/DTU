"""Independent SI calculations for 34840 Week 4. Run with Python 3, no packages."""
import json
from math import pi, sqrt, log10
from pathlib import Path

rho, c, z, pref = 1.2, 343, 413, 20e-6
spl = lambda p: 20 * log10(p / pref)
pmax, pmin = [pref * 10 ** (v / 20) for v in (85, 74)]
s = pmax / pmin
alpha = 1 - ((s - 1) / (s + 1)) ** 2
S = pi * (0.15 / 2) ** 2
ma, ka = 0.020 / S**2, rho * c**2 / 0.016
power4 = 0.01 * pmax * pmin / z
tau = 4 * z * 1.48e6 / (z + 1.48e6) ** 2
out = {
    'bottle_hz': c / (2*pi) * sqrt(pi*0.01**2 / (400e-6 * 0.021)),
    'plane_power_w': 10 * (pref * 10**(82/20))**2 / z,
    'transmission_fraction': tau,
    'transmission_attenuation_db': -10*log10(tau),
    'tube_alpha': alpha,
    'tube_absorbed_w': power4,
    'tube_power_db': 10*log10(power4/1e-12),
    'cone_acoustic_mass': ma, 'cabinet_acoustic_stiffness': ka,
    'cabinet_hz': sqrt(ka/ma)/(2*pi),
    'cabinet_spl': spl(ka*S*0.002/sqrt(2)),
    'exam_net_intensity': 1e-6/(pi*0.05**2),
    'exam_max_spl': spl(sqrt(z*1e-5/(pi*0.05**2))*(1+sqrt(0.9))),
    'octave_levels': [10*log10(10**5.6+10**5.8),60,10*log10(10**6.2+10**6.4),66],
    'distances_m': [10**((64-L)/20) for L in [70,61,44]],
    'mc_absorption': 1-10**((70-90)/10),
}
for key, expected, tolerance in [
    ('bottle_hz',334,0.5),('plane_power_w',1.54e-3,0.01e-3),
    ('transmission_attenuation_db',30,0.6),('tube_alpha',0.69,0.005),
    ('tube_absorbed_w',0.87e-6,0.01e-6),('tube_power_db',59.4,0.1),
    ('cabinet_hz',59,0.5),('cabinet_spl',140.9,0.1),
    ('exam_max_spl',97,0.1)]:
    assert abs(out[key]-expected) < tolerance, (key,out[key],expected)
assert abs(tau + ((1.48e6-z)/(1.48e6+z))**2 - 1) < 1e-12
assert abs(power4-alpha*0.01*((pmax+pmin)/2)**2/z) < 1e-18
assert abs(ma*S*S-0.020) < 1e-15
print(json.dumps(out, indent=2))
Path(__file__).with_name('answers.json').write_text(json.dumps(out, indent=2)+'\n')
