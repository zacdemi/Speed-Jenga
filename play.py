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
        print(scale.__dict__)
        input("Press enter to start the game")
        clear_screen()
        
        while True:
           
            game.current_player().start_turn()
            sound.start_turn()
            print (game.scoreboard())
            
            while (scale.on() or scale.paused()) and not game.current_player().out_of_time():
                print (game.current_player().status(), end="\r")

                if game.current_player().current_time() <= 10 and not countdown:
                    sound.warning()
                    countdown = True
         
                if scale.paused() and not game.current_player().out_of_pause_blocks():
                    sound.stop_all()
                    game.current_player().pause_turn()
                    sound.pause_turn()

                    clear_screen()
                    print (game.scoreboard())
                    print (game.current_player().status())

                    while scale.paused():
                        print(scale.__dict__['pause'],scale.current_weight(),scale.status())

                    game.current_player().start_turn()
                    sound.start_turn()
                    clear_screen()
     
            sound.stop_all()
            game.current_player().end_turn()
            countdown = False
            clear_screen()

            #check if player is out of the game
            if game.current_player().out_of_time() or scale.disqualified():
                game.current_player().out_of_game = True
                sound.out_of_game()
            else:
                sound.end_turn()

            #check if game is over
            if game.one_player_remains() or scale.collapsed():
                if scale.collapsed():
                    game.current_player().out_of_game = True
                    game.current_player().knock_over_tower = True
                break 

            #check if end of round
            if game.round_complete():
                game.end_round()

            #display game info
            print (game.scoreboard())
            print (game.current_player().status())
            print (f"next player: {game.next_player_name()} ({game.next_player_current_time()})")

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
                    game.current_player().destroyer = True
                    game.current_player().out_of_game = True
                    break
                else:
                    print ("success!")
                    game.moves += 1

            game.move_to_next_player()
            clear_screen()

        scale.stop()

        game.end_game()
        clear_screen()
        print ("GAME OVER\n")
        print (game.scoreboard())
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

