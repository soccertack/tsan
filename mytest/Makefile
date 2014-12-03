all: dataflow
	../../../../../build/bin/clang many_races.c -fsanitize=thread -g -o many_races 

dataflow:
	../../../../../build/bin/clang -emit-llvm input_controlled_loop.c -o input_controlled_loop.ll -S -g
	../../../../../build/bin/opt -load ../../../../../build/lib/WindowDataFlow.so -WindowDataFlow -stats -WindowBeginLocation=/home/mateus/reliable/llvm/projects/compiler-rt/lib/tsan/mytest/input_controlled_loop.c:19:5 -WindowEndLocation=/home/mateus/reliable/llvm/projects/compiler-rt/lib/tsan/mytest/input_controlled_loop.c:32:5 input_controlled_loop.ll -S > input_controlled_loop_instrumented.ll
	../../../../../build/bin/clang -emit-llvm ../../../../../lib/Transforms/llvm-windowrtl/runtime/runtime.c -o runtime.ll -S
	../../../../../build/bin/llvm-link input_controlled_loop_instrumented.ll runtime.ll -S > input_controlled_loop_linked.ll
	../../../../../build/bin/opt -dfsan -dfsan-abilist=/home/mateus/reliable/llvm/build/bin/../lib/clang/3.6.0/dfsan_abilist.txt input_controlled_loop_linked.ll -S > input_controlled_loop_linked_dataflowed.ll
	../../../../../build/bin/clang -fsanitize=dataflow input_controlled_loop_linked_dataflowed.ll -o input_controlled_loop

dataflowtest:
	../../../../../build/bin/clang -emit-llvm test_dfsan.c -o test_dfsan.ll -S -g -v
	../../../../../build/bin/opt -dfsan -dfsan-abilist=/home/mateus/reliable/llvm/build/bin/../lib/clang/3.6.0/dfsan_abilist.txt test_dfsan.ll -S > test_dfsan_dataflowed.ll 
	../../../../../build/bin/clang -fsanitize=dataflow test_dfsan_dataflowed.ll -o test_dfsan -v
	#../../../../../build/bin/clang -emit-llvm -fsanitize=dataflow test_dfsan.c -o test_dfsan.ll -S -g -v
	#../../../../../build/bin/clang -fsanitize=dataflow test_dfsan.ll -o test_dfsan

test: dataflow
	./input_controlled_loop 5 | grep yes | wc -l
	./input_controlled_loop 10 | grep yes | wc -l
	./input_controlled_loop 100 | grep yes | wc -l

ori:
	../../../../../build_ori/bin/clang++ simple_race.cc -fsanitize=thread -fPIE -pie -g
	../../../../../build_ori/bin/clang many_races.c -fsanitize=thread -g -o  many_races

simple:
	../../../../../build/bin/clang++ simple_race.cc -fsanitize=thread -fPIE -pie -g
run:
	! ./a.out 2>report
	./reorder.py

clean:
	rm *.ll
	rm ./many_races
	rm ./a.out

