#!/usr/bin/env python
import os
import sys
import fnmatch
import argparse
import bisect
import collections

'''
addr_map is a mapping from addr to access list.

access list is implemented by OrderedDict.
the format is
(access #, (tid, time, time_diff, log, mem, mem_diff))

'''
addr_dict = collections.OrderedDict()
addr_map = {}
tid_pos = 0
time_pos = 1
diff_pos = 2
content_pos = 3
mem_pos = 4
mdiff_pos = 5
curr_ac_pos = 6
prev_ac_pos = 7
location_pos = 8

verbose = 0

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
	need_save_curr = 0
	need_save_prev = 0
	location = ""
	while True:
		line = fin.readline()
		if not line:
			break;

	
		if (parse_state == state.STARTED):
			content = content + line

		if need_save_curr:
			curr_access = line.strip()
			need_save_curr = 0
		if need_save_prev:
			prev_access = line.strip()
			need_save_prev = 0

		if line[0] == "=":
			if parse_state == state.NONE:
				parse_state = state.STARTED
				isFirstRace = 0
				tid = 0
				addr = 0
				content = line
				curr_mem = 0
				curr_access = ""
				prev_access = ""
				need_save_curr = 0
				need_save_prev = 0
				location = ""
			elif parse_state == state.STARTED:
				parse_state = state.NONE
				
		if "  Write of size" in line:
			need_save_curr = 1
			line_split = line.split()
			addr = line_split[5]
			tid = line_split[8][:-1]
			if not addr_map.get(addr):
				isFirstRace = 1

		if "  Read of size" in line:
			need_save_curr = 1
			line_split = line.split()
			addr = line_split[5]
			tid = line_split[8][:-1]
			if not addr_map.get(addr):
				isFirstRace = 1

		if "  Previous " in line:
			need_save_prev = 1
			prev_access = line
			line_split = line.split()
			prev_tid = line_split[9][:-1]

		if "Location is " in line:
			location = line.strip()

		if "Memory allocated" in line:
			line_split = line.split(" ")
			curr_mem= int(line_split[2])

		if "Report Timestamp" in line:
			line_split = line.split(" ")
			curr_ts = float(line_split[2])
			prev_ts = curr_ts
			prev_mem = curr_mem
			bk = 0
			if isFirstRace == 0:
				old_dict =  addr_map[addr]
				for item in reversed(old_dict.items()):
					if item[1][tid_pos] == tid:
						prev_ts = item[1][time_pos]
						prev_mem = item[1][mem_pos]
						prev_access = item[1][curr_ac_pos]
						bk = 1
						break;
				if bk == 0:
					print "\n\n\n\n prev not found \n\n\n"
					sys.exit(0)


			diff_ts = curr_ts - prev_ts
			diff_mem = curr_mem - prev_mem

			if isFirstRace == 1:
				#print "The first race"
				newdict = collections.OrderedDict()
				newdict[len(newdict)] = (prev_tid, curr_ts, diff_ts, "", curr_mem, 0, prev_access, "", location)

				newdict[len(newdict)] = (tid, curr_ts, diff_ts, content, curr_mem, 0, curr_access, "", location)
				addr_map[addr] = newdict
				#print addr_map[addr]
			else:
				old_dict =  addr_map[addr]
				#print "Existing race"
				if diff_ts == 1.003:
					sys.exit(0)
				old_dict[len(old_dict)] = (tid, curr_ts, diff_ts, content, curr_mem, diff_mem, curr_access, prev_access, location)
				#print old_dict

	fin.close()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", help="input file", action='store', dest='input_file')
	parser.add_argument("-o", "--output", help="output file", action='store_true')
	parser.add_argument("-v", "--verbose", help="verbose mode", action='store_true')
	args = parser.parse_args()

	if args.input_file:
		filename = args.input_file
		print filename
	else:
		filename = "report"
	#	print "default file is report"

	if args.verbose:
		verbose = 1
	else:
		verbose = 0
	
	reorderReport(filename)

	combinedDict=collections.OrderedDict()

	# Merge the accesses across addresses
	i = 0
	for item in addr_map:
		for access in addr_map[item]:
			combinedDict[i] = addr_map[item][access]
			i += 1

	i = 0
	foo = collections.OrderedDict(reversed(sorted(combinedDict.iteritems(), key=lambda x:x[1][2])))
	for item_foo in foo:
		if foo[item_foo][content_pos] != "":
			if foo[item_foo][prev_ac_pos] !="":
				i += 1
				print "<------------- Window %d ------------->"%i
				print foo[item_foo][location_pos]
				print "Window size is %.3f sec"%foo[item_foo][diff_pos]
				if foo[item_foo][mdiff_pos] != 0:
					print "Mem alloc %d bytes"%foo[item_foo][mdiff_pos]
				print "Current Access: ", foo[item_foo][curr_ac_pos]
				print "Previous Access: ", foo[item_foo][prev_ac_pos]
				if verbose :
					print "  <---------- TSAN report ----------->"
					print foo[item_foo][content_pos]
				print ""

	print "There are", i, "windows"
#	print addr_map
	'''
	for item in addr_map:
#		print item
#		print	addr_map[item]
		foo = collections.OrderedDict(reversed(sorted(addr_map[item].iteritems(), key=lambda x:x[1][2])))
		for item_foo in foo:
			if foo[item_foo][content_pos] != "":
				print "Window size is %.3f sec"%foo[item_foo][diff_pos]
				if foo[item_foo][mdiff_pos] != 0:
					print "Mem alloc %d bytes"%foo[item_foo][mdiff_pos]
				print foo[item_foo][content_pos]
	'''


	sys.exit(0)

if __name__ == '__main__':
	main()

