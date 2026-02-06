----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 01/30/2020 03:41:04 PM
-- Design Name: 
-- Module Name: tb_testFF4bit1 - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.Std_logic_1164.all;
use IEEE.Numeric_Std.all;

entity testFF4bit_tb is
end;

architecture bench of testFF4bit_tb is

  component testFF4bit
   Port ( d : in STD_LOGIC_VECTOR (3 downto 0);
              q : out STD_LOGIC_VECTOR (3 downto 0);
              clk : in STD_LOGIC);
  end component;

  signal d: STD_LOGIC_VECTOR (3 downto 0);
  signal q: STD_LOGIC_VECTOR (3 downto 0);
  signal clk: STD_LOGIC;
constant clk_period : time:= 10 ns;
  signal endtest: std_logic:= '0';
begin

  uut: testFF4bit port map ( d   => d,
                             q   => q,
                             clk => clk );

clock: process
                           begin
                          while endtest='0'  loop
                          clk<='0';
                          wait for clk_period/2;
                          clk<='1';
                           wait for clk_period/2;
                           end loop;
                              wait;
                           end process;


  stimulus: process
  begin
  
  d<="1010"; wait for clk_period;
  d<="1011"; wait for clk_period;
    -- Put initialisation code here


    -- Put test bench stimulus code here
endtest<='1';
    wait;
  end process;


end;
