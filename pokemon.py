import json
from status import normal
from base import Item, STAT_NAMES, Factory, coef_stage
from move import Move
from status import *

CONFUSION_PROB = 0.33
MOVE_DB_PATH = 'moves.json'


def stat(stat_name):
    stat_name = stat_name.lower()
    
    def setter(instance, val):
        if stat_name == 'hp':
            max_hp = instance.max_hp
            if val > max_hp:
                val = max_hp
            elif val <= 0:
                val = 0
                # instance.game.winner = instance
        instance.__dict__[stat_name] = val

    def getter(instance):
        val = instance.__dict__[stat_name]
        if stat_name != 'hp':
            val *= coef_stage[getattr(instance.stages, stat_name)+6]
        return val

    return property(getter, setter)

# Mimum stat stage is -6 and maximum stat stage is +6
class Stages(Item):
    seperator = ' | '
    def __setattr__(self, name, val):
        if val > 6: val = 6
        if val < -6: val = -6
        self.__dict__[name] = val

class Pokemon(Item):
    move_fac = Factory(Move, MOVE_DB_PATH)
    for stat_name in STAT_NAMES:
        vars()[stat_name] = stat(stat_name)

    def __init__(self, user, player, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.player = player
        self.level = 100
        self.active = True
        self.confused = False
        self.status = []
        self.next_move = None
        self.stages = Stages(**{stat_name:0 for stat_name in STAT_NAMES})
        for stat_name in STAT_NAMES:
            basic_stat = getattr(self, stat_name)
            self.__dict__['basic_' + stat_name] = basic_stat
            self.__dict__[stat_name] = self.compute_stat(stat_name, basic_stat)
        self.max_hp = self.hp

    # To calculate the actual stats of the Pokemon in battle from the base stats
    # Stat calculation is from https://bulbapedia.bulbagarden.net/wiki/Statistic

    def add_status(self, status_name, *arg, **kwargs):
        append_condition = True
        # check conditions of adding the status
        if status_name == 'sleep'
            if 'burn' in self.status:
                #TODO
                #TODO

        if append_condition:
            status = globals()[stat_name](*arg, **kwargs)
            status.bind(self)
            status.start()
            self.status.append(status)

    def remove_status(self, status):
        for my_status in self.status:
            if my_status == status:
                my_status.remove()
                self.status.remove(stat_name)

    def clear_status(self):
        self.status.clear()

    def status_effect(self):
        for status in self.status:
            status.end_turn()

    def compute_stat(self, stat_name, val):
        if stat_name == 'hp':
            val = int((2*val + 31 + (252/4)) + self.level + 10)
        else:
            val = int((2*val + 31) + 5)
        return val

    def bind_opp(self, opp):
        self.opp = opp
        self._moves = [self.move_fac.make(name, user=self) for name in self.moves]

    def select_move(self):
        # ask user to selct move
        for no_move, move in enumerate(self._moves, 1):
            print(no_move)
            print(move)
            print()

        # Prompts the player to select their move, and if it is an invalid input, it will prompt the user to select again.
        while True:
            user_move_no = input(f'{self.player[1]}, please select your move (1, 2, 3 or 4) for your {self.name}: ')
            print('___________________________________________________________________________________________________')
            
            if (user_move_no == '1' or user_move_no == '2' or user_move_no == '3' or user_move_no == '4') and user_move_no != '':
                move = self._moves[int(user_move_no) - 1]

                if move.pp > 0:
                    move.pp -= 1
                    break
                    
                else:
                    print(f'You have no more PP for "{move.name}"!\nPlease choose another one.')
            
                if self.active is False:
                    move = move_fac.make('cant_move', self)

                if self.confused is True:
                    if random.random <= CONFUSION_PROB:
                        move = move_fac.make('self_attack', self, self)

            else:
                print(f'{user_move_no} is not a valid input, please input only 1, 2, 3 or 4.')

            # try:
            #     move = self._moves[int(user_move_no)-1]
            # except (ValueError, IndexError):
            #     print(user_move_no, 'is not a valid choice, please input 1, 2, 3 or 4.')

            # else:
            #     if move.pp > 0:
            #         move.pp -= 1
            #         break
            #     else:
            #         print(f'You have no more PP for "{move.name}"!\nPlease choose another one.')
            
            #     if self.active is False:
            #         move = move_fac.make('cant_move', self)

            #     if self.confused is True:
            #         if random.random <= CONFUSION_PROB:
            #             move = move_fac.make('self_attack', self, self)

        self.next_move = move
        return move

    def move(self):
        self.next_move()
