from random import randint

# This file contains the library of things that exist within the game.

# All of the things for the protagonist to interact with will be either a
# Creature, a Weapon, an Armor, or a SpecialItem.  The most complicated of
# these is the Creature.  I want the Creature class to contain all of the
# actions that a creature might take.  The creature subclasses will contain
# the creature attributes such as maximum hit points and the like.
class Creature(object):

	# The attack action is the most obvious.  This is how one creature attempts
	# to kill another creature.  This action requires that target is another creature.
	# All creatures must have the attributes:
	# att, ac, damage, name, and hit_points
	def attack(self, target):
		if self.die == None:
			print "That is impossible."
		else:
			result = randint(1, 20) + self.att
			
			if result >= target.ac:
				damage = randint(1, self.die) + self.damage
			
				if damage <= 1:
					damage = 1
					pt = 'point'
				else:
					pt = 'points'
				
				print "{0} hits {1}.  The attack deals {2} {3} of damage.".format(
					self.name, target.name, damage, pt)
				target.hit_points = target.hit_points - damage
				print "{0} has {1} hit points left".format(
					target.name, target.hit_points
				)
			else:
				print "{0} attacks {1} and misses.".format(self.name, target.name)
				print "{0} has {1} hit points left".format(
					target.name, target.hit_points
				)
				
	def act(self, targets):
		return 'Steve'
		
class Weapon(object):
	
	def __init__(self, name, die, bonus):
		self.name = name
		self.die = die
		self.bonus = bonus
		
class SpecialItem(object):

	def __init__(self, name, action, other):
		self.name = name
		self.action = action
		self.other = other
		
class Armor(object):
	
	# The slots are 0: chest, 1: head, 2: hands, 3: feet, 4: back
	def __init__(self, name, action, bonus, slot):
		self.name = name
		self.action = action
		self.bonus = bonus
		self.slot = slot
		
def magic_missile(legal_targets):
	n = 0
	damage = []
	targets = []
	while n < 2:
		damage.append(randint(1, 4) + 1)
		print "Who do you want to hit with missile {0}?".format(n + 1)
		print "The legal targets are:"
		for thing in legal_targets:
			print thing
		target = raw_input("> ")
		while not(target in legal_targets):
			print "Try again."
			target = raw_input("> ")
		targets.append(target)
		n = n + 1
	return ['damage', damage, targets]

club = Weapon('Club', 4, 0)
dagger = Weapon('Dagger', 4, 1)
ssword = Weapon('Shord Sword', 6, 1)
cloth = Armor('Cloth Armor', None, 1, 0)
leather = Armor('Leather Armor', None, 2, 0)
mail = Armor('Chain Mail', None, 4, 0)
mmwand = SpecialItem('Wand of Magic Missile', magic_missile, [None])
buckler = SpecialItem('Buckler', None, ['ac', 1])
	
class PlayerCharacter(Creature):
		
	armor = [cloth, None, None, None, None]
	held = [club, buckler]
	bag = []

	def __init__(self, name, maxhp, combat, athletic):
		self.name = name
		self.maxhp = maxhp
		self.hit_points = maxhp
		self.ac = 10 + athletic + self.armor[0].bonus
		self.att = 1 + combat + self.held[0].bonus
		self.damage = combat + self.held[0].bonus
		self.initiative = athletic
		self.die = self.held[0].die
		
		if self.held[1] != None:
			if self.held[1].other[0] == 'ac':
				self.ac = self.ac + self.held[1].other[1]
			elif self.held[1].other[0] == 'attack':
				self.att = self.att + self.held[1].other[1]
	
	# Creatures should be able to drop items and store items.  That is the reason for
	# the two functions drop and store.
	# The thing must be an instance of a weapon or armor.
	# The location must be either [self.held, #], [self.armor, #], or a list
	# The room must be a list.
	def drop(self, thing, location, room):
		print "You are attempting to drop {0}.".format(thing.name)
		if location[0] == self.armor:
			self.ac = self.ac - thing.bonus
			print "Your Armor Class is now: {0}.".format(self.ac)
			location[0][location[1]] = None
		elif location[0] == self.held and location[1] == 0:
			self.die = self.die - thing.die
			print "Your Attack Die is now: {0}.".format(self.die)
			self.att = self.att - thing.bonus
			print "Your Attack Bonus is now: {0}.".format(self.att)
			self.damage = self.damage - thing.bonus
			print "Your Damage Bonus is now: {0}.".format(self.damage)
			location[0][0] = None
		elif location[0] == self.held and location[1] == 1:
			if thing.other[0] == 'ac':
				self.ac = self.ac - thing.other[1]
				print "Your Armor Class is now {0}.".format(self.ac)
			elif thing.other[0] == 'attack':
				self.att = self.att - thing.other[1]
				print "Your Aattack Bonus is now {0}.".format(self.att)
			location[0][1] = None
		else:
			location.remove(thing)
		room.append(thing)
		print "You have dropped {0}.".format(thing.name)
		
	# The thing must be an instance of a weapon or armor.
	# The location must be either [self.held, #], [self.armor, #], or a list
	# The room must be a list.
	def store(self, thing, location, room):
		print "You are attempting to store {0}.".format(thing.name)
		if len(self.bag) >= 5:
			print "Your bag is already full."
			self.drop(thing, location, room)
		elif location[0] == self.armor:
			self.ac = self.ac - thing.bonus
			print "Your Armor Class is now: {0}.".format(self.ac)
			location[0][location[1]] = None
		elif location[0] == self.held and location[1] == 0:
			self.die = self.die - thing.die
			print "Your Attack Die is now: {0}.".format(self.die)
			self.att = self.att - thing.bonus
			print "Your Attack Bonus is now: {0}.".format(self.att)
			self.damage = self.damage - thing.bonus
			print "Your Damage Bonus is now: {0}.".format(self.damage)
			location[0][0] = None
		elif location[0] == self.held and location[1] == 1:
			if thing.other[0] == 'ac':
				self.ac = self.ac - thing.other[1]
				print "Your Armor Class is now {0}.".format(self.ac)
			elif thing.other[0] == 'attack':
				self.att = self.att - thing.other[1]
				print "Your Aattack Bonus is now {0}.".format(self.att)
			location[0][1] = None
		else:
			location.remove(thing)
		self.bag.append(thing)
		print "You have stored {0}.".format(thing.name)
		
	# This function will check what slot an item will take up.  Then it will check if
	# there is already an item there.  If an item is already in that slot, the
	# function will attempt to store whatever is already in the slot.  If there is not
	# enough storage space, then it will drop the item that is already in the
	# destination slot. The next step is to equip the item.  This means that any
	# attributes that should be changed by the item are changed, and the item should
	# be placed in the appropriate list.
	# thing should be an instance of Weapon or Armor
	# location should be a list
	# room should be a list
	def wear(self, thing, location, room):
		print "You are attempting to put on {0}.".format(thing.name)
		if self.armor[thing.slot] != None:
			self.store(self.armor[thing.slot], [self.armor, thing.slot], room)
		
		self.armor[thing.slot] = thing
		self.ac = self.ac + thing.bonus
		print "Your Armor Class is now: {0}.".format(self.ac)
		
		location.remove(thing)
		print "You have put on {0}.".format(thing.name)
		
	def hold(self, thing, location, room):
		print "You are attempting to equip {0}.".format(thing.name)
		if self.held[1] != None:
			self.store(self.held[1], [self.held, 1], room)
		
		self.held[1] = thing
		if thing.other[0] == 'ac':
			self.ac = self.ac + thing.other[1]
			print "Your Armor Class is now {0}.".format(self.ac)
		elif thing.other[0] == 'attack':
			self.att = self.att + thing.other[1]
			print "Your Aattack Bonus is now {0}.".format(self.att)
		
		location.remove(thing)
		print "You have equipped {0}.".format(thing.name)
		
	
	def equip(self, thing, location, room):
		print "You are attempting to equip {0}.".format(thing.name)
		if self.held[0] != None:
			self.store(self.held[0], [self.held, 0], room)
		
		self.held[0] = thing
		self.die = self.die + thing.die
		print "Your Attack Die is now: {0}.".format(self.die)
		self.att = self.att + thing.bonus
		print "Your Attack Bonus is now: {0}.".format(self.att)
		self.damage = self.damage + thing.bonus
		print "Your Damage Bonus is now: {0}.".format(self.damage)
		
		location.remove(thing)
		print "You have equipped {0}.".format(thing.name)
	
	def act(self, targets):
		while targets != []:
			print "Who will you attack?  The legal targets are:"
			for thing in targets:
				print thing
			target = raw_input("> ")
		
			while not(target in targets):
				print "That isn't a legal target."
				target = raw_input("> ")
		
			return target
	
player = PlayerCharacter('Steve', 14, 2, 1)
		
class Goblin(Creature):
	
	def __init__(self, name):
		self.name = name
		self.maxhp = 4
		self.hit_points = 4
		self.ac = 10
		self.att = 0
		self.damage = -1
		self.initiative = 2
		self.die = 3
	
class Wolf(Creature):

	def __init__(self, name):
		self.name = name
		self.maxhp = 6
		self.hit_points = 6
		self.ac = 15
		self.att = 3
		self.damage = 2
		self.initiative = 2
		self.die = 8