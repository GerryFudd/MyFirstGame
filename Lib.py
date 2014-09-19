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
		
class Weapon(object):
	
	def __init__(self, name, die, bonus):
		self.name = name
		self.die = die
		self.bonus = bonus
		
class SpecialItem(object):
		
	def special(self, target):
		self.spell_name(target)
		
def magic_missile(target):
	damage = randint(1, 4) + 1
	target.hit_points = target.hit_points - damage
	print """
A short bolt of pure force springs forth from your arm.  It strikes {0} in the chest
and deals {1} points of damage.

{0} has {2} hit points left.
	""".format(target.name, damage, target.hit_points)  
	
def bolster(target):
	hp = randint(1, 8) + 2
	target.hit_points += hp
	print "{0} has {1} hit points.".format(target.name, target.hit_points)
	target.att += 1
	target.damage += 1
	target.buff += 1
	print "{0} has been bolstered.".format(target.name)
	
def heal(target):
	healing = randint(1, 8) + 1
	if target.maxhp < target.hit_points + healing:
		print "{0} gains {1} hit points.".format(
			target.name, target.maxhp - target.hit_points
		)
		target.hit_points = target.maxhp
	else:
		print "{0} gains {1} hit points.".format(target.name, healing)
		target.hit_points = target.hit_points + healing
	
class Wand(SpecialItem):

	def __init__(self, name, spell_name, num_targets):
		self.name = name
		self.spell_name = spell_name
		self.num_targets = num_targets
		
class Potion(SpecialItem):

	def __init__(self, name, spell_name):
		self.name = name
		self.spell_name = spell_name
		
	def action(self):
		self.spell_name(player)
		
class Armor(object):
	
	# The slots are 0: chest, 1: head, 2: hands, 3: feet, 4: back
	def __init__(self, name, action, bonus, slot):
		self.name = name
		self.action = action
		self.bonus = bonus
		self.slot = slot

class Shield(Armor):
	
	def __init__(self, name, bonus):
		self.name = name
		self.bonus = bonus

club = Weapon('Club', 4, 0)
dagger = Weapon('Dagger', 4, 1)
ssword = Weapon('Shord Sword', 6, 1)
cloth = Armor('Cloth Armor', None, 1, 0)
leather = Armor('Leather Armor', None, 2, 0)
mail = Armor('Chain Mail', None, 4, 0)
mmwand = Wand('Wand of Magic Missile', magic_missile, 2)
buckler = Shield('Buckler', 1)
hpot1 = Potion('Healing Potion', heal)
	
class PlayerCharacter(Creature):
		
	armor = [cloth, None, None, None, None]
	held = [club, mmwand]
	belt = [hpot1]
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
		self.buff = 0
		
		if self.held[1] != None:
			if isinstance(self.held[1], Shield):
				self.ac = self.ac + self.held[1].bonus
	
	def stuff_names(self):
		armor_names = []
		for thing in self.armor:
			if thing != None:
				armor_names.append(thing.name)
		held_names = []
		for thing in self.held:
			if thing != None:
				held_names.append(thing.name)
		belt_names = []
		for thing in self.belt:
			belt_names.append(thing.name)
		bag_names = []
		for thing in self.bag:
			bag_names.append(thing.name)
			
		return [bag_names, held_names, armor_names, belt_names]
	
# The game defaults to making a player named Steve with 14 hit points, combat = 2, and
# athletic = 1
player = PlayerCharacter('Steve', 14, 50, 1)
		
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
		self.buff = 0