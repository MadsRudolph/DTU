–– 2-to-4-Line Decoder: Dataflow VHDL Description –– 1
–– (See Figure 3-16 for logic diagram) –– 2
–– Use library, use, and entity entries from 2_to_4_decoder_st; –– 3
 –– 4
architecture dataflow_1 of decoder_2_to_4_w_enable is –– 5
 –– 6
signal A0_n, A1_n: std_logic; –– 7
begin –– 8
 A0_n <= not A0; –– 9
 A1_n <= not A1; –– 10
 D0 <= A0_n and A1_n and EN; –– 11
 D1 <= A0 and A1_n and EN; –– 12
 D2 <= A0_n and A1 and EN; –– 13
 D3 <= A0 and A1 and EN; –– 14
end dataflow_1; 