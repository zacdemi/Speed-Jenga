
import unittest
import time as t
from .timer import Timer

class TestTimer(unittest.TestCase):

    @classmethod
    def setuUpClass(cls):
        print ('setUpClass')

    @classmethod
    def tearDownClass(cls):
        print ('tearDownClass')
   
    def setUp(self):
        print ('setup')
        self.timer1 = Timer(.2)
        self.timer2 = Timer(10)

    def tearDown(self):
        print ('tearDown')

    def test_start_basic(self):
        self.timer1.start()
        t.sleep(.1)
        current_time = self.timer1.get_seconds()
        self.assertTrue(current_time >= .09 and current_time <= .1)

    def test_start_basic_long(self):
        self.timer2.start()
        t.sleep(9)
        current_time = self.timer2.get_seconds()
        self.assertTrue(current_time >= .9 and current_time <= 1)
 
    def test_pause_while_active(self):
        self.timer1.start()
        t.sleep(.1)
        self.timer1.pause()
        t.sleep(.4)
        current_time = self.timer1.get_seconds()
        self.assertTrue(current_time >= .09 and current_time <= .1)
   
    def test_add_while_active(self):
        self.timer1.start()
        self.timer1.add_seconds(.2)
        t.sleep(.3)
        current_time = self.timer1.get_seconds()
        self.assertTrue(current_time >= .09 and current_time <= .1)

    def test_end_timer(self):
        self.timer1.start()
        t.sleep(.2)
        current_time = self.timer1.get_seconds()
        self.assertEqual(current_time,0.00)

    def test_pause_paused_timer(self):
        self.timer1.start()       
        self.timer1.pause()
        self.timer1.pause()
        current_time = self.timer1.get_seconds()
        self.assertTrue(current_time >= .19 and current_time <= .2)

    def test_pause_inactive_timer(self):
        self.timer1.pause()
        self.assertEqual(self.timer1.get_seconds(),.2) 

    def test_get_seconds_repeatedly(self):
        self.timer2.start()
        self.timer2.get_seconds()
        self.timer2.get_seconds()
        t.sleep(3)
        self.timer2.get_seconds()
        self.timer2.get_seconds()
        self.timer2.get_seconds()
        current_time = self.timer2.get_seconds()
        print (current_time, 7)
        self.assertTrue(current_time >= 6 and current_time <= 7)

if __name__ == '__main__':
    unittest.main()

