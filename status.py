import random

def make_status(cls_name):

    start = globals().get(cls_name+'_start', do_nothing)
    end_turn = globals().get(cls_name+'_end', do_nothing)
    end = globals().get(cls_name+'_del', do_nothing)

    def start(instance):
        instance.__class__.start(**instance.__dict__)

    def bind(instance, user):
        instance.user = user

    def __init__(instance, **kwargs):
        for name, val in kwargs.items():
            setattr(instance, name, val)

    cls_attrs = dict(
            __init__ = __init__,
            name = cls_name,
            bind = bind,
            start = start,
            end_turn = end_turn,
            )

    return type(cls_name, (object,), cls_attrs)

def do_nothing(user):
    pass

def flinch_start(user):
    user.active = False
 
def flinch_end(user):
    user.active = True


def poison_end(user):
    user.hp -= user.max_hp / 8

 
def bad_poison_start(user):
    user.poison_level = 1
 
def bad_poison_end(user):
    user.hp -= user.max_hp * user.posion_level * (1 / 16)
    user.posion_level += 1


def sleep_start(user, turns):
    user.t_sleep = turns
    user.active = False
 
def sleep_end(user):
    user.t_sleep -= 1
 
    if user.t_sleep == 0:
        user.status = normal()
        user.active = True
 
    del user.t_sleep


def burn_end(user):
    user.hp -= user.max_hp / 16 


def leech_seed_end(user):
    opp = user.opp
    user.hp -= user.max_hp / 8
    opp.hp += user.hp

 
def paralyse_start(user):
    user.speed /= 2
    if random.random() < 0.25:
        user.active = False
    else:
        user.active = True
 
def paralyse_end(user):
    if random.random() < 0.25:
        user.active = False
    else:
        user.active = True

def paralyse_del(user):
    user.speed *= 2
    user.active = True

 
def freeze_start(user):
    user.active = False    
 
def freeze_end(user):
    if random.random() < 0.2:
        user.status = normal()
        user.active = True



normal = make_status('normal')
flinch = make_status('flinch')
poison = make_status('poison')
bad_poison = make_status('bad_poison')
sleep = make_status('sleep')
burn = make_status('burn')
leech_seed = make_status('leech_seed')
paralyse = make_status('paralyse')
freeze = make_status('freeze')