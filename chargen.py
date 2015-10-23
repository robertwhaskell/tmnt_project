import AnimalPowers
import random
import os

powers_list = AnimalPowers.Make_Powers_Array()
animals_list = AnimalPowers.Make_Animals_Array()
skills_list = AnimalPowers.Make_Skills_Array()
male_first_names = AnimalPowers.Make_Male_First_List()
female_first_names = AnimalPowers.Make_Female_First_List()
last_names = AnimalPowers.Make_Last_Names_List()

big_animal_preset = [
powers_list[len(powers_list) - 1],
powers_list[len(powers_list) - 1],
powers_list[len(powers_list) - 1],
powers_list[len(powers_list) - 1]
]

def Roll_3d6():
  total = 0
  for i in range(0, 3):
    total += random.randint(1, 6)
  return total

def get_stat():
  stat = Roll_3d6()
  if stat >= 16:
    stat += random.randint(1, 6)
  return stat

def get_hit_points(stats):
  return stats["PE"] + random.randint(1, 6)

def get_skills(num):
  temp_skill_list = list(skills_list)
  random.shuffle(temp_skill_list)
  final_skills = []
  for i in range(num):
    final_skills.append(temp_skill_list.pop())
  return final_skills

def apply_skill_bonuses(skills, stats):
  for skill in skills:
    for bonus in skill.bonuses:
      if 'd' in bonus.bonus:
        bon = 0
        breakdown = list(bonus.bonus)
        for i in range(int(breakdown[0])):
          bon += random.randint(1, int(breakdown[2]))
        stats[bonus.attr] += bon
      else:
        stats[bonus.attr] += int(bonus.bonus)
  return stats

def get_base_stats():
  stats = {}
  stats['IQ'] = get_stat()
  stats['ME'] = get_stat()
  stats['MA'] = get_stat()
  stats['PS'] = get_stat()
  stats['PP'] = get_stat()
  stats['PE'] = get_stat()
  stats['PB'] = get_stat()
  stats['SPD'] = get_stat()
  stats['HP'] = get_hit_points(stats)
  stats['SDC'] = 0
  stats['Punch/Fall'] = 0
  stats['Parry/Dodge'] = 0
  return stats

def apply_bonuses(bonuses, stats):
  if bonuses[0] != 'b':
    for i in range(0, len(bonuses), 2):
      stats[bonuses[i]] += int(bonuses[i + 1])
  return stats

def define_powers(animal):
  powers_array = []
  for animal_power in animal.powers:
    for power in powers_list:
      if animal_power == power.name:
        powers_array.append(power)
  if random.randint(1, 2) == 1:
    powers_array.append(AnimalPowers.Other_Power("hands_partial", 5))
  else:
    powers_array.append(AnimalPowers.Other_Power("hands_full", 10))
  if random.randint(1, 2) == 1:
    powers_array.append(AnimalPowers.Other_Power("bipedal_partial", 5))
  else:
    powers_array.append(AnimalPowers.Other_Power("bipedal_full", 10))
  if random.randint(1, 2) == 1:
    powers_array.append(AnimalPowers.Other_Power("looks_partial", 5))
  else:
    powers_array.append(AnimalPowers.Other_Power("looks_full", 10))
  if animal.stats["ME"] >= 12:
    with open("psionics.txt", "r") as psionics:
      for line in psionics.readlines():
        psionic_power = line.split()
        powers_array.append(AnimalPowers.Other_Power(psionic_power[0], int(psionic_power[1])))
  return powers_array

def assign_points(points, available_powers, selected_powers):
  if points == 0:
    return selected_powers
  for power in available_powers:
    if (points - power.cost >= 0):
      selected_powers.append(power)
      diminished_powers_list = list(available_powers)
      diminished_powers_list.remove(power)
      result = assign_points(points - power.cost, diminished_powers_list, selected_powers)
      if result != False:
        return result
      else:
        selected_powers.pop()
  return False

def add_size_change(animal):
  powers = animal.powers
  if animal.sl >= 16:
    for i in range(7):
      powers.append(powers_list[len(powers_list) - 1])
  else:
    for i in range(20 - animal.sl):
      powers.append(powers_list[len(powers_list) - 2])
    for i in range(animal.sl):
      powers.append(powers_list[len(powers_list) - 1])
  return powers

def too_big(animal):
  powers = animal.powers
  for i in range(4):
    powers.remove(powers_list[len(powers_list) - 1])
  return powers

def get_size_bonus(sl):

  size_chart = {
      1 : {"IQ": -8, "PS": -12, "PE": -4, "SPD": 7, "SDC": 5},
      2 : {"IQ": -6, "PS": -6, "PE": -2, "SPD": 5, "SDC": 10},
      3 : {"IQ": -4, "PS": -3, "PE":  -1, "SPD": 3, "SDC": 15},
      4 : {"IQ": -2, "PS": -2, "PE":  0, "SPD": 0, "SDC": 20},
      5 : {"IQ": 0, "PS": -1, "PE": 0, "SPD": 0, "SDC": 25},
      6 : {"IQ": 0, "PS": 0, "PE": 0, "SPD": 0, "SDC": 30},
      7 : {"IQ": 0, "PS": 1, "PE": 0, "SPD": 0, "SDC": 30},
      8 : {"IQ": 0, "PS": 2, "PE": 0, "SPD": 0, "SDC": 35},
      9 : {"IQ": 0, "PS": 3, "PE": 1, "SPD": 0, "SDC": 35},
      10 : {"IQ": 0, "PS": 4, "PE": 2, "SPD": 0, "SDC": 35},
      11 : {"IQ": 0, "PS": 5, "PE": 3, "SPD": -1, "SDC": 40},
      12 : {"IQ": 0, "PS": 6, "PE": 4, "SPD": -2, "SDC": 40},
      13 : {"IQ": 0, "PS": 7, "PE": 5, "SPD": -3, "SDC": 45},
      14 : {"IQ": 0, "PS": 8, "PE": 6, "SPD": -4, "SDC": 50},
      15 : {"IQ": 0, "PS": 9, "PE": 7, "SPD": -5, "SDC": 55},
      16 : {"IQ": 0, "PS": 10, "PE": 8, "SPD": -6, "SDC": 60},
      17 : {"IQ": 0, "PS": 11, "PE": 9, "SPD": -7, "SDC": 65},
      18 : {"IQ": 0, "PS": 12, "PE": 10, "SPD": -8, "SDC": 70},
      19 : {"IQ": 0, "PS": 13, "PE": 11, "SPD": -9, "SDC": 75},
      20 : {"IQ": 0, "PS": 14, "PE": 12, "SPD": -10, "SDC": 80},
  }
  return size_chart[sl]

def generate():
  gender = ""
  firstname = ""
  if random.randint(1, 2) == 1:
    firstname = male_first_names[random.randint(0, len(male_first_names))]
    gender = "Male"
  else:
    firstname = female_first_names[random.randint(0, len(female_first_names))]
    gender = "Female"
  lastname = last_names[random.randint(0, len(last_names))]
  print firstname + " " + lastname
  print gender
  animal = animals_list[random.randint(0, len(animals_list) - 1)]
  animal.stats = get_base_stats()
  animal.powers = define_powers(animal)
  animal.powers = add_size_change(animal)
  random.shuffle(animal.powers)
  if animal.bioe <= 10:
    animal.powers = assign_points(animal.bioe + 10, too_big(animal), big_animal_preset)
  else:
    animal.powers = assign_points(animal.bioe, animal.powers, [])
  powlist = []
  sizeup = 0
  sizedown = 0
  for power in animal.powers:
    if power.name == "size_up":
      sizeup += 1
    elif power.name == "size_down":
      sizedown += 1
    else:
      powlist.append(power)
  animal.powers = powlist
  animal.sl = animal.sl + sizeup - sizedown
  animal.stats = apply_bonuses(animal.bonuses, animal.stats)
  animal.hp = get_hit_points(animal.stats)
  bonus_set = get_size_bonus(animal.sl)
  num = random.randint(1, 7)
  animal.stats = apply_skill_bonuses(get_skills(num), animal.stats)
  for bonus in bonus_set:
    animal.stats[bonus] += bonus_set[bonus]

  with open("NewCharacter.txt", 'w') as new_character:
    new_character.write(firstname + " " + lastname + "\n")
    new_character.write(gender + " " + animal.name + "\n")
    if animal.stats['IQ'] >= 16:
      new_character.write('Smart ')
    if animal.stats['IQ'] <= 7:
      new_character.write('Dumb ')
    if animal.stats['MA'] >= 16:
      new_character.write('Charismatic ')
    if animal.stats['MA'] <= 7:
      new_character.write('Not_Charismatic ')
    if animal.stats['PS'] >= 16:
      new_character.write('Strong ')
    if animal.stats['PS'] <= 7:
      new_character.write('Weak ')
    if animal.stats['PP'] >= 16:
      new_character.write('Agile ')
    if animal.stats['PP'] <= 7:
      new_character.write('Clumsy ')
    if animal.stats['PE'] >= 16:
      new_character.write('Tough ')
    if animal.stats['PE'] <= 7:
      new_character.write('Not_Tough ')
    if animal.stats['PB'] >= 16:
      new_character.write('Beautiful ')
    if animal.stats['PB'] <= 7:
      new_character.write('Ugly ')
    if animal.stats['SPD'] >= 16:
      new_character.write('Fast ')
    if animal.stats['SPD'] <= 7:
      new_character.write('Slow ')
    new_character.write("\n")
    new_character.write("SL = " + str(animal.sl) + ", " + AnimalPowers.Return_SL_Description(animal.sl))
    new_character.write("\n")
    new_character.write("\n")
    new_character.write("HP = " + str(animal.stats["HP"]) + "\n")
    new_character.write("SDC = " + str(animal.stats["SDC"]) + "\n")
    new_character.write("Punch/Fall = " + str(animal.stats["Punch/Fall"]) + "\n")
    new_character.write("Parry/Dodge = " + str(animal.stats["Parry/Dodge"]) + "\n")
    new_character.write("\n")
    new_character.write("IQ = " + str(animal.stats["IQ"]) + "\n")
    new_character.write("ME = " + str(animal.stats["ME"]) + "\n")
    new_character.write("MA = " + str(animal.stats["MA"]) + "\n")
    new_character.write("PS = " + str(animal.stats["PS"]) + "\n")
    new_character.write("PP = " + str(animal.stats["PP"]) + "\n")
    new_character.write("PE = " + str(animal.stats["PE"]) + "\n")
    new_character.write("PB = " + str(animal.stats["PB"]) + "\n")
    new_character.write("SPD = " + str(animal.stats["SPD"]) + "\n")
    new_character.write("\n")

    power_string = "powers: ";
    for power in animal.powers:
      power_string += (power.name + ", ")
    
    if power_string == "powers: ":
      power_string += "none"

    new_character.write(power_string)
    
  



    for filename in os.listdir("."):
        if filename == "NewCharacter.txt":
            os.rename(filename, firstname + lastname)





  return animal

print generate().str()
























