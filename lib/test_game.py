import unittest
from .game import Game
from .config import BONUS_SECONDS as bs
import json

class TestGame(unittest.TestCase):

    @classmethod
    def setuUpClass(cls):
        print ('setUpClass')

    @classmethod
    def tearDownClass(cls):
        print ('tearDownClass')
   
    def setUp(self):
        print ('setUp')
        #setup games with different number of players
        self.game_2 = Game.two_player()
        self.game_3 = Game.three_player()
        self.game_4 = Game.four_player()
        self.game_4.data = {
                     1:[
                        {'time_remaining': 6, 'turn_time': 4, 'out_of_game': False,"name":'Player1',"turns":1,"player_id":0},
                        {'time_remaining': 9, 'turn_time': 3, 'out_of_game': False,"name":'Player2',"turns":1,"player_id":1}, 
                        {'time_remaining': 8, 'turn_time': 2, 'out_of_game': False,"name":'Player3',"turns":1,"player_id":2}, 
                        {'time_remaining': 7, 'turn_time': 1, 'out_of_game': False,"name":'Player4',"turns":1,"player_id":3}],
                     2:[
                        {'time_remaining': 8, 'turn_time': 2, 'out_of_game': False,"name":'Player1',"turns":2,"player_id":0},
                        {'time_remaining': 7, 'turn_time': 1, 'out_of_game': False,"name":'Player2',"turns":2,"player_id":1}, 
                        {'time_remaining': 6, 'turn_time': 3, 'out_of_game': False,"name":'Player3',"turns":2,"player_id":2}, 
                        {'time_remaining': 6, 'turn_time': 4, 'out_of_game': True,"name":'Player4',"turns":2,"player_id":3}]
                       }

    def tearDown(self):
        print ('tearDown')
   
    def test_create_player_objects(self):
        players = self.game_3.player_objects
        print (players)
        self.assertEqual(players[0].player_id,0)
        self.assertEqual(players[1].player_id,1)
        self.assertEqual(players[2].player_id,2)

    def test_current_player(self):
        self.assertEqual(self.game_3.current_player().player_id,0)

    def test_get_next_highest_integer_basic(self):
       self.assertEqual(self.game_4._next_highest_integer([1,2,3,4],3),4)

    def test_get_next_highest_integer_missing_value(self):
       self.assertEqual(self.game_4._next_highest_integer([1,2,4,6,7],5),6)

    def test_get_next_highest_integer_out_of_range(self):
       self.assertEqual(self.game_4._next_highest_integer([1,2,4],6),1)

    def test_get_next_highest_integer_first_element(self):
       self.assertEqual(self.game_4._next_highest_integer([1,2,4],1),2)

    def test_get_next_highest_integer_last_element(self):
       self.assertEqual(self.game_4._next_highest_integer([1,4,5],5),1)

    def test_next_player_index_basic(self):
        self.assertEqual(self.game_4._next_player_index(),1)
  
    def test_next_player_index_two_players_out(self):
        self.game_4.player_objects[1].out_of_game = True
        self.game_4.player_objects[2].out_of_game = True
        self.assertEqual(self.game_4._next_player_index(),3)

    def test_move_to_next_player_basic(self):
        self.game_4.move_to_next_player()
        self.assertEqual(self.game_4.player_index,1)

    def test_next_player_name(self):
        self.assertEqual(self.game_4.next_player_name(),'Player2')

    def test_round_complete(self):
        self.game_4.move_to_next_player() # move to player 2
        self.game_4.move_to_next_player() # move to player 3
        self.game_4.move_to_next_player() # move to player 4
        self.assertTrue(self.game_4.round_complete())

    def test_round_complete_players_eliminated(self):
        self.game_4.player_objects[0].out_of_game = True
        self.game_4.player_objects[3].out_of_game = True
        self.game_4.move_to_next_player() # move to player 2
        self.game_4.move_to_next_player() # move to player 3
        self.assertTrue(self.game_4.round_complete())

    def test_finalize_last_round_of_game(self):
        self.game_4.round_index = 2
        self.game_4.player_objects[0].out_of_game = True
        self.game_4.finalize_last_round_of_game()
        self.assertTrue(self.game_4.data[self.game_4.round_index][0]['out_of_game'])

    def test_str_round(self):
        r  = "\n ROUND 0\n"
        self.assertEqual(self.game_4._str_round(),r)

    def test_str_moves(self):
        pass

    def test_player_data_by_round_time_remaining(self):
        result =   {
                      'Player1':[6,8],
                      'Player2':[9,7],
                      'Player3':[8,6],
                      'Player4':[7,6]
        }
        self.assertEqual(self.game_4._player_data_by_round('time_remaining'),result)
 
    def test_graph(self):
        for k,v in self.game_4.player_objects.items():
            v.fastest_move_count = v.player_id

        self.game_4.graph()        

if __name__ == "__main__":
    unittest.main()
