def Make_Powers_Array():
  power_array = []
  with open("powers.txt", "r") as powers:
    for line in powers.readlines():
      power = line.split()
      if len(power) == 2:
        power_array.append(Other_Power(power[0], power[1]))
      elif len(power) == 3:
        power_array.append(Attack_Power(power[0], power[1], power[2]))
      elif len(power) == 4:
        power_array.append(Defense_Power(power[0], power[1], power[2], power[3]))
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
  def str(self):
    print self.name
    print self.bioe
    print self.sl
    print self. bonuses
    print self.powers
  def __init__(self, name, bioe, sl, bonuses, powers):
    self.name = name
    self.bioe = bioe
    self.sl = sl
    self.bonuses = bonuses
    self.powers = powers

powers = Make_Powers_Array()
animals = Make_Animals_Array()
for an in animals:
  print an.str()
  print ""
