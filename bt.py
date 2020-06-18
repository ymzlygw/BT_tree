import random

class Node(object):
    def __init__(self, name): 
        super(Node, self).__init__() #object 对象初始化没有name
        self.name = name  
        self.status = None

    def run(self):
        return True

class Person(Node):
    def __init__(self, name, hp): 
        super(Person, self).__init__(name) 
        self.hp = hp

    def under_attack(self, power):
        self.hp -= power

class Skill(Node):
    def __init__(self, name, power, probability): 
        super(Skill, self).__init__(name)
        self.power = power
        self.probability = probability

    def setEnemy(self, person):
        self.person = person

    def run(self):
        if self.person == None:
            print("{} need select enemy first".format(self.name))
            return False

        random_p = random.random()
        if random_p < self.probability:
            print(self.name, "fire")
            self.person.under_attack(self.power)
            return True
        else:
            print(self.name,  "miss")
            return False


class ConditionCheckHp(Node):
    def __init__(self, name, hp_threshold, person, is_larger, child):
        super(ConditionCheckHp, self).__init__(name)
        self.child = None
        self.person = person
        self.hp_threshold = hp_threshold
        self.is_larger = is_larger
        self.child = child

    
    def run(self):
        
        if self.is_larger:
            if self.person.hp < self.hp_threshold  :
                return False
            else:
                if self.child != None:
                    self.child.run()
                return True
        else:
            if self.person.hp < self.hp_threshold  :
                if self.child != None:
                    self.child.run()
                return True
            else:
                return False


class Sequence(Node):
    def __init__(self, name):
        super(Sequence, self).__init__(name)
        self.childrenList = []
        self.status = None

    def addChild(self, node):
        self.childrenList.append(node)

    def run(self):
        for child in self.childrenList:
            if child.run() == False:
                return False
        return True

class Selector(Node):
    def __init__(self, name):
        super(Selector, self).__init__(name)
        self.childrenList = []
        self.status = None

    def addChild(self, node):
        self.childrenList.append(node)

    def run(self):
        for child in self.childrenList:
            if child.run():
                return True
        return False

class ActionNode(Node):
    def __init__(self, name, action):
        super(ActionNode, self).__init__(name)
        self.action = action
        self.status = None
        
    def run(self):
        print(self.action)
        self.status = True
        return self.status

class Paraller(Node):
    def __init__(self, name):
        super(Paraller, self).__init__(name)
        self.status = None
        self.childrenList = []

    def addChild(self,node):
        self.childrenList.append(node)

    def run(self):
        for child in self.childrenList:
            child.run()
        return True

class Repeater(Node):
    def __init__(self, name, i):
        super(Repeater, self).__init__(name)
        self.i = i
        self.childrenList = []

    def addChild(self, node):
        self.childrenList.append(node)

    def run(self):
        while self.i >=1:
            for child in self.childrenList:
                child.run()
            self.i = self.i - 1
        return True

#skill1発動確率P
P = 0.5

hp = 150
e_hp = 120
skill1_power = 50
skill2_power = 60
me = Person("me", hp)
enemy = Person("enemy", e_hp)


root = Sequence("root")

para1 = Paraller("para1")
re1 = Repeater("re1", 2)
se1 = Selector("se1")
se2 = Selector("se2")


act1 = ActionNode("act1", "出発")
act2 = ActionNode("act2", "敵に寄る")
act3 = ActionNode("act3", "友達Aを呼ぶ")
act4 = ActionNode("act4", "友達Bを呼ぶ")

act5 = ActionNode("act5", "end1")
act6 = ActionNode("act6", "end2")

check_me_hp_condition = ConditionCheckHp("check_me_hp_condition", 100, me, True, act2)
check_enemy_dead_condition = ConditionCheckHp("check_enemy_dead_condition", 1, enemy, False, act5)
check_enemy_alive_condition = ConditionCheckHp("check_enemy_alive_condition", 0, enemy, True,  act6)

skill_1 = Skill("skill_1", skill1_power, P)
skill_2 = Skill("skill_2", skill2_power, 1)
skill_1.setEnemy(enemy)
skill_2.setEnemy(enemy)


root.addChild(act1)
root.addChild(check_me_hp_condition)

root.addChild(para1)
para1.addChild(act3)
para1.addChild(act4)

root.addChild(re1)
re1.addChild(se1)
se1.addChild(skill_1)
se1.addChild(skill_2)

root.addChild(se2)
se2.addChild(check_enemy_dead_condition)
se2.addChild(check_enemy_alive_condition)

root.run()