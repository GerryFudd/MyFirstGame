from random import randint
from sys import exit
import Lib

# This function figures out the order in which the creatures in the room act.
# make a list 'rolls' to collect the rolls
# make a dict 'match' to track who got what initiative roll
# for each creature in the list, determine the value of roll by d20 + init
# if roll matches any previous roll, compare the initiative modifiers of the
# 	previous creature and the current creature.  If they are equal, then move
#	the value of roll up or down slightly.  If one is greater, adjust the new value
#	of roll to make the better initiative value go first.
#	Repeat this process until roll matches no other rolls.
# Add roll to rolls and add roll: creature to match.
def initiative(creature_list):
	rolls = []
	match = {}
	for creature in creature_list:
		roll = randint(1, 20) + creature.initiative
		while roll in rolls:
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
	# set n to be the largest of the indices that will call something from rolls
	# make an empty list called 'initiative_order'
	n = len(rolls) - 1
	initiative_order = []
	while n >= 0:
		initiative_order.append(match[rolls[n]])
		n = n - 1
	return initiative_order
	
def store_fun(loot, loot_names, held_names, armor_names, d):
	print "What do you want to store?"
	target = raw_input("> ")
				
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
		
def equip_fun(loot, loot_names, bag_names, held_names, armor_names, d):
	print "What do you want to equip?"
	target = raw_input("> ")
			
	while not(target in loot_names or target in bag_names):
		print "You can't equip that."
		target = raw_input("> ")
	if target == 'nothing':
		print "Very well."
				
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
				
def drop_fun(loot, loot_names, bag_names, held_names, armor_names, d):
	print "What do you want to drop?"
	target = raw_input("> ")
				
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

def action(loot):
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
		elif action == 'manage inventory':
			while action != 'done':
				action = manage_inventory(
					loot, loot_names, bag_names, held_names, armor_names, d
				)
				
		elif action == 'leave':
			print "There are no other rooms yet.  Try something else."
		else:
			print "That isn't an option.  Try again."

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
		
		# This code makes lists of legal targets and makes a way of targeting objects
		targets = []
		d = {}
		for thing in order:
			targets.append(thing.name)
			d[thing.name] = thing
		targets.remove(Lib.player.name)
			
		# Set n to 0
		# Make sure that Steve is alive and that Steve is not the only creature left
		# Check if the active creature is dead.  If it is, remove it from targets
		# and the turn order.  This doesn't change n.
		# If the active creature is alive, run the act function for that creature
		# and store the returned action as choice.
		# verify that choice[0] is attack and verify that order[1] is a valid target.
		# Run the attack function for the active creature with order[1] as the target.
		#	This sets n to the next integer.
		# If order[1] isn't a legal target, leave n alone and start over.
		# If n is outside the length of order, start the turn order over.
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
		next_room = action(self.loot)

great_hall = GreatHall()