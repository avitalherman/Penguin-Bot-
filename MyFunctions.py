
# The function calculate the num of penguins on the way from src to dest
def my_group_on_the_way(game,src,des):
    for group in game.get_my_penguin_groups():
        if group.source==src and group.destination == des:
            return True
    return False


# The function returns all groups of penguins on the way to dest
def group_of_penguins_to_dest(group, dest):
    return sorted(filter(lambda group: group.destination == dest, group),key=lambda x: turns_till_arrival_of_group(x))


# The function determines the size of groups based on the size of enemy groups
def size_of_group(game, iceberg):
    x = 1
    if game.get_enemy_penguin_groups():
        size = cal_average_groups_size(game.get_enemy_penguin_groups())
        x = iceberg.penguin_amount // size if 3< size < iceberg.penguin_amount else 1
    elif not game.get_enemy_penguin_groups() and not game.get_my_penguin_groups():
        x += 1
    return x

# The functon checks if the iceberg can be upgraded and be safe
def check_upgrade(game, iceberg):
    turn = 1
    if not iceberg.can_upgrade():  
        return False
    level = iceberg.level + 1  
    enemy_penguins_to_iceberg = group_of_penguins_to_dest(game.get_enemy_penguin_groups(), iceberg)
    penguin_amount = iceberg.penguin_amount - iceberg.upgrade_cost
    if len(game.get_my_icebergs())==1 and len(game.get_enemy_icebergs())==1:
        if (calc_distance_from_icebergs(iceberg,game.get_enemy_icebergs())*level +penguin_amount) < game.get_enemy_icebergs()[0].penguin_amount:
            return False
    my_penguins_to_iceberg = group_of_penguins_to_dest(game.get_my_penguin_groups(), iceberg)
    penguins_to_iceberg = sorted(enemy_penguins_to_iceberg + my_penguins_to_iceberg,key=lambda x: turns_till_arrival_of_group(x))
    for group in penguins_to_iceberg:
        penguin_amount += (turns_till_arrival_of_group(group) - turn) * level
        turn = turns_till_arrival_of_group(group)
        if group in my_penguins_to_iceberg:
            penguin_amount =  penguin_amount+group.penguin_amount
        else:
            penguin_amount -= group.penguin_amount
            if penguin_amount <= 0:
                return False
    return True


# Calculate turns till arrival with bridge
def calc_turns_till_arrival(game, group):
    src  = group.source 
    dest=group.destination
    bridge= None
    bridges_from_src = src.bridges
    bridges_to_dest= dest.bridges
    for brdg in bridges_to_dest:
        if brdg in bridges_from_src:
            bridge= brdg
    if not bridge:
        return group.turns_till_arrival
    if bridge.duration >= group.turns_till_arrival:
        return int(group.turns_till_arrival // bridge.speed_multiplier)
    return int((group.turns_till_arrival - bridge.duration) + (bridge.duration // bridge.speed_multiplier))

#The function calculate number of turns till penguin_group will arrive
def turns_till_arrival_of_group(penguin_group):
    source_ice = penguin_group.source
    destination_ice = penguin_group.destination
    dur = 0
    if len(source_ice.bridges) != 0:
        my_bridge = filter(lambda x: destination_ice in x.get_edges(), source_ice.bridges)
        if len(my_bridge) != 0:
            dur = my_bridge[0].duration
    return penguin_group.turns_till_arrival - min(int(penguin_group.turns_till_arrival + 1)*0.5, dur)


# The function return the owner of Specific penuins groups
def owner_of_Specific_group(penuins_groups,icebergs):
    for i in penuins_groups:
        if i.destination in icebergs:
            return i.source
    return None


# The function return all the icebergs with the same owner who are in danger of being conquered      
def attackted_icebergs(game, iceberg):
    help = []
    for i in game.get_my_icebergs():
        if i != iceberg and calc_future_owner_of_iceberg(game, i, iceberg.get_turns_till_arrival(i))[0] == game.get_enemy():   
            help.append(i)
    return help
  
     
#The function calculate the distance between 2 icebergs
def calc_distance_from_icebergs(src_iceberg, icebergs):
    infinite=100000000
    dist = 0
    if len(icebergs)==0:
        return infinite
    for ice in icebergs:
        dist += ice.get_turns_till_arrival(src_iceberg)
    dist=dist/len(icebergs)
    return dist
          
# The function return list with all the enemy icebergs that worth building a bridge to
def find_potential_bridge(game, iceberg):
    des_icebergs =  []
    for i in game.get_my_penguin_groups():
        if i.destination.owner == game.get_enemy() and i.source == iceberg and i.penguin_amount > game.iceberg_bridge_cost and calc_turns_till_arrival(game, i) / iceberg.max_bridge_duration >= 0.5:
                des_icebergs += [i.destination]
    return des_icebergs
    

#The function calculate average size of all groups of penguins (without decoys
def cal_average_groups_size(groups):
    num_penguins=0
    num_groups=0
    for x in groups:
        if not x.decoy:
            num_penguins += x.penguin_amount
            num_groups += 1
    return num_penguins // num_groups


#The function return all the groups of penguins without decoys
def num_of_groups(iceberg, groups):
    num_groups = 0
    for i in groups:
        if i.destination == iceberg and not i.decoy:
            num_groups += i.penguin_amount
    return num_groups
 
    
#The function return enemy iceberg to attack
def des_to_attack(game, ice):
    des = None
    for i in game.get_my_penguin_groups():
        owner, amount_of_penuins = calc_future_owner_of_iceberg(game, i.destination, ice.get_turns_till_arrival(i.destination))
        if owner == game.get_enemy() and i.penguin_amount > i.source.level and not i.decoy and (not des or ice.get_turns_till_arrival(i.destination) < ice.get_turns_till_arrival(des)): 
            return  i.destination
   
# The function return if the enemy is dangerous        
def enemy_is_dangerous(game, icberg, penguin_amount):
    icebergs = sorted(game.get_all_icebergs(), key = lambda x: icberg.get_turns_till_arrival(x))
    icebergs = icebergs[1:len(icebergs)//3]
    for i in icebergs:
        if i.owner != game.get_enemy():
            return False
    if sum(i.penguin_amount for i in icebergs) < (icberg.penguin_amount - penguin_amount):
        return False
    return True


# A function that check the consequences of making an update
def if_can_upgrade(game, iceberg):
    return iceberg.can_upgrade() and calc_future_owner_of_iceberg(game, iceberg, iceberg.upgrade_cost //iceberg.level, iceberg.upgrade_cost)[0] != game.get_enemy()


# A function that checks if the enemy is using decoy
def using_decoy(game):
    for i in game.get_enemy_penguin_groups():
        if i.decoy:
            return True
    return False


# The function return thde function to do sort
def  do_sort(iceberg):
    return lambda x:  x.penguin_amount*0.1 + iceberg.get_turns_till_arrival(x)*0.9
    


# Calculatee the iceberg state (owner and penguin_amount) in x turns
def calc_future_owner_of_iceberg(game, iceberg, time, sended=0):
    ice_owner = iceberg.owner
    penguin_amount = iceberg.penguin_amount - sended
    if penguin_amount < 0: #change owner
        if ice_owner != game.get_enemy():
            ice_owner = game.get_enemy()
        else:
            ice_owner=game.get_myself()
        penguin_amount = penguin_amount*-1
    penguin_groups = sorted([i for i in game.get_my_penguin_groups()+game.get_enemy_penguin_groups() if calc_turns_till_arrival(game, i) <= time and i.destination == iceberg], key=lambda x: calc_turns_till_arrival(game, x))
    current = 0
    for group in penguin_groups: # run on all gruop of penguins that on the way to iceberg 
        if group.decoy:
            continue
        turns_till_arrival = calc_turns_till_arrival(game, group)
        if ice_owner != game.get_neutral() and not iceberg.equals(game.get_bonus_iceberg()):
            penguin_amount =penguin_amount+ ((turns_till_arrival-current) * iceberg.level)
        if group.owner == ice_owner:
            penguin_amount = penguin_amount+group.penguin_amount
        else:
            penguin_amount= penguin_amount-group.penguin_amount
        if penguin_amount < 0: # change owner
            ice_owner = group.owner
            penguin_amount = penguin_amount*-1
        if penguin_amount == 0: # natural iceberg
            ice_owner = game.get_neutral()
        current = turns_till_arrival
    if ice_owner != game.get_neutral() and not iceberg.equals(game.get_bonus_iceberg()):  
        penguin_amount = penguin_amount+((time-current) * iceberg.level)
    return (ice_owner, penguin_amount)
    
    

    