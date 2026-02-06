-- tb_adder_4_top.vhd
-- Testbench for the 4-bit adder top-level wrapper

library ieee;
use ieee.std_logic_1164.all;

entity tb_adder_4_top is
end tb_adder_4_top;

architecture behavior of tb_adder_4_top is

    component adder_4_top
        port (
            SW   : in  std_logic_vector(7 downto 0);
            BTNC : in  std_logic;
            LED  : out std_logic_vector(4 downto 0)
        );
    end component;

    signal SW   : std_logic_vector(7 downto 0) := (others => '0');
    signal BTNC : std_logic := '0';
    signal LED  : std_logic_vector(4 downto 0);

begin

    UUT: adder_4_top
        port map (
            SW   => SW,
            BTNC => BTNC,
            LED  => LED
        );

    stim_proc: process
    begin
        -- Test 1: 0 + 0 + 0 = 0  (S=0000, C4=0)
        SW   <= "00000000";  -- B=0, A=0
        BTNC <= '0';
        wait for 100 ns;
        assert LED = "00000"
            report "Test 1 FAILED: 0+0+0" severity error;

        -- Test 2: 3 + 5 + 0 = 8  (S=1000, C4=0)
        -- A=5 (0101) on SW(3:0), B=3 (0011) on SW(7:4)
        SW   <= "00110101";
        BTNC <= '0';
        wait for 100 ns;
        assert LED = "01000"
            report "Test 2 FAILED: 5+3+0" severity error;

        -- Test 3: 15 + 15 + 1 = 31  (S=1111, C4=1)
        -- A=15 (1111), B=15 (1111), C0=1
        SW   <= "11111111";
        BTNC <= '1';
        wait for 100 ns;
        assert LED = "11111"
            report "Test 3 FAILED: 15+15+1" severity error;

        -- Test 4: 9 + 7 + 1 = 17  (S=0001, C4=1)
        -- A=9 (1001) on SW(3:0), B=7 (0111) on SW(7:4)
        SW   <= "01111001";
        BTNC <= '1';
        wait for 100 ns;
        assert LED = "10001"
            report "Test 4 FAILED: 9+7+1" severity error;

        report "All tests completed." severity note;
        wait;
    end process;

end behavior;
