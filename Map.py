from random import randint
from sys import exit

import sys
sys.dont_write_bytecode = True

import Lib

# This file contains all of the rooms that the player can move between and all of the
# actions that a player can take when he or she is in the rooms.

# This function figures out the order in which the creatures in the room act.
# the list 'rolls' keeps track of the rolls and the dict 'match' makes sure the roll
# is attributed to the correct creature.
def initiative(creature_list):
	rolls = []
	match = {}
	for creature in creature_list:
		roll = randint(1, 20) + creature.initiative
		while roll in rolls:
			# If two initiative rolls are the same, the program needs to decide who goes
			# first.  The following decides tiebreakers. To track tiebreakers I
			# chose to add or subtract a very small number to the initiative
			# rolls.
			if match[roll].initiative == creature.initiative:
				result = randint(0, 1)
				if result == 0:
					roll = roll + .01
				else:
					roll = roll - .01
			elif match[roll].initiative > creature.initiative:
				roll = roll - .01
			else:
				roll = roll + .01
		rolls.append(roll)
		match[roll] = creature
	# sort the list of rolls to go from smallest to largest
	rolls.sort()
	
	# Figure out and return the initiative order.
	n = len(rolls) - 1
	initiative_order = []
	while n >= 0:
		initiative_order.append(match[rolls[n]])
		n = n - 1
	return initiative_order
	
# This function represents what happens when the player attempts to store an item.
def store_fun(loot, loot_names, held_names, armor_names, d):
	print "What do you want to store?"
	target = raw_input("> ")
			
	# The store function in Lib.player.py only works if target is in certain places.
	# This loop forces the player to chose an object in one of those places.	
	while not(
		target in loot_names or target in held_names
		or target in armor_names or target == 'nothing'
	):
		print "You can't store that."
		target = raw_input("> ")
	if target == 'nothing':
		print "Very well."
			
	elif target in loot_names:
		Lib.player.store(d[target], loot, loot)
			
	elif target in held_names:
		Lib.player.store(d[target], [Lib.player.held, 0], loot)
			
	elif target in armor_names:
		Lib.player.store(
			d[target], [Lib.player.armor, d[target].slot], loot
		)
		
# This function represents what happens when the player attempts to equip an item.
def equip_fun(loot, loot_names, bag_names, held_names, armor_names, d):
	print "What do you want to equip?"
	target = raw_input("> ")
			
	# The equip function in Lib.player.py only works if target is in certain places.
	# This loop forces the player to chose an object in one of those places.
	while not(target in loot_names or target in bag_names):
		print "You can't equip that."
		target = raw_input("> ")
	if target == 'nothing':
		print "Very well."
				
	# I may want to change this to something more elegant.  If the player decides to
	# equip 'nothing', then isinsthance(d['nothing'], ...) will return an error.  I need
	# to prevent that.  I also need to sort out whether the equipped item is a weapon
	# or an armor, and that will decide which function from Lib.player I will need.
	if target != 'nothing':
		if isinstance(d[target], Lib.Weapon):
			if d[target] in loot:
				Lib.player.equip(d[target], loot, loot)
			else:
				Lib.player.equip(d[target], Lib.player.bag, loot)
		elif isinstance(d[target], Lib.Armor):
			if d[target] in loot:
				Lib.player.wear(d[target], loot, loot)
			else:
				Lib.player.wear(d[target], Lib.player.bag, loot)
				
# This function represents what happens when the player attempts to drop an item.
def drop_fun(loot, loot_names, bag_names, held_names, armor_names, d):
	print "What do you want to drop?"
	target = raw_input("> ")
				
	# The drop function in Lib.player.py only works if target is in certain places.
	# This loop forces the player to chose an object in one of those places.
	while not(
		target in armor_names or target in held_names
		or target in bag_names or target == 'nothing'
	):
		print "You can't drop that."
		target = raw_input("> ")
	if target == 'nothing':
		print "Very well."
				
	if d[target] in Lib.player.armor:
		Lib.player.drop(
			d[target], [Lib.player.armor,d[target].slot], loot
		)
	elif d[target] in Lib.player.held:
		Lib.player.drop(
			d[target], [Lib.player.held,d[target].slot], loot
		)
	elif d[target] in Lib.player.bag:
		Lib.player.drop(d[target], Lib.player.bag, loot)

# This function represents what happens when the player choses to manage inventory.
def manage_inventory(
	loot, loot_names, bag_names, held_names, armor_names, d
):

	print """
Do you want to 'store', 'equip', or 'drop' an item?  If you don't want any
of the above, say 'done'.
	"""
	action = raw_input("> ")
					
	while not(action in ['store', 'equip', 'drop', 'done']):
		print "Try again."
		action = raw_input("> ")
	if action == 'done':
		print "Very well."
		return action
	elif action == 'store':
		store_fun(loot, loot_names, held_names, armor_names, d)
				
	elif action == 'equip':
		equip_fun(loot, loot_names, bag_names, held_names, armor_names, d)
		
	elif action == 'drop':
		drop_fun(loot, loot_names, bag_names, held_names, armor_names, d)
			
	return action
	
# This function represents what happens when the player choses to check inventory.
def check_inventory():
	arms = {0: 'chest', 1: 'head', 2: 'hands', 3: 'feet', 4: 'back'}
	print "Your armor:"
	n = 0
	while n < 5:
		if Lib.player.armor[n] != None:
			print "You are wearing {0} on your {1}.".format(
				Lib.player.armor[n].name, arms[n]
			)
		else:
			print "You are wearing {0} on your {1}.".format(
				'nothing', arms[n]
			)
		n = n + 1
			
	print "Your held items:"
	hands = {0: 'main', 1: 'off'}
	n = 0
	while n < 2:
		if Lib.player.held[n] != None:
			print "You are holding {0} in your {1} hand.".format(
				Lib.player.held[n].name, hands[n]
			)
		else:
			print "You are holding {0} in your {1} hand.".format(
				'nothing', hands[n]
			)
		n = n + 1
			
	print "The following items are in your bag:"
	for thing in Lib.player.bag:
		print thing.name
				
	print """
Your stats are the following:
\tHit Points: {0}
\tArmor Class: {1}
\tAttack Bonus: {2}
\tDamage Bonus: {3}
\tAttack Die: {4}
	""".format(
		Lib.player.hit_points, Lib.player.ac, Lib.player.att, Lib.player.damage,
		Lib.player.die
	)

# This function runs as soon as the encounter for a room is completed.  It manages all
# of the non-encounter actions that the player can choose.
def action(loot):
	# I made lists containing the names of all of the legal targets for various actions
	# and a dict that matches them with their objects.  This is the best way I found
	# to manage interactions with inputs.
	loot_names = []
	bag_names = []
	held_names = []
	armor_names = []
	d = {}
	for thing in loot:
		loot_names.append(thing.name)
		d[thing.name] = thing
	loot_names.append('nothing')
	for thing in Lib.player.bag:
		bag_names.append(thing.name)
		d[thing.name] = thing
	for thing in Lib.player.held:
		if thing != None:
			held_names.append(thing.name)
			d[thing.name] = thing
	for thing in Lib.player.armor:
		if thing != None:
			armor_names.append(thing.name)
			d[thing.name] = thing
			
	while True:
		print "Do you want to 'search', 'check inventory', 'manage inventory',"
		print "or 'leave'?"
		action = raw_input("> ")
		if action == 'search':
			print "You find:"
			for thing in loot:
				print thing.name
		elif action == 'check inventory':
			check_inventory()
		
		elif action == 'manage inventory':
			while action != 'done':
				action = manage_inventory(
					loot, loot_names, bag_names, held_names, armor_names, d
				)
				
		elif action == 'leave':
			print "There are no other rooms yet.  Try something else."
		else:
			print "That isn't an option.  Try again."

# This is the first room in the fortress.  It has an encounter and then a chance to loot.
class GreatHall(object):

	loot = [Lib.dagger, Lib.leather]
	
	def enter(self):
		print """
You are now in the great hall.  There are two goblins guarding the main entrance
and two doors on the far side of the room.  The guards attack you from the
left and right.
		"""
		gob1 = Lib.Goblin('The Left Guard')
		gob2 = Lib.Goblin('The Right Guard')
		order = initiative([Lib.player, gob1, gob2])
		
		# This code makes lists of legal targets and a dict to match
		targets = []
		d = {}
		for thing in order:
			targets.append(thing.name)
			d[thing.name] = thing
		targets.remove(Lib.player.name)
			
		# This code runs through a combat.  So far, the only action is to attack.
		# I will alter this to include more options later.
		n = 0
		while order != [Lib.player]:
			if order[n].hit_points <= 0:
				dead_thing = order[n].name
				print "{0} is dead.".format(dead_thing)
				targets.remove(order[n].name)
				order.remove(order[n])
			else:
				print "{0} has the initiative.".format(order[n].name)
				choice = order[n].act(targets)
				order[n].attack(d[choice])
				n = n + 1
			if Lib.player.hit_points <= 0:
				print "You are dead."
				exit(1)
			if n >= len(order):
				n = 0
		
		print """
The guards have both fallen.  You don't think you hear any approaching soldiers,
but there are most likely more surprises farther in.  For now, you have a chance
to catch your breath and prepare.
		"""
		# The function action will only return anything if the option 'leave'
		# is chosen.  In this case, next_room will represent the next room.
		next_room = action(self.loot)

great_hall = GreatHall()