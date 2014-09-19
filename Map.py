from random import randint
from sys import exit

import sys
sys.dont_write_bytecode = True

import Lib

# This file contains all of the rooms that the player can move between and all of the
# actions that a player can take when he or she is in the rooms.

# A global variable
d = {}

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
	
# This function details what happens when the player uses a special item
def special_fun(n, targets, d1, held_names, armor_names, d2):

	# First report to the player what special items are available.
	special_items = []
	for thing in held_names:
		if isinstance(d2[thing], Lib.SpecialItem):
			special_items.append(thing)
	for thing in armor_names:
		if isinstance(d2[thing], Lib.SpecialItem):
			special_items.append(thing)
	print "You have the following special items equipped:"
	for thing in special_items:
		print thing
		
	# Once the player gets a look at the items that are available, he or she
	# can pick which one or nothing.  If nothing is chosen, the player restarts
	# his or her turn.
	print """
Which item do you want to use?  If you've changed your mind, write 'nothing'.
	"""
	target = raw_input("> ")
					
	while not(target in special_items or target == 'nothing'):
		print "That isn't an option. Try again."
		target = raw_input("> ")
						
	if target == 'nothing':
		print "Very well."
		
	# Here is where the use of special items is detailed.
	else:
		print """
You attempt to use {0}. It requires {1} targets. The legal targets are:
		""".format(target, d2[target].num_targets)
		for thing in targets:
			print thing
		print Lib.player.name
		m = 1
		use_on = []
		while m <= d2[target].num_targets:
			print "Target {0} is:".format(m)
			tar = raw_input("> ")
			while not(tar in targets or tar == Lib.player.name):
				print "That isn't a legal target.  Try again."
				tar = raw_input("> ")
			use_on.append(tar)
			m = m + 1
		for thing in use_on:
			d2[target].special(d1[thing])
		n = n + 1
	return n
	
# The next four functions are used whenever a piece of armor or a weapon
# is equipped or unequipped.
def add_armor(thing):
	Lib.player.ac = Lib.player.ac + thing.bonus
	print "Your Armor Class is now: {0}.".format(Lib.player.ac)
	if isinstance(thing, Lib.Shield):
		Lib.player.held[1] = thing
	else:
		Lib.player.armor[thing.slot] = thing
	
def lose_armor(thing):
	Lib.player.ac = Lib.player.ac - thing.bonus
	print "Your Armor Class is now: {0}.".format(Lib.player.ac)
	if isinstance(thing, Lib.Shield):
		Lib.player.held[1] = None
	else:
		Lib.player.armor[thing.slot] = None
	
def add_weapon(thing):
	Lib.player.die = Lib.player.die + thing.die
	print "Your Attack Die is now: {0}.".format(Lib.player.die)
	Lib.player.att = Lib.player.att + thing.bonus
	print "Your Attack Bonus is now: {0}.".format(Lib.player.att)
	Lib.player.damage = Lib.player.damage + thing.bonus
	print "Your Damage Bonus is now: {0}.".format(Lib.player.damage)
	Lib.player.held[0] = thing
	
def lose_weapon(thing):
	Lib.player.die = Lib.player.die - thing.die
	print "Your Attack Die is now: {0}.".format(Lib.player.die)
	Lib.player.att = Lib.player.att - thing.bonus
	print "Your Attack Bonus is now: {0}.".format(Lib.player.att)
	Lib.player.damage = Lib.player.damage - thing.bonus
	print "Your Damage Bonus is now: {0}.".format(Lib.player.damage)
	Lib.player.held[0] = None
	
# The next three functions manage the three major out of combat actions.
def drop(thing, loot):
	print "You are attempting to drop {0}.".format(thing.name)
	if thing in Lib.player.bag:
		Lib.player.bag.remove(thing)
		
	elif isinstance(thing, Lib.Armor):
		lose_armor(thing)
			
	elif isinstance(thing, Lib.Weapon):
		lose_weapon(thing)
		
	elif isinstance(thing, Lib.Wand):
		Lib.player.held[1] = None
		
	else:
		Lib.player.belt.remove(thing)
		
	loot.append(thing)
	print "You have dropped {0}.".format(thing.name)
	
def store(thing, loot):
	print "You are attempting to store {0}.".format(thing.name)

	if len(Lib.player.bag) >= 5:
		print "Your bag is already full."
		drop(thing)
		
	elif thing in loot:
		loot.remove(thing)
		
	elif isinstance(thing, Lib.Armor):
		lose_armor(thing)
			
	elif isinstance(thing, Lib.Weapon):
		lose_weapon(thing)
		
	elif isinstance(thing, Lib.Wand):
		Lib.player.held[1] = None
		
	else:
		Lib.player.belt.remove(thing)
		
			
	Lib.player.bag.append(thing)
	print "You have stored {0}.".format(thing.name)
	
def equip(thing, loot):
	if thing in loot:
		loot.remove(thing)
	else:
		Lib.player.bag.remove(thing)
			
	if isinstance(thing, Lib.Weapon):
		print "You are attempting to equip {0}.".format(thing.name)
		if Lib.player.held[0] != None:
			store(Lib.player.held[0], loot)
		add_weapon(thing)
		print "You have equipped {0}.".format(thing.name)
			
	elif isinstance(thing, Lib.Armor):
		print "You are attempting to put on {0}.".format(thing.name)
		if isinstance(thing, Lib.Shield):
			if Lib.player.held[1] != None:
				store(Lib.player.held[1], loot)
		elif Lib.player.armor[thing.slot] != None:
			store(Lib.player.armor[thing.slot], loot)
		add_armor(thing)
		print "You have put on {0}.".format(thing.name)
			
	elif isinstance(thing, Lib.Wand):
		print "You are attempting to equip {0}.".format(thing.name)
		if Lib.player.held[1] != None:
			store(Lib.player.held[1], loot)
		Lib.player.held[1] = thing
		print "You have equipped {0}.".format(thing.name)
		
	else:
		print """
You are attempting to tuck {0} into your potion belt.
		""".format(thing.name)
		
		if len(Lib.player.belt) >= 5:
			print "Your potion belt is already full."
			store(thing, loot)
		else:	
			Lib.player.belt.append(thing)
			print "{0} is tucked into your belt.".format(thing.name)
	
# The next three functions are where the player makes decisions about inventory
# manipulation.
def store_fun(loot, loot_names, held_names, armor_names, belt_names, d):
	print "What do you want to store?  If you don't want to store something, type"
	print "'nothing'."
	target = raw_input("> ")
			
	# The store function in Lib.player.py only works if target is in certain places.
	# This loop forces the player to chose an object in one of those places.	
	while not(
		target in loot_names or target in held_names
		or target in armor_names or target in belt_names
		or target == 'nothing'
	):
		print "You can't store that."
		target = raw_input("> ")
	if target == 'nothing':
		print "Very well."
			
	else:
		store(d[target], loot)
		
# This function represents what happens when the player attempts to equip an item.
def equip_fun(loot, loot_names, bag_names, d):
	print "What do you want to equip?  If you don't want to equip something, type"
	print "'nothing'."
	target = raw_input("> ")
			
	# The equip function in Lib.player.py only works if target is in certain places.
	# This loop forces the player to chose an object in one of those places.
	while not(target in loot_names or target in bag_names or target == 'nothing'):
		print "You can't equip that."
		target = raw_input("> ")
	if target == 'nothing':
		print "Very well."
				
	# I may want to change this to something more elegant.  If the player decides to
	# equip 'nothing', then isinsthance(d['nothing'], ...) will return an error.  I need
	# to prevent that.  I also need to sort out whether the equipped item is a weapon
	# or an armor, and that will decide which function from Lib.player I will need.
	else:
		equip(d[target], loot)
		
				
# This function represents what happens when the player attempts to drop an item.
def drop_fun(loot, bag_names, held_names, armor_names, belt_names, d):
	print "What do you want to drop?  If you don't want to drop something, type"
	print "'nothing'."
	target = raw_input("> ")
				
	# The drop function in Lib.player.py only works if target is in certain places.
	# This loop forces the player to chose an object in one of those places.
	while not(
		target in armor_names or target in held_names
		or target in bag_names or target in belt_names
		or target == 'nothing'
	):
		print "You can't drop that."
		target = raw_input("> ")
	if target == 'nothing':
		print "Very well."
		
	else:
		drop(d[target], loot)
		
def manage_inventory(
	loot, loot_names, bag_names, held_names, armor_names, belt_names, d
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
		
	elif action == 'store':
		store_fun(loot, loot_names, held_names, armor_names, belt_names, d)
				
	elif action == 'equip':
		equip_fun(loot, loot_names, bag_names, d)
		
	elif action == 'drop':
		drop_fun(loot, bag_names, held_names, armor_names, belt_names, d)
			
	return action
	
def check_inventory():
	armor_slots = {0: 'chest', 1: 'head', 2: 'hands', 3: 'feet', 4: 'back'}
	print "Your armor:"
	n = 0
	while n < 5:
		if Lib.player.armor[n] != None:
			print "You are wearing {0} on your {1}.".format(
				Lib.player.armor[n].name, armor_slots[n]
			)
		else:
			print "You are wearing {0} on your {1}.".format(
				'nothing', armor_slots[n]
			)
		n = n + 1
			
	print "\nYour held items:"
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
	
	print "\nThe following potions are in your belt:"
	for thing in Lib.player.belt:
		print thing.name
	
	print "\nThe following items are in your bag:"
	for thing in Lib.player.bag:
		print thing.name
				
	print """
\nYour stats are the following:
\tHit Points: {0}
\tArmor Class: {1}
\tAttack Bonus: {2}
\tDamage Bonus: {3}
\tAttack Die: {4}
	""".format(
		Lib.player.hit_points, Lib.player.ac, Lib.player.att, Lib.player.damage,
		Lib.player.die
	)


# I made lists containing the names of all of the legal targets for various actions
# and a dict that matches them with their objects.  This is the best way I found
# to manage interactions with inputs.
def reset_names(loot):
	loot_names = []
	for thing in loot:
		loot_names.append(thing.name)
	list = [loot_names]
	for thing in Lib.player.stuff_names():
		list.append(thing)
	global d
	d = {}
	
	for thing in loot:
		d[thing.name] = thing
	for thing in Lib.player.bag:
		d[thing.name] = thing
	for thing in Lib.player.belt:
		d[thing.name] = thing
	for thing in Lib.player.held:
		if thing != None:
			d[thing.name] = thing
	for thing in Lib.player.armor:
		if thing != None:
			d[thing.name] = thing
			
	list.append(d)
	return list
	
# This function runs as soon as the encounter for a room is completed.  It manages all
# of the non-encounter actions that the player can choose.
def loot_the_room(loot, adjacent):
	targetable = reset_names(loot)
			
	while True:
		print "Do you want to 'search', 'check inventory', 'manage inventory',"
		print "'use potion', or 'leave'?"
		action = raw_input("> ")
		if action == 'search':
			print "\nYou find:"
			for thing in loot:
				print thing.name
				
		elif action == 'check inventory':
			check_inventory()
		
		elif action == 'manage inventory':
			while action != 'done':
				action = manage_inventory(
					loot, targetable[0], targetable[1], targetable[2], targetable[3],
					targetable[4], targetable[5]
				)
				targetable = reset_names(loot)
				
		elif action == 'use potion':
			print "Which potion do you want to use?  If you don't want to use one,"
			print "write 'nothing'."
			print "The available potions are:"
			for thing in Lib.player.belt:
				print thing.name
			potion = raw_input("> ")
			while not(potion in targetable[4] or potion == 'nothing'):
				print "That isn't an available potion."
				potion = raw_input("> ")
				
			if potion == 'nothing':
				print "Very well."
			else:
				targetable[5][potion].action()
				Lib.player.belt.remove(targetable[5][potion])
				
		elif action == 'leave':
			if adjacent == []:
				print "There are no other rooms yet.  Try something else."
			else:
				print "The possible rooms to enter are:"
				dest_names = []
				d3 = {}
				for thing in adjacent:
					print thing.name
					dest_names.append(thing.name)
					d3[thing.name] = thing
				print """
Were do you want to go?  If you don't want to leave yet, type 'nothing'.
				"""
				dest = raw_input("> ")
				while not(dest in dest_names or dest == 'nothing'):
					print "That isn't an option.  Try again."
					dest = raw_input("> ")
				if dest == 'nothing':
					print "Very well."
				else:
					print "You go to {0}.".format(dest)
					return d3[dest]
		else:
			print "That isn't an option.  Try again."

# This is my basic room outline.  It has an encounter and then a chance to loot.
class Room(object):
	
	def __init__(self, name, loot, creatures, adjacent):
		self.name = name
		self.loot = loot
		self.creatures = creatures
		self.adjacent = adjacent
	
	def encounter(self, creatures):
		creatures.append(Lib.player)
		order = initiative(creatures)
		
		# This code makes lists of legal targets and a dict to match
		targets = []
		d1 = {}
		for thing in order:
			targets.append(thing.name)
			d1[thing.name] = thing
		targets.remove(Lib.player.name)
			
		# This code runs through a combat.  Monsters attack the player on their turns.
		# The player may attack a target or use an item.
		n = 0
		while order != [Lib.player]:
			if order[n].hit_points <= 0:
				dead_thing = order[n].name
				print "{0} is dead.".format(dead_thing)
				targets.remove(order[n].name)
				order.remove(order[n])
			elif order[n] == Lib.player:
				print "{0} has the initiative.".format(Lib.player.name)
				targetable = reset_names(self.loot)
				d2 = targetable[5]
				belt_names = targetable[4]
				armor_names = targetable[3]
				held_names = targetable[2]
				# The combat function in Creature needs to return a list.
				# The first entry in the list needs to be either 'attack' or
				# special.  The second entry needs to be a choice that is associated
				# with that type of action.
				print """
What do you want to do?  You can 'attack', 'use special item', or 'use potion'.
				"""
				action = raw_input("> ")
		
				while not(
					action == 'attack'
					or action == 'use special item'
					or action == 'use potion'
				):
					print "You can't do that."
					action = raw_input("> ")
			
				if action == 'use special item':
					n = special_fun(n, targets, d1, held_names, armor_names, d2)
				
				elif action == 'use potion':
					print """
Which potion do you want to use?  If you don't want to use one, write 'nothing'.
					"""
					print "The available potions are:"
					for thing in Lib.player.belt:
						print thing.name
					potion = raw_input("> ")
					while not(potion in targetable[4] or potion == 'nothing'):
						print "That isn't an available potion."
						potion = raw_input("> ")
				
					if potion == 'nothing':
						print "Very well."
					else:
						targetable[5][potion].action()
						Lib.player.belt.remove(targetable[5][potion])
						n = n + 1
	
				elif action == 'attack':
					print "Who will you attack?  The legal targets are:"
					for thing in targets:
						print thing
					print "If you don't want to attack anything, write 'nothing'."
					target = raw_input("> ")
				
					while not(target in targets or target == 'nothing'):
						print "That isn't a legal target."
						target = raw_input("> ")
					if target == 'nothing':
						print "Very well."
					else:
						Lib.player.attack(d1[target])
						n = n + 1
			else:
				print "{0} has the initiative.".format(order[n].name)
				order[n].attack(Lib.player)
				n = n + 1
				
			if Lib.player.hit_points <= 0:
				print "You are dead."
				exit(1)
			if n >= len(order):
				n = 0
				
# This is the opening scene.  It will include the plot hook for the game and there
# will be enough loot that the player will have to start making decisions about what
# to equip.
class Woods(Room):

	def enter(self):
		print """
I will add better flavor text when I feel more creative.
		"""
		
		self.encounter(self.creatures)
		
		print """
The encounter is done. You find some stuff and may re equip before you move on
to the fortress.
		"""
		
		next_room = loot_the_room(self.loot, self.adjacent)
		return next_room
		
# This is the Great Hall.  It is the first room in the fortress.
class GreatHall(Room):
	
	def enter(self):
		print """
You are now in the great hall.  There are two goblins guarding the main entrance
and two doors on the far side of the room.  The guards attack you from the
left and right.
		"""
		
		self.encounter(self.creatures)
		
		print """
The guards have both fallen.  You don't think you hear any approaching soldiers,
but there are most likely more surprises farther in.  For now, you have a chance
to catch your breath and prepare.
		"""
		# The function action will only return anything if the option 'leave'
		# is chosen.  In this case, next_room will represent the next room.
		next_room = loot_the_room(self.loot, self.adjacent)
		return next_room

great_hall = GreatHall(
	'The Great Hall', [Lib.ssword, Lib.mail], [Lib.gob3, Lib.gob4], []
)		
woods = Woods(
	'The Woods', [Lib.dagger, Lib.leather, Lib.mmwand, Lib.buckler, Lib.hpot2],
	[Lib.gob1, Lib.gob2], [great_hall]
)