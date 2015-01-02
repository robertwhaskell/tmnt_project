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
  return 0

def Make_Animals_Array():
  animals_array = []
  with open("animalnames.txt", "r")

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
  def __init__(self, name, bioe, sl, bonuses, powers):
    self.name = name
    self.bioe = bioe
    self.sl = sl
    self.bonuses = bonuses
    self.powers = powers
