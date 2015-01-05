def Make_Powers_Array():
  power_array = []
  with open("powers.txt", "r") as powers:
    for line in powers.readlines():
      power = line.split()
      if len(power) == 2:
        power_array.append(Other_Power(power[0], int(power[1])))
      elif len(power) == 3:
        power_array.append(Attack_Power(power[0], int(power[1]), power[2]))
      elif len(power) == 4:
        power_array.append(Defense_Power(power[0], int(power[1]), power[2], power[3]))
  return power_array

def Make_Animals_Array():
  animals_array = []
  with open("animalnames.txt", "r") as animals:
    line_counter = 0
    name = ""
    bioe = 0
    sl = 0
    bonuses = []
    powers = []
    for line in animals.readlines():
      if line_counter == 5:
        animals_array.append(Animal(name, bioe, sl, bonuses, powers))
        line_counter = 0
      if line_counter == 0:
        name = line.strip()
      elif line_counter == 1:
        bioe = int(line)
      elif line_counter == 2:
        sl = int(line)
      elif line_counter == 3:
        bonuses = line.split()
      elif line_counter == 4:
        powers = line.split()
      line_counter += 1
  return animals_array

def Make_Skills_Array():
  skills_array = []
  with open("physicalskills.txt", "r") as skills:
    line_counter = 0
    name = ""
    bonuses = []
    for line in skills.readlines():
      if line_counter == 0:
        name = line.strip()
        line_counter += 1
      elif line_counter == 1:
        bonus_list = []
        bonuses = line.split()
        bcounter = 0
        attr = ""
        bonus_figure = ""
        for bonus in bonuses:
          if bcounter == 0:
            attr = bonus
            bcounter += 1
          elif bcounter == 1:
            bonus_figure = bonus
            bonus_list.append(Skill_Bonus(attr, bonus_figure))
            bcounter = 0
        skills_array.append(Physical_Skill(name, bonus_list))
        line_counter = 0
  return skills_array

def Make_Male_First_List():
  names_list = []
  with open("malefirstnames.txt", "r") as names:
    for line in names.readlines():
      names_list.append(line.strip())
  return names_list

def Make_Female_First_List():
  names_list = []
  with open("femalefirstnames.txt", "r") as names:
    for line in names.readlines():
      names_list.append(line.strip())
  return names_list

def Make_Last_Names_List():
  names_list = []
  with open("lastname.txt", "r") as names:
    for line in names.readlines():
      names_list.append(line.strip())
  return names_list

class Skill_Bonus(object):
  def __init__(self, attr, bonus):
    self.attr = attr
    self.bonus = bonus

class Physical_Skill(object):
  def __init__(self, name, bonuses):
    self.name = name
    self.bonuses = bonuses

class Attack_Power(object):
  def __init__(self, name, cost, attack_die):
    self.name = name
    self.cost = cost
    self.attack_die = attack_die

class Defense_Power(object):
  def __init__(self, name, cost, ar, sdc):
    self.name = name
    self.cost = cost
    self.ar = ar
    self.sdc = sdc

class Other_Power(object):
  def __init__(self, name, cost):
    self.name = name
    self.cost = cost

class Animal(object):
  hp = 0
  sdc = 0
  stats = {}
  skills = []
  def str(self):
    print self.name
    print self.stats
    print "hp = " + str(self.stats['HP'])
    print "sdc = " + str(self.stats['SDC'])
    print "bioe = " + str(self.bioe)
    print "sl = " + str(self.sl)
    powlist = []
    for power in self.powers:
      powlist.append(power.name)
    print powlist
  def __init__(self, name, bioe, sl, bonuses, powers):
    self.name = name
    self.bioe = bioe
    self.sl = sl
    self.bonuses = bonuses
    self.powers = powers

