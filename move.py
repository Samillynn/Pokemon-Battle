import json
import random
from math import ceil
from base import Item, coef_type
from status import *

NORMAL_CRITICAL = 0.04167

class Move(Item):
	def __init__(self, name, user, opp=None, **kwargs):
		# self.name = name
		super().__init__(name=name, **kwargs)
		self.user = user
		if opp is None:
			opp = user.opp
		self.opp = opp
		self.critical = NORMAL_CRITICAL
		self.effect = globals().get('_' + self.name.lower(), _normal_attack)

	def __repr__(self):
		return ' | '.join(f'{prop_name.title()}: {getattr(self, prop_name)}' for prop_name in self._prop_list if prop_name.lower() != 'description') + '\n' + self.description

	def __call__(self):
		# if hasattr(user, 'attack_buf'):
		#     attack_buf(move)
		# if hasattr(opp, 'receive_buf'):
		#     receive_buf(move)
		self.effect(self)

	# Physical moves use the Attack stat of the user and Defense stat of the target for damage calculation.
	# Special moves use the Sp_Atk stat of the user and Sp_Def stat of the target for damage calculation.
	def attack(self):
		user, opp = self.user, self.opp
		if self.category == 'Physical':
			A = user.attack
			D = opp.defense
		elif self.category == 'Special':
			A = user.sp_atk
			D = opp.sp_def
		
		# Finds the resultant type effectiveness if the target is a dual-type Pokemon. If its a single type Pokemon it will work as well
		coef_type_dual = 1
		for type_name in opp.type:
			coef_type_dual *= coef_type[self.type][type_name]

		# A super-effective move based on the move's type and the target's type
		if coef_type_dual > 1:
			print('The move is super effective!')
			print()

		# A not very effective move based on the move's type and the target's type
		elif coef_type_dual < 1 and coef_type_dual > 0:
			print('The move is not very effective...')
			print()

		# If the target Pokemon is immune to a move of a particular type, due to the target Pokemon's type
		elif coef_type_dual == 0:
			print(f"It didn't even affect {opp.player[1]}'s {opp.name} at all...")

		# For damage calculation
		modifier = random.uniform(0.85, 1)*coef_type_dual
		# If it is a critical hit
		critical_check = False
		if random.random() < self.critical:
			critical_check = True
			modifier *= 1.5
		# If the type of the move is the same as that of the user
		if self.type in user.type:
			modifier *= 1.5
		# If the user is burned
		if user.status.name.startswith('burn'):
			modifier *= 0.5
		# Damage calculation
		damage = ceil(((2*user.level/5 + 2)*self.power*A/D/50 + 2)*modifier)
		if random.random() > self.accuracy:
			print('The attack missed!')
			damage = 0
		else:
			opp.hp -= damage

		if damage > 0 and critical_check == True:
			print ("It's a critical hit!")

		return damage

# For moves that only deal damage without any effects/secondary effects
def _normal_attack(move):
	damage = move.attack()

def _self_attack(move):
	move.type = move.user.type
	move.opp = move.user
	damage = move.attack()

def _cant_move(move):
	user = move.user
	print(f"{user.player[1]}'s {user.name} cant\'t move because it is {user.status}")

def _curse(move):
	user = move.user
	user.stages.attack += 1
	user.stages.defense += 1
	user.stages.speed -= 1
	print(f"{user.player[1]}'s {user.name}'s Attack and Defense rose!")
	print(f"{user.player[1]}'s {user.name}'s Speed fell!")
	
def _body_slam(move):
	opp = move.opp
	damage = move.attack() # Deals the damage, causes the target's HP to decrease
	
	if damage > 0: # Secondary effects only come in to play if the attack lands and deals damage on the opposing Pokemon
		if random.random() < 0.3:
			opp.status = paralyse()
			print (f"{opp.player[1]}'s {opp.name} is paralysed!")
 
def _rest(move):
	user = move.user
	user.hp = user.max_hp
	user.status = sleep(turns=2)
	print(f"{user.player[1]}'s {user.name} went to sleep and became healthy!")
 
def _swords_dance(move):
	user = move.user
	user.stages.attack += 2
	print(f"{user.player[1]}'s {user.name}'s Attack rose sharply!")
 
def _meteor_mash(move):
	user = move.user
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.2:
			user.stages.attack +=1
			print(f"{user.player[1]}'s {user.name}'s Attack rose!")
 
def _close_combat(move):
	user = move.user
	damage = move.attack()

	if damage > 0:
		user.stages.attack -= 1
		user.stages.sp_def -= 1
		print(f"{user.player[1]}'s {user.name}'s Defense and Sp_Def fell!")
 
def _dragon_dance(move):
	user = move.user
	user.stages.attack += 1
	user.stages.speed += 1
	print(f"{user.player[1]}'s {user.name}'s Attack and Speed rose!")
 
def _double_edge(move):
	opp = move.opp
	user = move.user
	damage = move.attack()

	if damage > 0:
		user.hp -= int(0.33 * damage)
		print(f"{user.player[1]}'s {user.name} received {int(0.33 * damage)} HP recoil damage!")
		print()
		print(f'''{user.player[1]}\n{user.name}\nHP: {user.hp}/{user.max_hp}''')
 
def _scald(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.3:
			opp.status = burn()
			print(f"{opp.player[1]}'s {opp.name} is burned!")
 
def _sludge_bomb(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.3:
			opp.status = poison()
			print(f"{opp.player[1]}'s {opp.name} is poisoned!")
 
def _stone_edge(move):
	opp = move.opp
	move.critical = 0.125
	damage = move.attack()
 
def _ice_punch(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.1:
			opp.status = freeze()
			print(f"{opp.player[1]}'s {opp.name} is frozen!")
 
def _rock_slide(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.3:
			opp.status = flinch()
			print(f"{opp.player[1]}'s {opp.name} flinched!")
 
def _crunch(move):
	opp = move.opp
	damage = move.attack()
 
	if damage > 0:
		if random.random() < 0.2:
			opp.stages.defense -= 1
			print(f"{opp.player[1]}'s {opp.name}'s Defense fell!")
 
def _fire_punch(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.1:
			opp.status = burn()
			print(f"{opp.player[1]}'s {opp.name} is burned!")
 
def _quiver_dance(move):
	user = move.user
	user.stages.sp_atk += 1
	user.stages.sp_def += 1
	user.stages.speed += 1
	print(f"{user.player[1]}'s {user.name}'s Sp_Atk, Sp_Def and Speed rose!")
 
def _flamethrower(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.1:
			opp.status = burn() 
			print(f"{opp.player[1]}'s {opp.name} is burned!")
 
def _bug_buzz(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.1:
			opp.stages.sp_def -= 1
			print(f"{opp.player[1]}'s {opp.name}'s Sp_Def fell!")
 
def _roost(move):
	user = move.user
	user.hp += user.max_hp / 2
	print(f"{user.player[1]}'s {user.name} has recovered some HP!")
	
def _shadow_ball(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.2:
			opp.stages.sp_def -= 1  
			print(f"{opp.player[1]}'s {opp.name}'s Sp_Def fell!")
 
def _sludge_wave(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.1:
			opp.status = poison()
			print(f"{opp.player[1]}'s {opp.name} is poisoned!")
 
def _focus_blast(move):
	opp = move.opp
	damage = move.attack()
 
	if damage > 0:
		if random.random() < 0.1:
			opp.stages.sp_def -= 1  
			print(f"{opp.player[1]}'s {opp.name}'s Sp_Def fell!")
 
def _thunderbolt(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.1:
			opp.status = paralyse()
			print(f"{opp.player[1]}'s {opp.name} is paralysed!")
 
def _fire_blast(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.1:
			opp.status = burn()
			print(f"{opp.player[1]}'s {opp.name} is burned!")
 
def _air_slash(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.3:
			opp.status = flinch()
			print(f"{opp.player[1]}'s {opp.name} flinched!")
 
def _fake_out(move):
	opp = move.opp
	damage = move.attack()

	if damage > 0:
		opp.status = flinch()
		print(f"{opp.player[1]}'s {opp.name} flinched!")
 
def _ice_beam(move):
	opp = move.opp
	damage = move.attack()
 
	if damage > 0:
		if random.random() < 0.1:
			opp.status = freeze()
			print(f"{opp.player[1]}'s {opp.name} is frozen!")
 
def _leech_seed(move):
	opp = move.opp
	opp.status = leech_seed()
	print(f"{opp.player[1]}'s {opp.name} is seeded!")
 
def _leaf_storm(move):
	user = move.user
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.2:
			user.stages.sp_atk -=2
			print(f"{user.player[1]}'s {user.name}'s Sp_Atk fell sharply!")
 
def _psychic(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.1:
			opp.stages.sp_def -= 1  
			print(f"{opp.player[1]}'s {opp.name}'s Sp_Def fell!")
 
def _moonblast(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.3:
			opp.stages.sp_atk -= 1  
			print(f"{opp.player[1]}'s {opp.name}'s Sp_Atk fell!")
 
def _icicle_crash(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.3:
			opp.status = flinch()
			print(f"{opp.player[1]}'s {opp.name} flinched!")
 
def _will_o_wisp(move):
	opp = move.opp
	opp.status = burn()
	print(f"{opp.player[1]}'s {opp.name} is burned!")
 
def _draco_meteor(move):
	user = move.user
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.2:
			user.stages.sp_atk -=2
			print(f"{user.player[1]}'s {user.name}'s Sp_Atk fell sharply!")
 
def _dark_pulse(move):
	user = move.user
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.2:
			opp.status = flinch()
			print(f"{opp.player[1]}'s {opp.name} flinched!")
 
def _charge_beam(move):
	user = move.user
	mve.attack()
	
	if damage > 0:
		if random.random() < 0.7:
			user.stages.sp_atk +=1
			print(f"{user.player[1]}'s {user.name}'s Sp_Atk rose!")
 
def _thunder_punch(move):
	opp = move.opp
	damage = move.attack()
	
	if damage > 0:
		if random.random() < 0.1:
			opp.status = paralyse()
			print(f"{opp.player[1]}'s {opp.name} is paralysed!")
 
def _mystical_fire(move):
	opp = move.opp
	damage = move.attack()

	if damage > 0:
		opp.stages.sp_atk -= 1
		print(f"{opp.player[1]}'s {opp.name}'s Sp_Atk fell!")
 
def _toxic(move):
	opp = move.opp
	opp.status = bad_poison()
	print(f"{opp.player[1]}'s {opp.name} is badly poisoned!")