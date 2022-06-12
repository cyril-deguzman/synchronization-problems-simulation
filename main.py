import threading
import time
import random as rand

class Model(threading.Thread):
  def __init__(self, color, id, flag):
    super().__init__()
    self.id = id
    self.color = color
    self.hasDressed = 0
    self.flag = flag

  def run(self):
    # randomized arrival time
    time.sleep(rand.randint(1, 21))
    
    # CRITICAL SECTION FOR FIRST THREAD TO ARRIVE
    if lock.acquire(blocking=False):
      global status 
      status = self.color
      self.hasDressed = 1
      self.flag.set()
    # END OF CRITICAL SECTION
    else:
      while self.hasDressed is 0:
        self.flag.wait()
        self.fit()
    
  def fit(self):
    slots.acquire()
    global entered
    # CRITICAL SECTION
    if self.color is status:
      entered += 1
      print(f'Person [{self.id}] with color [{self.color}] has entered the fitting room.')
      time.sleep(rand.randint(1, 21))
    # END OF CRITICAL SECTION

def main():
  # init global variables
  global status
  global lock
  global slots
  global entered
  global swap

  # init room
  swap = int(input())
  slots = threading.Semaphore(swap)
  lock = threading.Semaphore()
  blue_flag = threading.Event()
  green_flag = threading.Event()
  status = 'empty'
  entered = 0
  
  # init models
  blue = [Model('blue', i, blue_flag) for i in range(int(input()))]
  green = [Model('green', i + len(blue), green_flag) for i in range(int(input()))]
  models = []

  for model in blue:
    model.start()
    models.append(model)

  for model in green:
    model.start()
    models.append(model)
  
  for model in models:
    model.join()

if __name__ == "__main__":
    main()