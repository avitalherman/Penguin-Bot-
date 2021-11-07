from penguin_game import *
from MyFunctions import *



    
def do_turn(game):
    my_decoy = None
    my_const=7
    
    for my_iceberg in game.get_my_icebergs():
        if game.turn>288 and len(game.get_all_icebergs()) == 5: 
            des=sorted([(my_iceberg.get_turns_till_arrival(i), i) for i in game.get_neutral_icebergs()],
                                key=lambda tup: tup[0])[0][1]
            if my_iceberg.penguin_amount>des.penguin_amount:
                my_iceberg.send_penguins(des, des.penguin_amount+1)
        my_penguin_amount = my_iceberg.penguin_amount 
        destination_penguin_amount = 0
        natural_ice = sorted(game.get_neutral_icebergs(), key = lambda x: my_iceberg.get_turns_till_arrival(x)) 
        if game.get_neutral_icebergs() and len(natural_ice)>1:
            neutral= natural_ice[1]
        elif game.get_neutral_icebergs():
            neutral= natural_ice[0]
        if game.get_enemy_icebergs():
           enemy = sorted(game.get_enemy_icebergs(), key = do_sort(my_iceberg))[0]
        bridge_des =  find_potential_bridge(game, my_iceberg) 
        if bridge_des:
            bridge = bridge_des[0] 
        else:
            bridge = None
        natural_and_enemy=sorted(game.get_enemy_icebergs()+game.get_neutral_icebergs(), key = do_sort(my_iceberg))
        decoy = None
        if not decoy:
            decoy = natural_and_enemy[0]
        group_size = size_of_group(game , my_iceberg)
        bonus = 0
        if game.get_bonus_iceberg() and game.get_bonus_iceberg().owner == game.get_enemy() :
            bonus = game.get_bonus_iceberg().penguin_bonus
        
        protect_ice = sorted(attackted_icebergs(game, my_iceberg), key = do_sort(my_iceberg))
        protect = None
        if len(protect_ice)>=1 :
            protect = protect_ice[0] 
        my_icebergs=sorted(game.get_my_icebergs(), key = do_sort(my_iceberg))    
        if protect   and my_iceberg.get_turns_till_arrival(protect)<=my_iceberg.get_turns_till_arrival(enemy):  
            destination = protect
        elif not my_decoy and des_to_attack(game, my_iceberg) and len(game.get_my_icebergs()) < len(game.get_enemy_icebergs()) and my_iceberg.get_turns_till_arrival(des_to_attack(game, my_iceberg))<=10: 
            destination = des_to_attack(game, my_iceberg)
        elif game.get_neutral_icebergs() and not owner_of_Specific_group(game.get_enemy_penguin_groups(), my_icebergs) and my_iceberg.get_turns_till_arrival(neutral) <9:
            if len(game.get_neutral_icebergs()) >= 2 and num_of_groups(natural_ice[0], game.get_my_penguin_groups()):
                destination = natural_ice[1]
            else: 
                destination = natural_ice[0]       
        elif game.get_neutral_icebergs()  and my_iceberg.get_turns_till_arrival(natural_ice[0])<=10:
            destination = natural_ice[0]  
        elif enemy:
            if  my_decoy == None:
                my_decoy = enemy
                destination = enemy
            else:
                destination = my_decoy
        else:
            destination=natural_and_enemy[0]
        if my_iceberg.get_turns_till_arrival(destination)>=25:
            destination=natural_and_enemy[0]
        des_own, des_amount = calc_future_owner_of_iceberg(game, destination, my_iceberg.get_turns_till_arrival(destination))
        
        if des_amount > my_penguin_amount  and des_own == game.get_enemy():
             destination_penguin_amount = des_amount//group_size
        else:
            destination_penguin_amount = des_amount
        destination_penguin_amount += bonus
        if game.get_bonus_iceberg():
            bonus_ice=sorted(game.get_my_icebergs(), key=lambda x: x.get_turns_till_arrival(game.get_bonus_iceberg()))
        my_owner, my_amount = calc_future_owner_of_iceberg(game, my_iceberg, my_iceberg.get_turns_till_arrival(destination), destination_penguin_amount)
        if enemy_is_dangerous(game, my_iceberg, destination_penguin_amount) or (num_of_groups(my_iceberg, game.get_enemy_penguin_groups()) and my_owner == game.get_enemy()): 
            continue
        elif (len(game.get_my_icebergs()) >= len(game.get_enemy_icebergs())) and if_can_upgrade(game, my_iceberg) and not(game.turn < 10 and my_iceberg.level > 1) :
            my_iceberg.upgrade()
            continue
        elif bridge and my_iceberg.can_create_bridge(bridge) and ((my_iceberg.level > 1 and my_iceberg.get_turns_till_arrival(bridge) >= my_const and num_of_groups(bridge,game.get_my_penguin_groups())>=my_const)): 
            my_iceberg.create_bridge(bridge)
            continue
        elif (len(game.get_my_icebergs()) >= len(game.get_enemy_icebergs())) and check_upgrade(game, my_iceberg):
            my_iceberg.upgrade()
            continue
        elif game.get_bonus_iceberg() and ((len(game.get_my_icebergs()) >= len(game.get_enemy_icebergs())and num_of_groups(game.get_bonus_iceberg(),game.get_enemy_penguin_groups())) or (game.get_bonus_iceberg().owner == game.get_enemy())) and my_iceberg in bonus_ice[0: len(bonus_ice)//2] :
            des_own, des_amount = calc_future_owner_of_iceberg(game, game.get_bonus_iceberg(),my_iceberg.get_turns_till_arrival(game.get_bonus_iceberg()))
            if des_own != game.get_myself and my_iceberg.penguin_amount > des_amount :
                my_iceberg.send_penguins(game.get_bonus_iceberg(), des_amount+1)
        elif using_decoy(game) and  my_iceberg.penguin_amount +2 > destination_penguin_amount*2   and my_iceberg.can_send_decoy_penguins(destination, natural_and_enemy[len(natural_and_enemy)//2], destination_penguin_amount) :
            destination_penguin_amount=destination_penguin_amount//2 
            my_iceberg.send_decoy_penguins(destination,natural_and_enemy[len(natural_and_enemy)//2], destination_penguin_amount +1) 
        #else:
            """
            if not my_group_on_the_way(game, my_iceberg,destination) and destination in game.get_neutral_icebergs() and game.turn<20:
                my_iceberg.send_penguins(destination, destination_penguin_amount +1)
            elif destination not in game.get_neutral_icebergs():
                my_iceberg.send_penguins(destination, destination_penguin_amount +1)
            elif game.turn>20:
                my_iceberg.send_penguins(destination, destination_penguin_amount +1)
            """
        elif my_iceberg.penguin_amount > destination_penguin_amount :
            my_iceberg.send_penguins(destination, destination_penguin_amount +1)
        
        if protect_ice:
            des_own, des_amount = calc_future_owner_of_iceberg(game, destination, my_iceberg.get_turns_till_arrival(protect_ice[0]))
            amount = des_amount
            while amount >= my_iceberg.penguins_per_turn:
                if my_owner == game.get_myself(): 
                    break
                amount //= 2
            #if my_iceberg.penguin_amount > amount + 1:
            my_iceberg.send_penguins(protect_ice[0], amount)
                    
       