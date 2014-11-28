#!/usr/bin/env python
import os
import sys
import fnmatch
import argparse
import bisect
import collections

addr_dict = collections.OrderedDict()
addr_map = {}
tid_pos = 0
time_pos = 1
diff_pos = 2
content_pos = 3
mem_pos = 4
mdiff_pos = 5

def enum(*sequential, **named):
	enums = dict(zip(sequential, range(len(sequential))), **named)
	return type('Enum', (), enums)

class race_rec:
	def __init__(self):
		self.addr = 0
		self.prev = 0
		self.time = 0
		self.curr = 0

'''
"WARNING: ThreadSanitizer: %s (pid=%d)\n", rep_typ_str,
268          (int)internal_getpid());
'''

def timediff(prev_sec_s, prev_nsec_s, curr_sec_s, curr_nsec_s):
	prev_sec = float(prev_sec_s)
	prev_nsec= float(prev_nsec_s)
	curr_sec= float(curr_sec_s)
	curr_nsec= float(curr_nsec_s)

	diff_sec = 0
	diff_nsec = 0

	if (curr_nsec - prev_nsec):
		diff_sec = curr_sec - prev_sec - 1
		diff_nsec = 1000000000 + curr_nsec - prev_nsec
	else:
		diff_sec = curr_sec - prev_sec
		diff_nsec = curr_nsec - prev_nsec
	
	return (diff_sec, diff_nsec)
#	return (2, 233)

'''
	    39         if ((curr_nsecend.tv_nsec-start.tv_nsec)<0) {
		     40                 temp.tv_sec = end.tv_sec-start.tv_sec-1;
		      41                 temp.tv_nsec = 1000000000+end.tv_nsec-start.tv_nsec;
		       42         } else {
			        43                 temp.tv_sec = end.tv_sec-start.tv_sec;
				 44                 temp.tv_nsec = end.tv_nsec-start.tv_nsec;
				  45         }
				   46         return temp;
				    47 }
				    '''



def find_addr(addr):
	idx = 0
	for item in reversed(addr_dict.items()):
		if item[1][2] == addr:
			print item
		'''
		if addr == item[2]
			print "find addr", addr
			return idx
		'''
		idx += 1
	return -1

#state = enum('NONE', 'WARNING_TYPE', 'CURR_ACCESS', 'PREV_ACCESS')
state = enum('NONE', 'STARTED')
def reorderReport(fname):
	fin = open(fname)
	started = 0;
	isFirstRace = 0
	tid = 0
	addr = 0
	parse_state = state.NONE
	while True:
		line = fin.readline()
		if not line:
			break;

		if (parse_state == state.STARTED):
			content = content + line
		if line[0] == "=":
			if parse_state == state.NONE:
				parse_state = state.STARTED
				isFirstRace = 0
				tid = 0
				addr = 0
				content = line
				curr_mem = 0
			elif parse_state == state.STARTED:
				parse_state = state.NONE
				
		if "  Write of size" in line:
			line_split = line.split()
		#	print "addr:", line_split[5]
			addr = line_split[5]
			tid = line_split[8][:-1]
			if not addr_map.get(addr):
				isFirstRace = 1

		if "  Previous " in line:
			line_split = line.split()
			prev_tid = line_split[9][:-1]
		if "Memory allocated" in line:
			line_split = line.split(" ")
			curr_mem= int(line_split[2])

		if "Report Timestamp" in line:
			line_split = line.split(" ")
			curr_ts = float(line_split[2])
			prev_ts = curr_ts
			prev_mem = curr_mem
			if isFirstRace == 0:
				old_dict =  addr_map[addr]
				for item in reversed(old_dict.items()):
					if item[1][tid_pos] == tid:
						prev_ts = item[1][time_pos]
						prev_mem = item[1][mem_pos]
						break;

			diff_ts = curr_ts - prev_ts
			diff_mem = curr_mem - prev_mem

			if isFirstRace == 1:
				#print "The first race"
				newdict = collections.OrderedDict()
				newdict[len(newdict)] = (prev_tid, curr_ts, diff_ts, "", curr_mem, 0)
				newdict[len(newdict)] = (tid, curr_ts, diff_ts, content, curr_mem, 0)
				addr_map[addr] = newdict
				#print addr_map[addr]
			else:
				old_dict =  addr_map[addr]
				#print "Existing race"
				old_dict[len(old_dict)] = (tid, curr_ts, diff_ts, content, curr_mem, diff_mem)
				#print old_dict

	fin.close()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", help="input file", action='store', dest='input_file')
	parser.add_argument("-o", "--output", help="output file", action='store_true')
	args = parser.parse_args()

	if args.input_file:
		filename = args.input_file
		print filename
	else:
		filename = "report"
	#	print "default file is report"
	
	reorderReport(filename)

#	for item in reversed(newdict.items()):

#	print addr_map
	for item in addr_map:
#		print item
#		print	addr_map[item]
		foo = collections.OrderedDict(reversed(sorted(addr_map[item].iteritems(), key=lambda x:x[1][2])))
		for item_foo in foo:
			print "Window size is %.3f sec"%foo[item_foo][diff_pos]
			if foo[item_foo][mdiff_pos] != 0:
				print "Mem alloc %d bytes"%foo[item_foo][mdiff_pos]
			print foo[item_foo][content_pos]

	sys.exit(0)

if __name__ == '__main__':
	main()

