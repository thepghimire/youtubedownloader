import time

class Timer:
    def __init__(self) -> None:
        self.start_time = time.time() 
    
    def end(self, text="Process"):
        elapsed_time = time.time() - self.start_time
        print(text + " took {0:.2f} seconds.".format(elapsed_time))
        return None
