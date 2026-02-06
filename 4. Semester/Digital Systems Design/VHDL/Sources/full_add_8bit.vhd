----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 01/04/2020 07:14:17 PM
-- Design Name: 
-- Module Name: full_add_8bit - Behavioral
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
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity full_add_8bit is

  generic (width:integer :=7);
    Port ( y : in STD_LOGIC_VECTOR (width downto 0);
           ci : in STD_LOGIC;
           x : in STD_LOGIC_VECTOR (width downto 0);
           sum : out STD_LOGIC_VECTOR (width downto 0);
           co : out STD_LOGIC);
end full_add_8bit;

architecture Behavioral of full_add_8bit is

 component half_add
     Port ( x,y : in STD_LOGIC;
            c,s : out STD_LOGIC);
 end component;
 
  component full_add
     Port ( x,y,ci : in STD_LOGIC;
            co,so : out STD_LOGIC);
 end component;
 signal cc: std_logic_vector(width downto 0);
 
begin

GEN_ADD: for i in 0 to width generate
 
Low_bit: if i=0 generate

        U0:    full_add port map 
        (y(i),x(i),ci,cc(0),sum(i));
     
       end generate Low_bit;
Upper_bits: if (i>0 and i<width) generate 
        UX: full_add port map
        (x(i),y(i),cc(i-1),cc(i),sum(i)); 
    -- (y(i),cc(i-1),x(i),cc(0),sum(i));  
         end generate upper_bits; 
msb: if i=width  generate
       Umsb:full_add port map
      (x(i),y(i),cc(i-1),co,sum(i));   
      -- (y(i),cc(i-1),x(i),co,sum(i));  
        end generate msb;
end generate GEN_ADD;

--co<=cc(7);

end Behavioral;
