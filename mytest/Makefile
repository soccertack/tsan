all: dataflow
	../../../../../build/bin/clang++ simple_race.cc -fsanitize=thread -fPIE -pie -g
	../../../../../build/bin/clang many_races.c -fsanitize=thread -g -o many_races 

dataflow:
	../../../../../build/bin/clang -fsanitize=dataflow test_dfsan.c -o test_dfsan
	../../../../../build/bin/clang -emit-llvm -fsanitize=dataflow test_dfsan.c -o test_dfsan.ll -S
	../../../../../build/bin/clang -emit-llvm -fsanitize=dataflow input_controlled_loop.c -o input_controlled_loop.ll -S -g
	../../../../../build/bin/opt -load ../../../../../build/lib/PrintAccesses.so -WindowDataFlow -stats -WindowBeginLine=19 -WindowEndLine=32 input_controlled_loop.ll -S > input_controlled_loop_instrumented.ll
	../../../../../build/bin/clang -fsanitize=dataflow -emit-llvm ../../../../../lib/Transforms/PrintAccess/runtime/runtime.c -o runtime_dataflowed.ll -S
	../../../../../build/bin/llvm-link input_controlled_loop_instrumented.ll runtime_dataflowed.ll -S > linked.ll
	../../../../../build/bin/clang -fsanitize=dataflow linked.ll -o linked

ori:
	../../../../../build_ori/bin/clang++ simple_race.cc -fsanitize=thread -fPIE -pie -g
	../../../../../build_ori/bin/clang many_races.c -fsanitize=thread -g -o  many_races
run:
	! ./a.out 2>report
	./reorder.py

clean:
	rm ./a.out
	rm ./many_races

