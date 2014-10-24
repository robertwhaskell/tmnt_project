def roll_percentage
  (rand(100) + 1)
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
    3.times {base_stats[stat] += (rand(6) + 1)}
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
  deliberate_experimentation = {
    [1, 10] => 'Adopted'
  }
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
    return line.strip.split if previous_line == '+++' && found_animal
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
    2.times {final_power_list.push(['sl up', 'sl', 5])}
    2.times {final_power_list.push(['sl down', 'sl', -5])}
  end
  powers
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
  bonuses = get_bonuses(animal_type, file)
  powers = randomly_remove_dups(get_powers(animal_type, file))
  powers = adjust_for_size(powers, sl)
  powers = assign_points(bio, powers.shuffle, [])
end

make_character






