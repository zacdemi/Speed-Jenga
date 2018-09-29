import time
from .sounds import Sounds

class Timer():
    """ standard timer """    

    def __init__(self, seconds):
         self._seconds = seconds
         self.active = False
         self.warning_on = True
         self.warning_range = [x + .99 for x in range(10)]
         self.sound = Sounds()
        
    def start(self):
        if not self.active:
            self.start_time = time.time()
            self.active = True

    def pause(self):
        if self.active:
            self._seconds = max(0,self._seconds - self._elapsed())
        self.active = False

    def add_seconds(self,seconds):
        self._seconds += seconds
    
    def get_seconds(self):
        if self.active:
            self._seconds = max(0,self._seconds - self._elapsed())
            self.check_warning(self._seconds)

        return round(self._seconds,2)

    def _elapsed(self):
        elapsed = time.time() - self.start_time
        self.start_time = time.time()
        return elapsed

    def check_warning(self,seconds):
        if self.warning_on and round(seconds,2) in self.warning_range:
            self.sound.warning()
 
def main():
    pass     

if __name__ == "__main__":
    main()
