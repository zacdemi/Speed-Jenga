#!/usr/bin/env python3
from lib.game import Game
from lib.scale import Scale
from lib.config import TEST_MODE
from lib.term_controls import clear_screen
from lib.sounds import Sounds
import threading
import json
import time
import pprint

def player_names(n):
    """ prompt the users for a list of player names """
    player_names = []
    for p in range(n):
        name = input(f"Who is player {p + 1}? ")
        player_names.append(name)
    return player_names

def main():
    print ("Welcome to ScaleJenga!")

    #init sounds
    sound = Sounds()

    #setup players
    if TEST_MODE:
        players = ["Tuna","Trout","QV","Clover"]
    else:
        number_of_players = int(input('How many players? '))
        players = player_names(number_of_players)

    while True:
        
        game = Game(players)
        scale = Scale()
        countdown = False

        clear_screen()
        print("tower details:")
        #print(scale.__dict__)
        input("Press enter to start the game")
        clear_screen()
        
        while True:
           
            game.current_player().start_turn()
            sound.start_turn()
            print(game._str_moves())
            
            while (scale.on() or scale.paused()) and not game.out_of_game_seconds():
                print (f'Time Remaining: {game.sum_of_player_times()}',end="\r")
         
                if scale.paused() and not game.current_player().out_of_pause_blocks():
                    sound.stop_all()
                    game.current_player().pause_turn()
                    sound.pause_turn()

                    clear_screen()
                    print(game._str_moves())
                    print ('Time Remaining',game.sum_of_player_times())
                    print (f'{game.current_player().name} has paused the game')
                    
                    while scale.paused():
                        pass

                    game.current_player().start_turn()
                    sound.start_turn()
                    clear_screen()
     
            sound.stop_all()
            game.current_player().end_turn()
            game.save_data()
            countdown = False
            clear_screen()
            sound.end_turn()

            #check if game is over
            if game.sum_of_player_times() <= 0 or scale.collapsed():
                break 

            #check if end of round
            if game.round_complete():
                game.end_round()

            #display game info
            print ('Time Remaining',game.sum_of_player_times())
            print (f'Next player: {game.next_player_name()}')

            #prompt user for next turn
            if scale.on():
                input("Press enter to start next turn")
            else:
                print ("waiting for tower to be restored...")

                while scale.off() or scale.disqualified():
                    pass
                    #print (scale.status(), end="\r")

                s = game.stability_seconds()            
                print (f"tower must stay stable for {s} second(s)...")
                time.sleep(s)

                if scale.collapsed():
                    break
                else:
                    print ("success!")
                    game.moves += 1

            game.move_to_next_player()
            game.save_data()
            clear_screen()

        scale.stop()

        game.end_game()
        clear_screen()
        print ("GAME OVER\n")
        print(game._str_moves())
        #pprint.pprint(game.data,indent=4)
        game.graph()
       
        while True: 
            answer = input("Would you like to play again? y/n: ")
            if answer in ['n','N','no','No','y','Y','yes','Yes']:
                break
            else:
               print ("{} is not an option: Please try again.".format(answer))

        if answer in ['n','N','no','No']: 
            break
        print("Thanks for playing!")
         
         
        #print json.dumps(game.data, indent=4)

if __name__ == "__main__":
     main()

