library IEEE;
use IEEE.Std_logic_1164.all;
use IEEE.Numeric_Std.all;

entity DataPath_tb is
end;

architecture bench of DataPath_tb is

  component DataPath
      Port ( RESET : in STD_LOGIC;
             CLK : in STD_LOGIC;
             W : in STD_LOGIC;
             DA,AA,BA : in STD_LOGIC_VECTOR (3 downto 0);
             ConstantIn : in STD_LOGIC_VECTOR (7 downto 0);
             MB,MD : in STD_LOGIC;
             FS3,FS2,FS1,FS0 : in STD_LOGIC;
             DataIn :in STD_LOGIC_VECTOR (7 downto 0);
             Address_Out: out STD_LOGIC_VECTOR (7 downto 0);
             Data_Out: out STD_LOGIC_VECTOR (7 downto 0);
             V,C,N,Z : out std_logic);
  end component;

  signal RESET: STD_LOGIC;
  signal CLK: STD_LOGIC;
  signal W: STD_LOGIC;
  signal DA,AA,BA: STD_LOGIC_VECTOR (3 downto 0);
  signal ConstantIn: STD_LOGIC_VECTOR (7 downto 0);
  signal MB,MD: STD_LOGIC;
  signal FS3,FS2,FS1,FS0: STD_LOGIC;
  signal DataIn: STD_LOGIC_VECTOR (7 downto 0);
  signal Address_Out: STD_LOGIC_VECTOR (7 downto 0);
  signal Data_Out: STD_LOGIC_VECTOR (7 downto 0);
  signal V,C,N,Z: std_logic;
  constant clk_period: time:= 10ns;
  signal end_test: std_logic:='1';
  

begin

  uut: DataPath port map ( RESET       => RESET,
                           CLK         => CLK,
                           W           => W,
                           DA          => DA,
                           AA          => AA,
                           BA          => BA,
                           ConstantIn  => ConstantIn,
                           MB          => MB,
                           MD          => MD,
                           FS3         => FS3,
                           FS2         => FS2,
                           FS1         => FS1,
                           FS0         => FS0,
                           DataIn      => DataIn,
                           Address_Out => Address_Out,
                           Data_Out    => Data_Out,
                           V           => V,
                           C           => C,
                           N           => N,
                           Z           => Z );
clock: process
                           begin
                           while end_test='1'loop
                           CLK<='1';
                           wait for clk_period*0.5;
                           CLK<='0';
                           wait for clk_period*0.5;
                           end loop;
                           wait;
                           end  process;


stimulus: process

  variable FS: std_logic_vector(3 downto 0):="0000";    --det skal være en variable -ellers sker der et delay på en clk periode!
    begin
     Reset<='1'; 
                                             -- Put initialisation code here
                        DA<="0000";BA<="0000";AA<="0000";
                        FS0<='0';
                        FS1<='0';
                        FS2<='0';
                        FS3<='0';
                        W<='0';
                        MB<='0';
                        MD<='0';
                        wait for clk_period;
                        Reset<='0'; 
                       wait for clk_period;
                       for i in 0 to 15 loop
                        FS:=std_logic_vector(to_unsigned(i,4));
                       FS0<=FS(0);
                         FS1<=FS(1);
                         FS2<=FS(2);
                         FS3<=FS(3);  
                      
                      if i=0 then
                       
                        
                         datain<="00001010" ;
                        
                           MD<='1';
                           DA<="0000";  --load data into R0
                           W<='1';
                           wait for clk_period*2;
                            W<='0';
                           MD<='0';
                           wait for clk_period;
                           datain<="00011010" ;
                            
                           MD<='1';
                           DA<="0001";  --load data into R1
                           W<='1';
                           wait for clk_period*2;
  
                           MD<='0';
                           w<='0';
                                   
                           BA<="0001";
                                   
                           AA<="0000";
                                  
                           MB<='0';
                           wait for clk_period;
                                  
                           w<='1';    --gem resulat 
                                  
                           DA<="0010";    --result in R2
                           wait for clk_period*2;
                           w<='0'; 
                           BA<="0010";     --fetch data in R2 into B
                           wait for clk_period*2;
                           end if;     --end for i =0 - resten køres nu udenfor if
   --her afvikles nu for fs0 1 til 15 nedenfor
                           AA<="0000";
                           BA<="0001";
                           MB<='0';
                                                         
                           DA<="0010";    --result in R2
                           w<='1';
                           wait for clk_period*2;  
                                                                                 
                           w<='0'; 
                          wait for clk_period;  
                                                      
                    
                        wait for clk_period;
                       end loop;   -- nu er alt testet
                        end_test<='0';
                      wait;
          end  process;        
 


end;
