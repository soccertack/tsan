all:
	../../../../../build/bin/clang++ simple_race.cc -fsanitize=thread -fPIE -pie -g
	../../../../../build/bin/clang many_races.c -fsanitize=thread -g -o many_races 
ori:
	../../../../../build_ori/bin/clang++ simple_race.cc -fsanitize=thread -fPIE -pie -g
	../../../../../build_ori/bin/clang many_races.c -fsanitize=thread -g -o  many_races
run:
	! ./a.out 2>report
	./reorder.py

clean:
	rm ./a.out
	rm ./many_races

