import random

class Status(Item):
    def __eq__(self, rhs):
        return self.name == rhs.name or self.name == rhs

    def bind(self, user):
        self.user = user

    def start(self):
        pass

    def end_turn(self):
        pass

    def remove(self):
        pass


class flinch(Status):
    def start(self):
        user = self.user
        user.active = False

    def end_turn(self):
        user = self.user
        user.active = True
 

class poison(Status):
    def end_turn(self):
        user = self.user
        user.hp -= user.max_hp / 8
 

class bad_poison(Status):
    def start(self):
        user = self.user
        self.poison_level = 1

    def end_turn(self):
        user = self.user
        user.hp -= user.max_hp * instance.posion_level * (1 / 16)
        self.posion_level += 1

 
class sleep(Status):
    def start(self):
        user = self.user
        user.active = False
 
    def end_turn(instance):
        user = self.user
        self.t_sleep -= 1
        if self.t_sleep == 0:
            self.user.remove_status('sleep')

    def remove(self):
        user = self.user
        user.active = True


class burn(Status):
    def start(self):
        user = self.user
        user.hp -= user.max_hp / 16 


class leech_seed(Status):
    def end_turn(self):
        user = self.user
        opp = user.opp
        user.hp -= user.max_hp / 8
        opp.hp += user.hp


class paralyse(Status):
    def start(self):
        user = self.user
        user.speed /= 2
        if random.random() < 0.25:
            user.active = False
        else:
        user.active = True
 
    def end_turn(self):
        user = self.user
        if random.random() < 0.25:
            user.active = False
        else:
            user.active = True

    def remove(self):
        user = self.user
        user.speed *= 2
        user.active = True


class freeze(Status):
    def start(self):
        user = self.user
        user.active = False    
 
    def end_turn(self):
        user = self.user
        if random.random() < 0.2:
            user.remove_status(self)
            user.active = True

