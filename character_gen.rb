def roll_percentage
  (rand(100) + 1)
end

def roll_3_6
  roll = 0
  3.times {roll += (rand(6) + 1)}
end

def percentage_result(hash, roll)
  hash.keys.each do |key|
    if roll.between?(key[0], key[1])
      result = hash[key]
      return result
    end
  end
end

def generate_base_stats

  base_stats = {
    IQ: 0,
    ME: 0,
    MA: 0,
    PS: 0,
    PP: 0,
    PE: 0,
    PB: 0,
    Spd: 0
  }

  base_stats.keys.each do |stat|
    base_stats[stat] += roll_3_6
    base_stats[stat] += (rand(6) + 1) if base_stats[stat] >= 16
  end
  base_stats[:HP] = base_stats[:PE] + (rand(6) + 1)
  base_stats
end

def generate_animal
  animal_type = {
    [1, 35] => 'Urban',
    [36, 50] => 'Rural',
    [51, 75] => 'Wild',
    [76, 85] => 'Wild Birds',
    [86, 100] => 'Zoo'
  }
  category = percentage_result(animal_type, roll_percentage)

  recording = false
  previous_line = 'nope'
  animals = {}

  File.read('animals.txt').each_line do |l|
    recording = true if previous_line.strip == category
    recording = false if l.strip == ''
    animals[[l.split[0].to_i, l.split[1].to_i]] = l.split[2] if recording
    previous_line = l
  end
  percentage_result(animals, roll_percentage)
end

def generate_mutation
  mutation_hash = {
    [1, 14] => 'Random Mutation',
    [15, 60] => 'Accidental Encounter',
    [61, 100] => 'Deliberate Experimentation'
  }
  result = percentage_result(mutation_hash, roll_percentage)
  if result == 'Deliberate Experimentation'
    deliberate_experimentation = {
      [1, 10] => ['Adopted', 2, 10, roll_3_6 * 1000],
      [11, 20] => ['Pet, happy', 0, 14],
      [21, 30] => ['Pet, unhappy', 0, 0, 0],
      [31, 40] => ['Experiment, unhappy', 0, 18, 2.times(1 + rand(6)) * 500],
      [41, 50] => ['Experiment, very unhappy', 0, 0, 0],
      [51, 60] => ['Educated Normal', 2, 8, 2.times(1 + rand(6)) * 2000],
      [61, 70] => ['Rescued', 0, 7, 2.times(1 + rand(6)) * 200],
      [71, 80] => ['Specialist, valued', 3, 10, (1 + rand(6)) * 10_000],
      [81, 90] => ['Specialist, ex-slave', 3, 8, 3.times(3 + rand(6)) * 10_000],
      [91, 100] => ['Assassin', 0, 8, (1 + rand(6)) * 20_000]
    }
    result = percentage_result(deliberate_experimentation, roll_percentage)
  end
  if ['Random Mutation', 'Accidental Encounter', 'Pet, unhappy', 'Experiment, very unhappy'].include? result
    wild_animal_education = {}
  end
end

def get_sl_bio(animal, file)
  previous_line = 'nope'
  file.each_line do |line|
    return [line.strip.split[0].to_i, line.strip.split[1].to_i] if previous_line == animal
    previous_line = line.strip
  end
end

def get_appearances(animal, file)
  appearance_array = []
  previous_line = 'nope'
  found_animal = false
  record_appearances = false
  file.each_line do |line|
    return appearance_array if found_animal && line.strip == '***'
    found_animal = true if previous_line == animal
    record_appearances = true if previous_line == '==='
    if found_animal && record_appearances
      l = line.strip.split
      array = []
      (0..((l.length / 3) - 1)).each {|n| array.push([l[0 + (3 * n)], l[1 + (3 * n)], l[2 + (3 * n)].to_i])}
      appearance_array.push(array)
    end
    previous_line = line.strip
  end
  appearance_array
end

def get_powers(animal, file)
  powers_array = []
  previous_line = 'nope'
  found_animal = false
  record = false
  file.each_line do |line|
    return powers_array if found_animal && line.strip == ''
    found_animal = true if previous_line == animal
    record = true if found_animal && previous_line == '***'
    if found_animal && record
      l = line.strip.split
      powers_array.push([l[0], l[1], l[2].to_i])
    end
    previous_line = line.strip
  end
  powers_array
end

def get_bonuses(animal, file)
  previous_line = 'nope'
  found_animal = false
  file.each_line do |line|
    found_animal = true if previous_line == animal
    if previous_line == '+++' && found_animal
      l = line.strip.split
      return {
       IQ: l[0].to_i,
       ME: l[1].to_i,
       MA: l[2].to_i,
       PS: l[3].to_i,
       PP: l[4].to_i,
       PE: l[5].to_i,
       PB: l[6].to_i,
       Spd: l[7].to_i
      }
    end
    previous_line = line.strip
  end
end

def randomly_remove_dups(powers)
  powers.shuffle!
  pruned_powers = []
  dup_check = []
  powers.each do |e|
    next if dup_check.include? e[0]
    dup_check.push(e[0])
    pruned_powers.push(e)
  end
  pruned_powers
end

def adjust_for_size(powers, sl)
  (14 - sl).times {powers.push(['sl up', 'sl', 5])} if sl - 8 < 0
  (sl - 10).times {powers.push(['sl down', 'sl', -5])} if sl - 10 > 0
  if sl.between?(8, 10)
    2.times {powers.push(['sl up', 'sl', 5])}
    2.times {powers.push(['sl down', 'sl', -5])}
  end
  powers
end

def get_size_bonus(sl)
  size_chart = {
    1 => {IQ: -8, PS: -12, PE: -4, Spd: 7, SDC: 5},
    2 => {IQ: -6, PS: -6, PE: -2, Spd: 5, SDC: 10},
    3 => {IQ: -4, PS: -3, PE:  -1, Spd: 3, SDC: 15},
    4 => {IQ: -2, PS: -2, PE:  0, Spd: 0, SDC: 20},
    5 => {IQ: 0, PS: -1, PE: 0, Spd: 0, SDC: 25},
    6 => {IQ: 0, PS: 0, PE: 0, Spd: 0, SDC: 30},
    7 => {IQ: 0, PS: 1, PE: 0, Spd: 0, SDC: 30},
    8 => {IQ: 0, PS: 2, PE: 0, Spd: 0, SDC: 35},
    9 => {IQ: 0, PS: 3, PE: 1, Spd: 0, SDC: 35},
    10 => {IQ: 0, PS: 4, PE: 2, Spd: 0, SDC: 35},
    11 => {IQ: 0, PS: 5, PE: 3, Spd: -1, SDC: 40},
    12 => {IQ: 0, PS: 6, PE: 4, Spd: -2, SDC: 40},
    13 => {IQ: 0, PS: 7, PE: 5, Spd: -3, SDC: 45},
    14 => {IQ: 0, PS: 8, PE: 6, Spd: -4, SDC: 50},
    15 => {IQ: 0, PS: 9, PE: 7, Spd: -5, SDC: 55},
    16 => {IQ: 0, PS: 10, PE: 8, Spd: -6, SDC: 60},
    17 => {IQ: 0, PS: 11, PE: 9, Spd: -7, SDC: 65},
    18 => {IQ: 0, PS: 12, PE: 10, Spd: -8, SDC: 70},
    19 => {IQ: 0, PS: 13, PE: 11, Spd: -9, SDC: 75},
    20 => {IQ: 0, PS: 14, PE: 12, Spd: -10, SDC: 80},
  }
  return size_chart[sl]
end

def apply_bonuses(base_stats, size_bonus, animal_bonus)
  base_stats.keys.each do |stat|
    base_stats[stat] += animal_bonus[stat] if animal_bonus[stat]
    base_stats[stat] += size_bonus[stat] if size_bonus[stat]
    base_stats[:SDC] = size_bonus[:SDC]
  end
  base_stats
end

def assign_points(points, available_powers, selected_powers)
  return selected_powers if points == 0
  available_powers.each do |power|
    next if points - power[2] < 0
    selected_powers.push(power[0])
    diminished_powers_list = available_powers.dup
    diminished_powers_list.delete_at(available_powers.index(power))
    result = assign_points(
      points - power[2],
      diminished_powers_list,
      selected_powers
    )
    return result if result
    selected_powers.pop
  end
  return false
end

def make_character
  file = File.read('animal_powers.txt')
  base_stats = generate_base_stats
  animal_type = generate_animal
  sl_bio = get_sl_bio(animal_type, file)
  sl = sl_bio.shift
  bio = sl_bio.shift
  appearances = get_appearances(animal_type, file)
  animal_bonuses = get_bonuses(animal_type, file)
  powers = randomly_remove_dups(get_powers(animal_type, file))
  powers = adjust_for_size(powers, sl)
  powers = assign_points(bio, powers.shuffle, [])
  size_bonus = get_size_bonus(sl)
  base_stats = apply_bonuses(base_stats, size_bonus, animal_bonuses)
end

make_character
