all:
	../../../../../build/bin/clang++ simple_race.cc -fsanitize=thread -fPIE -pie -g
	../../../../../build/bin/clang four_races.c -fsanitize=thread -g -o four_races
ori:
	../../../../../build_ori/bin/clang++ simple_race.cc -fsanitize=thread -fPIE -pie -g
	../../../../../build_ori/bin/clang four_race.c -fsanitize=thread -g -o four_races
clean:
	rm ./a.out
	rm ./four_races

