
import unittest
import time as t
from .player import Player
from .config import BONUS_SECONDS as bs

class TestPlayerTimer(unittest.TestCase):

    @classmethod
    def setuUpClass(cls):
        print ('setUpClass')

    @classmethod
    def tearDownClass(cls):
        print ('tearDownClass')
   
    def setUp(self):
        print ('setup')
        #setup games with different number of players
        self.player1 = Player(0,'Player1',.2)

    def tearDown(self):
        print ('tearDown')

    def test_player_status_is_active(self):
        self.player1.timer.start()
        t.sleep(.05)
        self.assertEqual("Player1",self.player1.status()[:7])
     
    def test_player_status_is_paused(self):
        self.player1.timer.start()
        self.player1.timer.pause() 
        self.assertEqual("Player1's clock is paused",self.player1.status()[:-5])

    def test_player_status_is_out_of_time(self):
        self.player1.timer.start()
        t.sleep(.2)
        self.assertEqual("Player1 is out of the game",self.player1.status())

    def test_out_of_time(self):
        self.assertFalse(self.player1.out_of_time())

    def test_out_of_time_after_sleep(self):
        self.player1.timer.start()
        t.sleep(.2) 
        self.assertTrue(self.player1.out_of_time())
 
    def test_start_turn(self):
        self.player1.start_turn()
        self.assertTrue(self.player1.timer.active)

    def test_pause_turn(self):
        self.player1.start_turn()
        self.player1.pause_turn()
        self.assertFalse(self.player1.timer.active)

    def test_end_turn_of_active_player(self):
        self.player1.start_turn()
        self.player1.end_turn()
        self.assertEqual(self.player1.turn_index,1)

    def test_turn_time_before_first_turn(self):
        self.assertEqual(self.player1.turn_time(),None)

if __name__ == '__main__':
    unittest.main()

