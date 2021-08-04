#Jooj
def s_organization(target_position, plant_position):
  #getting all the S-Shooters
  s_list = []
  first_s_passed = False
  for plant_target_position in target_position:
    if 'S' in plant_target_position:
      pind = target_position.index(plant_target_position)
      if not first_s_passed:
        s_start_index = pind
        first_s_passed = True
      s_list.append([plant_position[pind], plant_target_position])

  #organizing them in another list
  s_organized_list = []
  for s_plant_stats in s_list:
    if s_organized_list == []:
      s_organized_list.append(s_plant_stats)
    else:
      for s_plant_stats_comparation_index in range(len(s_organized_list)):
        s_plant_stats_comparation = s_organized_list[s_plant_stats_comparation_index]
        p_position_comparation = s_plant_stats_comparation[0]
        p_position = s_plant_stats[0]
        if p_position[0] == p_position_comparation[0] and s_plant_stats not in s_organized_list:
          if p_position[1] < p_position_comparation[1]:
            s_organized_list.insert(s_plant_stats_comparation_index, s_plant_stats)
          else:
            if s_plant_stats_comparation_index == len(s_organized_list)-1:
              s_organized_list.append(s_plant_stats)
        elif p_position[0] > p_position_comparation[0] and s_plant_stats not in s_organized_list:
          s_organized_list.insert(s_plant_stats_comparation_index, s_plant_stats)
        else:
          if s_plant_stats_comparation_index == len(s_organized_list)-1:
            s_organized_list.append(s_plant_stats) 
            

  #giving back them to the original lists
  target_position_new = []
  plant_position_new = []
  for counter in range(s_start_index):
    target_position_new.append(target_position[counter])
    plant_position_new.append(plant_position[counter])
  for pind in range(len(s_organized_list)):
    s_plant_stats = s_organized_list[pind]
    target_position_new.append(s_plant_stats[1])
    plant_position_new.append(s_plant_stats[0])

  
  #return the new lists
  return target_position_new, plant_position_new





def add_zombies(zombie, health, row_spawn, zombies_position, lenght):
  health.append(zombie[2])
  zombies_position.append([lenght, row_spawn])
  return health, zombies_position


def plants_and_zombies(lawn,zombies):
  
  '''
  example_tests = [
    [
      [
        '2       ',
        '  S     ',
        '21  S   ',
        '13      ',
        '2 3     '],
      [[0,4,28],[1,1,6],[2,0,10],[2,4,15],[3,2,16],[3,3,13]]],
    [
      [
        '11      ',
        ' 2S     ',
        '11S     ',
        '3       ',
        '13      '],
      [[0,3,16],[2,2,15],[2,1,16],[4,4,30],[4,2,12],[5,0,14],[7,3,16],[7,0,13]]],
    [
      [
        '12        ',
        '3S        ',
        '2S        ',
        '1S        ',
        '2         ',
        '3         '],
      [[0,0,18],[2,3,12],[2,5,25],[4,2,21],[6,1,35],[6,4,9],[8,0,22],[8,1,8],[8,2,17],[10,3,18],[11,0,15],[12,4,21]]],
    [
      [
        '12      ',
        '2S      ',
        '1S      ',
        '2S      ',
        '3       '],
      [[0,0,15],[1,1,18],[2,2,14],[3,3,15],[4,4,13],[5,0,12],[6,1,19],[7,2,11],[8,3,17],[9,4,18],[10,0,15],[11,4,14]]],
    [
      [
        '1         ',
        'SS        ',
        'SSS       ',
        'SSS       ',
        'SS        ',
        '1         '],
      [[0,2,16],[1,3,19],[2,0,18],[4,2,21],[6,3,20],[7,5,17],[8,1,21],[8,2,11],[9,0,10],[11,4,23],[12,1,15],[13,3,22]]]
  ]
  example_solutions = [10,12,20,19,None]
  
  #Variables
  1)plant_position: list that agroup all the plants positions
  2)target_position: list that agroup all the shooter_list
  3)plant_damage: list that contains all the plants damage
  4)n_row: position of the row (like an y coord)
  5)row: string of the row
  6)position: position of the target (like an x coord)
  7)shooter_list: explained in Logic (1)
  8)possible_target: to construct shooter_list; contains all the x_positions in front of the plant
  9)n_shooter: contains the damage of the plant
  10)zi: index of each zombie
  11)lenght: lenght of each row
  12)zombies_cp: copy of the zombies list
  13)zombie_position: [x_zombie_position, y_zombie_position]
  14)pind: plant index
  14)zombies_position_cp: copy of the zombie_position list
  15)first_zombie_spawn: True if the first zombie have been spawned, and False if not 
  16)zombies_are_killed: True if no zombie have been left, and False if not
  17)plants_killed: list that contains all the killed plants on that round
  18)p_position: each plant position
  19)plant_target_position: all the positions that each plant can hit the target
  20)health_cp: copy of the health list
  21)zombie_health: health of each zombie
  22)possible_target_positions: it represents all the target possitions that are not blocked
  23)plant_damage_left: all the damage remaining to hit the zombies
  24)damage: damage that some zombie have gotten
  25)target: an unique target_position
  26)medium_line: refeer to the medium target_positions for a S-Shooter
  27)upper_line: refeer to the upper target_positions for a S-Shooter
  28)lower_line: refeer to the lower target_positions for a S-Shooter
  29)n_fire_line: the index of each line in the S-Shooter target_position
  30)S_list_damage: represent the S-Shooter's list that contains each line damage left 
  31)line_damage: each line damage left in a S-Shooter
  32)target_position_cp: copy of the target_position list
  33)plant_damage_cp: copy of the plant_damage list
  34)not_conflicted_pind: pind that doesn't conflict with the for loop
  35)s_list: list with the target_position and the plant_position of each S-Shooter
  36)first_s_passed: verify if the first S-Shooter have been added in the s_list
  37)s_start_ind: index of the first S-Shooter in the target_position list
  38)s_organized_list: s_list organized by order of shooting
  39)s_plant_stats: each S-Shooter stats in s_list
  40)s_plant_stats_comparation: s_plant_stats in s_organized_list used in a for loop
  41)p_position_comparation: s_plant_stats_comparation's position
  42)s_plant_stats_comparation_index: index of the s_plant_stats_comparation
  43)counter: variable to determinates how many times some for loop will occur
  44)target_position_new: target_position with organized S-Shooters stats, that will assign his values to the target_position
  45)plant_position_new: plant_position with organized S-Shooters stats, that will assign his values to the plant_position 
  46)map_reset: list that contains strings of each row, but all cleaned


  #Logic
  1) Creating a system that contains the position that each plant will get the zombie
  -notes: shooter_list format: [sequence of possible positions to get the target
  -notes2: if shooter_list refeer to a S-plant, it have an element 'S' to identify this type
  -notes3: organize the S-Shooters in order of fire (usage of a function)
  2) Creating lists that contains the health, the present position and when the zombies will be spawned. The index of each list represents each zombie
  3) The game itself 
  3.1) Changing the round
  3.2) Moving all the zombies, and excluding the plant if the zombie caches it up
  3.3) Verifying if some zombie is spawn
  3.4) Verifying the plants shoots
  3.5) Verifying if some zombie have been killed by the plants
  3.6) Verifying if all the zombies have been killed
  
  #Possible Errors:
  V - 1) "index()" conflicts if have two zombies in the same position
  V - 2) Damaging zombies: target_position is a list of lists, and in the damaging, the zombie_position have to be inside one of 
  those lists, not inside target_position
  V - 3) Blocking bullets for other zombies are not included
  V - 4) If an 4-plant kill some zombie with 2 balls, it have 2 balls left
  V - 5) If the row index and column index starts with 0 or 1
  V - 6) Error, maybe, in the zombies walking
  V - 7) N-Shooters fire before the S-Shooters
  V - 8) S-Shooters have a order to fire: right to left; then top to bottom
  V - 9) S-Shooters bullets are not being blocked
  10) Some plants do not receive damage from S-Shooter
  '''
  #1
  plant_position = []
  target_position = [] 
  plant_damage = []
  for n_row in range(len(lawn)):
    row = lawn[n_row]
    for position in range(len(row)):
      if row[position] == ' ': #Blank Spaces
        pass
        
      elif row[position] == 'S': #S-Shooter
        shooter_list = ['S']
        plant_position.append([position, n_row])
        plant_damage.append([1,1,1]) #upper, medium, lower

        #medium positions
        medium_line = []
        for possible_target in range(position + 1, len(row)):
          medium_line.append([possible_target, n_row])
        shooter_list.append(medium_line)

        #upper positions
        upper_line = []
        timer = 0
        while n_row-timer >= 0 and position+timer <= len(row)-1:
          upper_line.append([(position+timer), (n_row-timer)])
          timer += 1
        shooter_list.append(upper_line)

        #lower positions
        lower_line = []
        timer = 0
        while n_row+timer <= len(lawn)-1 and position+timer <= len(row)-1:
          lower_line.append([(position+timer), (n_row+timer)])
          timer += 1
        shooter_list.append(lower_line)
      
        target_position.append(shooter_list)

      else: #N-Shooter
        plant_position.insert(0,[position, n_row])
        n_shooter = int(row[position])
        plant_damage.insert(0, n_shooter)
        shooter_list = []
        for possible_target in range(position + 1, len(row)):
          shooter_list.append([possible_target, n_row])
        target_position.insert(0, shooter_list)

  target_position, plant_position = s_organization(target_position, plant_position)



  #2
  health = []
  zombies_position = []
  lenght = len(lawn[0]) - 1



  #3





  round = -1
  lose = False
  first_zombie_spawn = False
  zombies_are_killed = False
  while (not lose) and (not zombies_are_killed):

    #Round's change
    round += 1
    
    #Zombies Moving
    plant_position_cp = plant_position.copy()
    target_position_cp = target_position.copy()
    plant_damage_cp = plant_damage.copy()
    if zombies_position != []: #verify if have some zombie spawned
      for zombie_position in zombies_position:
        zombie_position[0] -= 1 #moving each zombie
        if zombie_position[0] == 0: #zombie reaches the first column
          lose = True
        if zombie_position in plant_position: #zombie kills some plant
          pind = plant_position.index(zombie_position)
          plant_position_cp = [p_position for p_position in plant_position_cp if p_position != zombie_position]
          not_conflicted_pind = target_position_cp.index(target_position[pind])
          target_position_cp = [target for target in target_position_cp if target != target_position[pind]]
          del plant_damage_cp[not_conflicted_pind]
    plant_position = plant_position_cp.copy()
    target_position = target_position_cp.copy()
    plant_damage = plant_damage_cp.copy()

    
    #Spawning 
    zombies_cp = zombies.copy()
    for zombie in zombies:
      if round >= zombie[0]:
        health, zombies_position = add_zombies(zombie, health, zombie[1], zombies_position, lenght)
        zombies_cp.remove(zombie)
    if zombies != zombies_cp: #verifying if the first zombie have been spawned
      first_zombie_spawn = True
    zombies = zombies_cp
    

    #Shooting   
    plant_damage_left = plant_damage.copy()
    possible_target_positions = target_position.copy()
    zombies_position_cp = zombies_position.copy()
    health_cp = health.copy()
    if zombies_position != []:
      for zombie_position in zombies_position:
        for pind in range(len(target_position)):
          plant_target_position = target_position[pind]
          zi = zombies_position.index(zombie_position)
          if 'S' in plant_target_position: #verifyng if this plant is a S-Shooter
            for n_fire_line in range(1, 4):
              S_list_damage = plant_damage_left[pind]
              for target in plant_target_position[n_fire_line]:
                if zombie_position == target and health_cp[zi] > 0 and S_list_damage[n_fire_line - 1] > 0: #verifying if the zombie is in a target_position
                  S_list_damage[n_fire_line - 1] -= 1
                  health_cp[zi] -= 1


          else: #verifying if this plant is a N-Shooter
            for target in plant_target_position:
              if zombie_position == target and health[zi] != 0 and plant_damage_left[pind] != 0: #verifying if the zombie is in a target_position
                while plant_damage_left[pind] != 0 and health_cp[zi] != 0:
                  plant_damage_left[pind] -= 1
                  health_cp[zi] -= 1
                  
    # OBS: For some reason, the .copy() used in plant_damage_left alternated the plant_damage list, and the S-Shooter damage in this list didn't reset. So, I have to use this.
    for damage_index in range(len(plant_damage)):
      if type(plant_damage[damage_index]) == list:
        plant_damage[damage_index] = [1,1,1]
    

    #Zombie Deaths
    health = health_cp.copy()
    for zi in range(len(health)):
      if health[zi] <= 0: #verifying if some zombie have been killed
        zombie_health = health[zi]
        zombie_position = zombies_position[zi]
        health_cp.remove(zombie_health)
        zombies_position_cp.remove(zombie_position)
    zombies_position = zombies_position_cp
    health = health_cp
    
    

    #Zombie's Chacine 
    if zombies_position == [] and first_zombie_spawn: #verifying if all the zombies have been killed
      zombies_are_killed = True  







  if lose:
    return round + 1 #+1 because we have to count round 0
  else:
    return None


