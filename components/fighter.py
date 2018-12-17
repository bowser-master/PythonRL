import libtcodpy as lbtc

from game_messages import Message

'''
What does this class do?
-accepts stats of a fighter (hp, max_hp, defense, power)
-makes unit take damage
-makes unit heal
-attacks another target (only enemies for now)

Ok a little brainstorming, I think i want to create another class that can heal and take damage
cause I plan to make stuff breakable, not necessarily only fighters (actors actually right?)
actual classes will probably be higher lvl class (inherited class?) so dat we only add some extra stuff
for now my planned classes are
-Bandit     -Merchant    -Cook

What will they provide?
-Exclusive items?
-Exclusive skills/passives?

What WON'T they provide?
-Elemental bonusses for sure
-Stats bonusses?
'''

class Fighter:
    def __init__(self, hp, defense, power, xp=0):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.xp = xp
        
    def take_damage(self, amount):
        results = []
        
        self.hp -= amount
        
        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})
            
        return results
        
    def heal(self, amount):
        self.hp += amount
        
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        
    def attack(self, target):
        results = []
    
        damage = self.power - target.fighter.defense
        
        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hitpoints. '.format(
                self.owner.name.capitalize(), target.name, str(damage)), lbtc.white )})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage. '.format(
                self.owner.name.capitalize(), target.name ), lbtc.white)})
                
        return results