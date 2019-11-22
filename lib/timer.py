import time

class Timer():
    """ standard timer """    

    def __init__(self, seconds):
         self._seconds = seconds
         self.active = False
        
    def start(self):
        if not self.active:
            self.start_time = time.time()
            self.active = True

    def pause(self):
        if self.active:
            self._seconds = self._seconds - self._elapsed()
        self.active = False

    def add_seconds(self,seconds):
        self._seconds += seconds
    
    def get_seconds(self):
        if self.active:
            self._seconds = self._seconds - self._elapsed()
        return round(self._seconds,2)

    def _elapsed(self):
        elapsed = time.time() - self.start_time
        self.start_time = time.time()
        return elapsed
 
def main():
    pass     

if __name__ == "__main__":
    main()
