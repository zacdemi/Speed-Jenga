#!/usr/bin/env python3
from lib.game import Game
from lib.scale import Scale
from lib.term_controls import clear_screen
from lib.sounds import Sounds
import threading
import json
import time

def player_names(n):
    """ prompt the users for a list of player names """
    player_names = []
    for p in range(n):
        name = input("Who is player %s? " % (p + 1))
        player_names.append(name)
    return player_names

def main():
    print ("Welcome to ScaleJenga!")

    #init sounds
    sound = Sounds()

    #setup players
    number_of_players = int(input('How many players? '))
    players = player_names(number_of_players)

    while True:
        
        game = Game(players)
        scale = Scale()

        clear_screen()
        input("Press enter to start the game")
        clear_screen()
         

        while True:
           
            game.current_player().start_turn()
            sound.start_turn()
     
            
            print (game.scoreboard())
            while (scale.on() or scale.paused()) and not game.current_player().out_of_time():
                print (game.current_player().status(), end="\r")
         
                if scale.paused() and not game.current_player().out_of_pause_blocks():
                    game.current_player().pause_turn()
                    sound.pause_turn()

                    clear_screen()
                    print (game.current_player().status())

                    while scale.paused():
                        pass

                    game.current_player().start_turn()
                    sound.start_turn()
                    clear_screen()
     
            game.current_player().end_turn()
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

            #display game info
            print (game.current_player().status())

            if scale.on():
                input("Press enter to start next turn")
                print ("next player: {name}".format(name=game.next_player_name()))
            else:
                print ("waiting for tower to be restored...")
                print ("next player: {name}".format(name=game.next_player_name()))

                while scale.off() or scale.disqualified():
                    #pass
                    print (scale.status(), end="\r")

                s = game.stability_seconds()            
                print ("tower must stay stable for {} second(s)...".format(s))
                time.sleep(s)

                if scale.collapsed():
                    game.current_player().destroyer = True
                    game.current_player().out_of_game = True
                    break
                else:
                    print ("success!")
                    game.moves += 1
                    clear_screen()

            if game.round_complete():
                game.end_round()
                #sound.end_of_round()
                #print (game.scoreboard())
                #input("Press enter to begin the next round") + "\n"
                print ("next player: {name}".format(name=game.next_player_name()))
              
            game.move_to_next_player()
            clear_screen()

        scale.stop()

        game.end_game()
        clear_screen()
        print ("GAME OVER\n")
        print (game.scoreboard())
        game.graph()
       
        while True: 
            answer = input("Would you like to play again? y/n: ")
            if answer in ['n','N','no','No','y','Y','yes','Yes']:
                break
            else:
               print ("{} is not an option: Please try again.".format(answer))

        if answer in ['n','N','no','No']: 
            break
         
         
        #print json.dumps(game.data, indent=4)

if __name__ == "__main__":
     main()

