-- 4-to-1-Line Multiplexer: Structural VHDL Description -- 1
-- (See Figure 3-25 for logic diagram) -- 2
library ieee, lcdf_vhdl; -- 3
use ieee.std_logic_1164.all, lcdf_vhdl.func_prims.all; -- 4
entity multiplexer_4_to_1_st is -- 5
port (S: in std_logic_vector(0 to 1); -- 6
 I: in std_logic_vector(0 to 3); -- 7
 Y: out std_logic); -- 8
end multiplexer_4_to_1_st; -- 9
 --10
architecture structural_2 of multiplexer_4_to_1_st is --11
component NOT1 --12
port(in1: in std_logic; --13
 out1: out std_logic); --14
end component; --15
component AND2 --16
port(in1, in2: in std_logic; --17
 out1: out std_logic); --18
end component; --19
component OR4 --20
port(in1, in2, in3, in4: in std_logic; --21
 out1: out std_logic); --22
end component; --23
signal S_n: std_logic_vector(0 to 1); --24
signal D, N: std_logic_vector(0 to 3); --25
begin --26
 g0: NOT1 port map (S(0), S_n(0)); --27
 g1: NOT1 port map (S(1), S_n(1)); --28
 g2: AND2 port map (S_n(1), S_n(0), D(0)); --29
 g3: AND2 port map (S_n(1), S(0), D(1)); --30
 g4: AND2 port map (S(1), S_n(0), D(2)); --31
 g5: AND2 port map (S(1), S(0), D(3)); --32
 g6: AND2 port map (D(0), I(0), N(0)); --33
 g7: AND2 port map (D(1), I(1), N(1)); --34
 g8: AND2 port map (D(2), I(2), N(2)); --35
 g9: AND2 port map (D(3), I(3), N(3)); --36
 g10: OR4 port map (N(0), N(1), N(2), N(3), Y); --37
end structural_2; 