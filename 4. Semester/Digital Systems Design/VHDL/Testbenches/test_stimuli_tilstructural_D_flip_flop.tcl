restart
add_force SN 0

add_force RN 1

run 10 ns
add_force SN 1

add_force RN 1

run 10ns
add_force RN 0

add_force SN 1

run 10 ns
add_force RN 1

add_force SN 1
run 10 ns

#SR latch med enable
restart

add_force S 0
add_force R 1
add_force C 1

run 10ns
add_force S 0
add_force R 1
add_force C 0

run 10ns
add_force S 1
add_force R 1
add_force C 1

run 10ns
add_force S 1
add_force R 0
add_force C 1

run 10ns


restart
add_force D 0

add_force C 1

run 10 ns
add_force D 1

add_force C 1

run 10ns
add_force C 0

add_force D 1

run 10 ns
add_force D 0
add_force C 1

run 10ns

restart

add_force D 1
run 10 ns
add_force E 0
run 10ns
add_force E 1
run 10 ns
add_force D 0


run 10 ns
add_force E 0




run 10 ns
add_force clk 1
run 10 ns
add_force D 1
run 10ns

restart

add_force D 1
add_force load 0
run 10 ns
add_force clk 0
run 10ns
add_force clk 1
run 10 ns
add_force D 0
add_force load 1

run 10 ns
add_force clk 0




run 10 ns
add_force clk 1
run 10 ns
add_force D 1
run 10 ns
add_force clk 0




run 10 ns
add_force clk 1
run 10 ns














add_force SN 1
run 10 ns
