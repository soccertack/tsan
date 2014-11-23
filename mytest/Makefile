all:
	../llvm/build/bin/clang++ simple_race.cc -fsanitize=thread -fPIE -pie -g
ori:
	../llvm_ori/build/bin/clang++ simple_race.cc -fsanitize=thread -fPIE -pie -g
clean:
	rm ./a.out

