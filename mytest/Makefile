all: dataflow
	../../../../../build/bin/clang many_races.c -fsanitize=thread -g -o many_races 

dataflow:
	../../../../../build/bin/clang -fsanitize=dataflow test_dfsan.c -o test_dfsan
	../../../../../build/bin/clang -emit-llvm -fsanitize=dataflow test_dfsan.c -o test_dfsan.ll -S
	../../../../../build/bin/clang -emit-llvm -fsanitize=dataflow input_controlled_loop.c -o input_controlled_loop_dataflowed.ll -S -g
	../../../../../build/bin/opt -loops -load ../../../../../build/lib/WindowDataFlow.so -WindowDataFlow -stats -WindowBeginLocation=/home/mateus/reliable/llvm/projects/compiler-rt/lib/tsan/mytest/input_controlled_loop.c:19:5 -WindowEndLocation=/home/mateus/reliable/llvm/projects/compiler-rt/lib/tsan/mytest/input_controlled_loop.c:31:5 input_controlled_loop_dataflowed.ll -S > input_controlled_loop_dataflowed_instrumented.ll
	../../../../../build/bin/clang -fsanitize=dataflow -emit-llvm ../../../../../lib/Transforms/llvm-windowrtl/runtime/runtime.c -o runtime_dataflowed.ll -S
	../../../../../build/bin/llvm-link input_controlled_loop_dataflowed_instrumented.ll runtime_dataflowed.ll -S > input_controlled_loop_linked.ll
	../../../../../build/bin/clang -fsanitize=dataflow input_controlled_loop_linked.ll -o input_controlled_loop

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
	rm ./a.out
	rm ./many_races

