-- adder_4_top.vhd
-- Top-level wrapper for 4-bit structural adder on Nexys 4 DDR
-- SW(0-3) = A, SW(4-7) = B, BTNC = carry-in
-- LED(0-3) = sum, LED(4) = carry-out

library ieee;
use ieee.std_logic_1164.all;

entity adder_4_top is
    port (
        SW   : in  std_logic_vector(7 downto 0);
        BTNC : in  std_logic;
        LED  : out std_logic_vector(4 downto 0)
    );
end adder_4_top;

architecture structural of adder_4_top is

    component adder_4
        port (
            B  : in  std_logic_vector(3 downto 0);
            A  : in  std_logic_vector(3 downto 0);
            C0 : in  std_logic;
            S  : out std_logic_vector(3 downto 0);
            C4 : out std_logic
        );
    end component;

begin

    UUT: adder_4
        port map (
            B  => SW(7 downto 4),
            A  => SW(3 downto 0),
            C0 => BTNC,
            S  => LED(3 downto 0),
            C4 => LED(4)
        );

end structural;
