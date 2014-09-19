import sys
sys.dont_write_bytecode = True

import Map

current_room = Map.woods
while True:
	next_room = current_room.enter()
	current_room = next_room