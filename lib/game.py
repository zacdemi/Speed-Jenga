from .player import Player
from .config import TOTAL_GAME_SECONDS, BONUS_SECONDS
from matplotlib import pyplot as plt
import time
import os

class Game(object):
  
    def __init__(self,player_names):

        """
        player_names -> list
        Initiate game variables, dict of player objects, and GameLogger.
        """
        self.player_names = player_names
        self.player_index = 0
        self.round_index = 0
        self.moves = 0
        self.data = {}
 
        self._create_player_objects()
        self._initialize_data()

    def _create_player_objects(self):
        """
        Create a hash table of player objects by player_id

        {0:<object>,1:<object>,2:<object>,3:<object>}
        """
        self.player_objects = {}
        player_seconds = TOTAL_GAME_SECONDS / len(self.player_names)

        for name in self.player_names:
           player_id = self.player_names.index(name)
           self.player_objects[player_id] = Player(player_id, name, player_seconds)
 
        return self.player_objects

    def current_player(self):
        """ return player object of current player index """
        return self.player_objects[self.player_index]

    def move_to_next_player(self):
        """ update player index to next active player """
        self.player_index = self._next_player_index()

    def next_player_name(self):
        """ return the name of the next player """
        return self.player_objects[self._next_player_index()].name

    def _active_player_ids(self):
        """ return a list of active player ids """
        return [k for k,v in self.player_objects.items() if not v.out_of_game]

    def one_player_remains(self):
        """ return True if one player remains in the game """
        return len(self._active_player_ids()) == 1 

    def _next_player_index(self):
        """ return the value of the next player index"""
        return self._next_highest_integer(self._active_player_ids(), self.player_index)

    def round_complete(self):
        """ return True if the player index is the last player in a round """
        return self._next_player_index() < self.player_index

    def award_fastest_move(self):
        """ increment player fastest move count """
        player_id, = self._fastest_turn()
        self.player_objects[player_id].fastest_move_count += 1

    def _fastest_turn(self):
        """ 
        return (player_id, turn_time, name) for player with fastest turn
        """
        rnd = self.data[self.round_index]
        turn = [ 
                   (p['player_id'], p['turn_time'], p['name']) 
                   for p in rnd 
                   if not p['out_of_game']
        ]
        turn = min(turn, key=lambda x: x[1])
        return turn 

    def save_round(self):
        """ add player data to data.round_index """
        rnd = []
  
        for k,v in self.player_objects.items():
            player = {'time_remaining': v.timer.get_seconds(),
                      'turn_time': v.turn_time(),
                      'out_of_game': v.out_of_game,
                      'name': v.name,
                      'player_id': v.player_id,
                      'turns': v.turn_index}

            rnd.append(player)
        self.data[self.round_index] = rnd

    def _initialize_data(self):
        """ save round zero to game data """
        self.save_round()

    def finalize_last_round_of_game(self):
        """ update last round to reflect the final player out_of_game status """
        for player in self.data[self.round_index]:
            player['out_of_game'] = self.player_objects[player['player_id']].out_of_game

    def stability_seconds(self):
        """ return the number of seconds the tower must be stable before next turn """
        if self.moves < 15:
            return 1
        if 15 <= self.moves <= 29:
            return 2
        else:
            return 3

    def end_round(self):
        self.round_index += 1
        self.save_round()
        self.award_fastest_move()

    def end_game(self):
        if self.round_complete():
            self.end_round()
        else:
            self.finalize_last_round_of_game()

    def scoreboard(self): #GUI
        """ combine _str elements into scoreboard """
        return self._str_round() + self._str_standings() + self._str_fastest_move() + self._str_moves()

    def _str_round(self): #GUI
        """ return a string representation of the current round
        'ROUND 3'
        """
        return  "\n ROUND {}\n".format(self.round_index)

    def _str_standings(self): #GUI
        """
        Return a string representation of the standings
        '  Player3  | 7  | False
           Player1  | 6  | False
           Player2  | 2  | False '
        """

        #sort players in round
        rnd = self.data[self.round_index]
        rnd.sort(key=lambda x: x['time_remaining'],reverse=True)
        rnd.sort(key=lambda x: x['out_of_game'])
        rnd.sort(key=lambda x: x['turns'],reverse=True)

        header = "\n {: <10} | {: <10} | {}\n".format("name", "time", "out of game")
        standings = header

        for p in rnd:
            standings += "\n {: <10} | {: <10} | {}".format(p['name'], p['time_remaining'], p['out_of_game'])
  
        return standings + "\n"

    def _str_fastest_move(self): #GUI
        """ 
        display player with the fastest move:
        ' fastest move: Zac | 1.34'
        """
        _,turn_time,name = self._fastest_turn()

        fastest =  "\n fastest move: {} | {}\n".format(name,turn_time)
        if self.round_index == 0:
            return ""
        else:
            return fastest  

    def _str_moves(self):
        """ 
        string of count of moves
        ' total moves: 12'
        """
        return " total moves: {} \n".format(self.moves)
 
    def _player_data_by_round(self, field):
        """ 
        return a dict of players and their times
       
        {'Player1':[30,25,24,23,20,15,10,5,0],
        'Player2':[30,25,24,23,20,15,10,5,0]}
        """
        result = {}
        for p in range(len(self.player_names)):
            data = []
            for rnd, players in self.data.items():
                for player in players:
                    if player['player_id'] == p:
                        data.append(player[field])
            result[self.player_names[p]] = data
        return result 

    def _player_fastest_move_count(self):
        """ 
        return a dict of players and their fastest move count 
        
        {'Player1':4,'Player2':5,'Player3':7}
        """
        players = {
            v.name:v.fastest_move_count
            for k,v in self.player_objects.items()
        } 
        return players 

    def graph(self):
        """ 
        graph subplot of player times and fastest move count
        """

        x = self.data.keys() #rounds
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

        for name,times in self._player_data_by_round('time_remaining').items():
            ax1.plot(x, times, label=name)
        ax1.set_title('Time Remaining by Round', fontsize=12)
        ax1.set_ylabel('Time Remaining')
        ax1.legend()
        
        for name,times in self._player_data_by_round('turn_time').items():
            ax2.scatter(x, times, label=name)
        ax2.set_title('Fastest Moves by Round', fontsize=12)
        ax2.set_ylabel('Seconds')
        ax2.legend()

        data = self._player_fastest_move_count()
        names = list(data.keys())
        count_of_fastest_moves = list(data.values())

       #ax3.bar(names,count_of_fastest_moves)
       #ax3.set_title('Count of Fastest Moves')
       #ax3.set_ylabel('Fastest Moves')

        fig.suptitle('Game Stats')
        fig.tight_layout()
        plt.show()

    @classmethod
    def two_player(cls):
        return cls(['Player1', 'Player2'])
 
    @classmethod
    def three_player(cls):
        return cls(['Player1', 'Player2', 'Player3'])
 
    @classmethod
    def four_player(cls):
        return cls(['Player1', 'Player2', 'Player3', 'Player4'])
 
    @staticmethod
    def _next_highest_integer(list_of_integers,n):
        """
        Given an array and integer n, return next greatest integer.
        if n is >= last integer in array, return first integer.
 
        ([1,2,4,6],5) -> 6
        ([1,2,4,6],6) -> 1
        ([1,2,4,6],2) -> 4
 
        """
        list_of_integers.sort()
     
        for i in range(0,len(list_of_integers)-1,1):
            if list_of_integers[i] <= n < list_of_integers[i+1]:
                return list_of_integers[i+1]
        return list_of_integers[0]

if __name__ == '__main__':
    pass

    
