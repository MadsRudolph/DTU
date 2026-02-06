# create_project.tcl
# Auto-creates the Vivado project for the 4-bit structural adder
# Usage: source {C:/Users/Mads2/DTU/4. Semester/Digital Systems Design/Vivado/Adder_Test/create_project.tcl}

# -- Paths --
set proj_dir    {C:/Users/Mads2/DTU/4. Semester/Digital Systems Design/Vivado/Adder_Test}
set src_dir     {C:/Users/Mads2/DTU/4. Semester/Digital Systems Design/Vivado/Adder_Test/src}
set sim_dir     {C:/Users/Mads2/DTU/4. Semester/Digital Systems Design/Vivado/Adder_Test/sim}
set vhdl_dir    {C:/Users/Mads2/DTU/4. Semester/Digital Systems Design/VHDL/Sources}

# -- Build full file paths --
set src_file1   [file normalize [file join $vhdl_dir four_bit_structural_adder.vhd]]
set src_file2   [file normalize [file join $src_dir  adder_4_top.vhd]]
set constr_file [file normalize [file join $src_dir  adder_4_top.xdc]]
set sim_file    [file normalize [file join $sim_dir  tb_adder_4_top.vhd]]

# -- Create project (Nexys 4 DDR board, VHDL) --
create_project adder_4_project [file join $proj_dir adder_4_project] -part xc7a100tcsg324-1 -force
set_property board_part digilentinc.com:nexys4_ddr:part0:1.1 [current_project]
set_property target_language VHDL [current_project]

# -- Add design sources --
add_files -norecurse [list $src_file1 $src_file2]

# -- Add constraints --
add_files -fileset constrs_1 -norecurse [list $constr_file]

# -- Add simulation sources --
add_files -fileset sim_1 -norecurse [list $sim_file]

# -- Set top modules --
set_property top adder_4_top [current_fileset]
set_property top tb_adder_4_top [get_filesets sim_1]
set_property top_lib xil_defaultlib [get_filesets sim_1]

# -- Update compile order --
update_compile_order -fileset sources_1
update_compile_order -fileset sim_1

puts "Project created successfully for Nexys 4 DDR (xc7a100tcsg324-1)"
puts "Target language: VHDL"
puts "Next steps: Run Simulation -> Synthesis -> Implementation -> Generate Bitstream"
