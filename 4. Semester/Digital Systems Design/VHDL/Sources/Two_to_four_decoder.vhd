–– 2-to-4-Line Decoder with Enable: Structural VHDL Description –– 1
–– (See Figure 3-16 for logic diagram) –– 2
library ieee, lcdf_vhdl; –– 3
use ieee.std_logic_1164.all, lcdf_vhdl.func_prims.all; –– 4
entity decoder_2_to_4_w_enable is –– 5
port (EN, A0, A1: in std_logic; –– 6
 D0, D1, D2, D3: out std_logic); –– 7
end decoder_2_to_4_w_enable; –– 8
 –– 9
architecture structural_1 of decoder_2_to_4_w_enable is –– 10
component NOT1 –– 11
port (in1: in std_logic; –– 12
 out1: out std_logic); –– 13
end component; –– 14
component AND2 –– 15
port (in1, in2: in std_logic; –– 16
 out1: out std_logic); –– 17
end component; –– 18
signal A0_n, A1_n, N0, N1, N2, N3: std_logic; –– 19
begin –– 20
 g0: NOT1 port map (in1 => A0, out1 => A0_n); –– 21
 g1: NOT1 port map (in1 => A1, out1 => A1_n); –– 22
 g2: AND2 port map (in1 => A0_n, in2 => A1_n, out1 => N0); –– 23
 g3: AND2 port map (in1 => A0, in2 => A1_n, out1 => N1); –– 24
 g4: AND2 port map (in1 => A0_n, in2 => A1, out1 => N2); –– 25
 g5: AND2 port map (in1 => A0, in2 => A1, out1 => N3); –– 26
 g6: AND2 port map (in1 => EN, in2 => N0, out1 => D0); –– 27
 g7: AND2 port map (in1 => EN, in2 => N1, out1 => D1); –– 28
 g8: AND2 port map (in1 => EN, in2 => N2, out1 => D2); –– 29
 g9: AND2 port map (in1 => EN, in2 => N3, out1 => D3); –– 30
end structural_1;