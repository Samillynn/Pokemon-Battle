# All the data of the game. All these information and data are obtained from smogon.com and bulbapedia.bulbagarden.net
from pokemon import Pokemon
from base import Factory
import random

POKE_DB_PATH = 'pokemons.json'
poke_fac = Factory(Pokemon, POKE_DB_PATH)

# Functions of the game
def view_move(): # Prompts the player to choose a move so that he can view the details of the move.
	# Move details
	print()
	move_name_string = input("Please type in the name of the move (exactly as displayed, excluding the '') to view its details, type 'next' if you no longer wish to view the moves: ")
	print()

	while move_name_string.lower() != 'next':
		# Checks if an invalid input has been entered (invalid input means not the exact name of the move as displayed)
		while move_name_string not in moves_list and move_name_string != 'next':
			move_name_string = input("Invalid move! Please type in the name of the move (exactly as displayed, case and space sensitive, excluding the ''), or type in 'next' to return to the Pokemon list: ")
			print()

		# Displays the details of each move, vars() syntax is from https://www.daniweb.com/programming/software-development/threads/111526/setting-a-string-as-a-variable-name
		if move_name_string != 'next': # In case the user types 'next' previously
			move_name = vars()[move_name_string]
			print(f'''{move_name_string} - Type: {move_name['Type']} | Category: {move_name['Category']} | Power: {move_name['Power']} | Accuracy: {int(move_name['Accuracy'] * 100)}% | PP: {move_name['PP']}\nDescription: {move_name['Description']}''')
			print()
			move_name_string = input("Type 'next' if you no longer wish to view the moves and go back to the Pokemon list. Else, type in the name of the move to view its details: ")
			print()

# Displays the current status and HP of the Pokemon in battle
def display_hp_status():
	print(f'''{player_1_pokemon.player[1]}''')
	print('_________________________')
	print(f'''{player_1_pokemon.name}\nHP: {player_1_pokemon.hp}/{player_1_pokemon.max_hp}''') # Prints out the current HP of the Pokemon
	print(f'''Status: {player_1_pokemon.status.name}''')
	print('_________________________')
	print()
	print(f'''{player_2_pokemon.player[1]}''')
	print('_________________________')
	print(f'''{player_2_pokemon.name}\nHP: {player_2_pokemon.hp}/{player_2_pokemon.max_hp}''') # Prints out the current HP of the Pokemon
	print(f'''Status: {player_2_pokemon.status.name}''')
	print('_________________________')
	print()

# To check if any Pokemon has died/fained/HP is 0 
def check_0_hp(pokemon):
	if pokemon.hp <= 0:
		print()
		display_hp_status()
		print(f"{pokemon.player[1]}'s {pokemon.name} has fainted, {pokemon.opp.player[1]} wins!")
		print()
		return True
	   
# The actual game
# The Pokemon ASCII art right below is from https://www.asciiart.eu/video-games/pokemon
print('''
  _ __   ___ | | _____ _ __ ___   ___  _ __       ___      __      _____   _____          _____
 | '_ \ / _ \| |/ / _ \ '_ ` _ \ / _ \| '_ \     |   |    /  \       |       |     |     |
 | |_) | (_) |   <  __/ | | | | | (_) | | | |    |___|   /____\      |       |     |     |_____
 | .__/ \___/|_|\_\___|_| |_| |_|\___/|_| |_|    |   |  /      \     |       |     |     |
 |_|                                             |___| /        \    |       |     |____ |_____
	''')

print()

# Gets the names of both players
player_1_name = input("Player 1, please input your name: ")
print(f'Hello, {player_1_name}!')
player_2_name = input("Player 2, please input your name: ")
print(f'Hello, {player_2_name}!')

# To allow the players to view the details and information of each move and Pokemon
print()
print('Each player shall choose one Pokemon and battle it out! The battle ends when one Pokemon faints/has 0 HP.')
print('Before both of you choose your Pokemon, please have a look at the details and information of the Pokemon.')
print()

trigger = True # So that the while loop below (to display the Pokemon list) can keep running until the user inputs 'continue'.

while trigger:
	print('''Pokemons available:\n\n- Snorlax (The Sleeping Giant)\n- Lucario (The UFC Fighter)\n- Salamence (The European Dragon)\n- Tentacruel (The Box Jellyfish)\n- Rhyperior (The Boulder Rhino)\n- Tyranitar (The Tyrannosarus Rex)\n- Volcarona (The Fire Bug)\n- Gengar (The Original Ghost)\n- Charizard (The Fire Dragon)\n- Blastoise (The Cannon Tortoise)\n- Venusaur (The Poison Rafflesia)\n- Electivire (The Electric Fighter)\n- Gardevoir (The Beautiful Sorcerer)\n- Mamoswine (The Ice Mammoth)\n- Garchomp (The Land Shark)\n- Hydreigon (The Black Dragon)\n- Metagross (The Computer Monster)\n- Sylveon (The Weird Eeveelution)\n - Magikarp (The Strongest and Most Legendary Pokemon in all of Existence)''')
	print()
	user_input = input("Please type in the name of a Pokemon to look at its information. Type in 'continue' to move on with the game: ")
	print()

	# Prints out the dictionary containing the main details of each Pokemon
	if user_input.lower() in pokemon_list:
		print(poke_fac.make(user_input, player = (3))) # So that whatever Pokemon the player chooses here (just to view its information) will not be assigned to any of the players in the actual battle
		view_move()

	elif user_input.lower() == 'continue':
		trigger = False
		
	else:
		user_input = input("Invalid input! Input any key to continue: ")
		print()

print('Please note that the stats you have seen previously are base stats and only serve as a comparison between the various Pokemon. The actual stats in battle will be based on the base stats, but not the same!')
print()
print("Now, it's time to choose your Pokemon!")
# The following quote is from https://bulbapedia.bulbagarden.net/wiki/Karen/Quotes#:~:text=%22Strong%20Pok%C3%A9mon.,to%20win%20with%20their%20favorites.
print('"Strong Pokemon. Weak Pokemon. That is only the selfish perception of people. Truly skilled trainers should try to win with their favorites." - Karen, Pokemon Gold/Silver')
print()

trigger = True
# Prompts player 1 to choose a Pokemon to battle with
while trigger:
	player_1_pokemon_string = input(f'{player_1_name}, please select a Pokemon from the list by inputing the name of the Pokemon!: ')

	if player_1_pokemon_string.lower() in pokemon_list:
		player_1_pokemon = poke_fac.make(player_1_pokemon_string, player = (1, player_1_name)) #Creates a new object for player 1's Pokemon and assign it to Player 1
		print (f'{player_1_name}, you have chosen {player_1_pokemon.name}!')
		print()
		trigger = False

	else:
		print('Invalid input!')
		print() 

trigger = True
# Prompts player 2 to choose a Pokemon to battle with
while trigger:
	player_2_pokemon_string = input(f'{player_2_name}, please select a Pokemon from the list by inputing the name of the Pokemon!: ')

	if player_2_pokemon_string.lower() in pokemon_list:
		player_2_pokemon = poke_fac.make(player_2_pokemon_string, player = (2, player_2_name)) #Creates a new object for player 2's Pokemon and assign it to Player 2
		print (f'{player_2_name}, you have chosen {player_2_pokemon.name}!')
		print()
		trigger = False

	else:
		print('Invalid input!')
		print()

# Assigns the opponent Pokemon to each of the player
player_1_pokemon.bind_opp(player_2_pokemon)
player_2_pokemon.bind_opp(player_1_pokemon)

# The battle begins
print('Let the battle begin!')
print(f'{player_1_name} - {player_1_pokemon.name} VS. {player_2_name} - {player_2_pokemon.name}!')
print()

trigger = True # So that the game can run infinitely, until trigger = False, when one of the Pokemon's HP decreases to 0.

while trigger:
	display_hp_status()
	player_1_move = player_1_pokemon.select_move() # Prompts the player to select a move
	print()
	player_2_move = player_2_pokemon.select_move()
	print()

	# Speed comparison and move priority comparison to determine which Pokemon will move first
	if player_1_move.priority > player_2_move.priority:
		# The Pokemon make their moves
		print(f"{player_1_name}'s {player_1_pokemon.name} used {player_1_move.name}!")
		print()
		player_1_pokemon.move()
		print()
		display_hp_status()
		
		if check_0_hp(player_2_pokemon) == True:
			trigger = False
			break

		print(f"{player_2_name}'s {player_2_pokemon.name} used {player_2_move.name}!")
		print()
		player_2_pokemon.move()
		print()

		if check_0_hp(player_1_pokemon) == True:
			trigger = False
			break

		if player_2_pokemon.speed > player_1_pokemon.speed:
			# The Pokemon receive any status effects
			player_2_pokemon.status.end_turn()

			if check_0_hp(player_2_pokemon) == True:
				trigger = False
				break

			player_1_pokemon.status.end_turn()

			if check_0_hp(player_1_pokemon) == True:
				trigger = False
				break

		else:
			player_1_pokemon.status.end_turn()

			if check_0_hp(player_1_pokemon) == True:
				trigger = False
				break
			
			player_2_pokemon.status.end_turn()

			if check_0_hp(player_2_pokemon) == True:
				trigger = False
				break

	elif player_2_move.priority > player_1_move.priority:
		print(f"{player_2_name}'s {player_2_pokemon.name} used {player_2_move.name}!")
		print()
		player_2_pokemon.move()
		print()
		display_hp_status()

		if check_0_hp(player_1_pokemon) == True:
			trigger = False
			break
		
		print(f"{player_1_name}'s {player_1_pokemon.name} used {player_1_move.name}!")
		print()
		player_1_pokemon.move()
		print()

		if check_0_hp(player_2_pokemon) == True:
			trigger = False
			break

		if player_2_pokemon.speed > player_1_pokemon.speed:
			# The Pokemon receive any status effects
			player_2_pokemon.status.end_turn()

			if check_0_hp(player_2_pokemon) == True:
				trigger = False
				break

			player_1_pokemon.status.end_turn()

			if check_0_hp(player_1_pokemon) == True:
				trigger = False
				break

		else:
			player_1_pokemon.status.end_turn()

			if check_0_hp(player_1_pokemon) == True:
				trigger = False
				break

			player_2_pokemon.status.end_turn()

			if check_0_hp(player_2_pokemon) == True:
				trigger = False
				break

	elif player_1_move.priority == player_2_move.priority:
		if player_1_pokemon.speed > player_2_pokemon.speed:
			print(f"{player_1_name}'s {player_1_pokemon.name} used {player_1_move.name}!")
			print()
			player_1_pokemon.move()
			print()
			display_hp_status()

			if check_0_hp(player_2_pokemon) == True:
				trigger = False
				break
			
			print(f"{player_2_name}'s {player_2_pokemon.name} used {player_2_move.name}!")
			print()
			player_2_pokemon.move()
			print()

			if check_0_hp(player_1_pokemon) == True:
				trigger = False
				break
			
			player_1_pokemon.status.end_turn()

			if check_0_hp(player_1_pokemon) == True:
				trigger = False
				break
			
			player_2_pokemon.status.end_turn()

			if check_0_hp(player_2_pokemon) == True:
				trigger = False
				break

		elif player_2_pokemon.speed > player_1_pokemon.speed:
			print(f"{player_2_name}'s {player_2_pokemon.name} used {player_2_move.name}!")
			print()
			player_2_pokemon.move()
			print()
			display_hp_status()

			if check_0_hp(player_1_pokemon) == True:
				trigger = False
				break
			
			print(f"{player_1_name}'s {player_1_pokemon.name} used {player_1_move.name}!")
			print()
			player_1_pokemon.move()
			print()

			if check_0_hp(player_2_pokemon) == True:
				trigger = False
				break
			
			player_2_pokemon.status.end_turn()

			if check_0_hp(player_2_pokemon) == True:
				trigger = False
				break
			
			player_1_pokemon.status.end_turn()

			if check_0_hp(player_1_pokemon) == True:
				trigger = False
				break

		elif player_1_pokemon.speed == player_2_pokemon.speed:
			random_number = random.random() < 0.5

			if random_number < 0.5:
				print(f"{player_1_name}'s {player_1_pokemon.name} used {player_1_move.name}!")
				print()
				player_1_pokemon.move()
				print()
				display_hp_status()

				if check_0_hp(player_2_pokemon) == True:
					trigger = False
					break
				
				print(f"{player_2_name}'s {player_2_pokemon.name} used {player_2_move.name}!")
				print()
				player_2_pokemon.move()
				print()

				if check_0_hp(player_1_pokemon) == True:
					trigger = False
					break
				
				player_1_pokemon.status.end_turn()

				if check_0_hp(player_1_pokemon) == True:
					trigger = False
					break
				
				player_2_pokemon.status.end_turn()

				if check_0_hp(player_2_pokemon) == True:
					trigger = False
					break

			else:
				print(f"{player_2_name}'s {player_2_pokemon.name} used {player_2_move.name}!")
				print()
				player_2_pokemon.move()
				print()
				display_hp_status()

				if check_0_hp(player_1_pokemon) == True:
					trigger = False
					break
				
				print(f"{player_1_name}'s {player_1_pokemon.name} used {player_1_move.name}!")
				print()
				player_1_pokemon.move()
				print()

				if check_0_hp(player_2_pokemon) == True:
					trigger = False
					break
				
				player_2_pokemon.status.end_turn()

				if check_0_hp(player_2_pokemon) == True:
					trigger = False
					break
				
				player_1_pokemon.status.end_turn()

				if check_0_hp(player_1_pokemon) == True:
					trigger = False
					break

# End of game
print('Game over, thank you for playing this game!')
