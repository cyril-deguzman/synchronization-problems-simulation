import threading
import time
import random as rand

class Model(threading.Thread):
  def __init__(self, color, id, flag, swap_flag, wait_flag):
    super().__init__()
    self.id = id
    self.color = color
    self.hasDressed = False
    self.flag = flag
    self.swap_flag = swap_flag
    self.wait_flag = wait_flag
    self.first = False
    
  def run(self):
    # randomized arrival time
    time.sleep(rand.randint(1, 6))
    
    # CRITICAL SECTION FOR FIRST THREAD TO ARRIVE
    if lock.acquire(blocking=False):
      self.first = True
      print(f'{self.color} only')
      self.fit()
    # END OF CRITICAL SECTION

    else:
      while not self.hasDressed:
        self.flag.wait()
        self.fit()
    
  def fit(self):
    global entered
    global exited
    global bctr 
    global gctr 

    # if first thread to enter an empty room
    if slots.acquire(blocking=False):
      if self.first:
        self.flag.set()
      
      # CRITICAL SECTION
      with lock_entered:
        entered += 1
      # END OF CRITICAL SECTION
      
      print(f'Person [{self.id}] with color [{self.color}] has entered the fitting room.')
      time.sleep(rand.randint(1, 6))
      self.hasDressed = True
      
      with lock_exited:
        exited += 1

      # CRITICAL SECTION
      with lock_entered:
        with lock_exited:
          if self.color == 'green':
            gctr -= 1
          else:
            bctr -= 1
          if entered == limit or entered == exited:
            # clear flag and replenish slots
            self.flag.clear()
            print('empty fitting room')
            slots._value = limit
            self.wait_flag.set()
            
            # swap flag or repeat
            if (self.color == 'green' and bctr != 0 
              or self.color == 'blue' and gctr != 0
              or self.color == 'green' and gctr == 0
              or self.color == 'blue' and bctr == 0):
              self.swap_flag.set()
            else:
              self.flag.set()
      # CRITICAL SECTION
    else:
      self.wait_flag.wait()
def main():
  # init global variables
  global lock
  global slots
  global limit
  global entered
  global exited
  global lock_entered
  global lock_exited
  global bctr 
  global gctr

  # init room
  limit = int(input())
  slots = threading.Semaphore(limit)
  lock = threading.Semaphore()
  lock_entered = threading.Semaphore()
  lock_exited = threading.Semaphore()
  blue_flag = threading.Event()
  green_flag = threading.Event()
  wait_flag = threading.Event()
  entered = 0
  exited = 0

  # init models
  blue = [Model('blue', i, blue_flag, green_flag, wait_flag) for i in range(int(input()))]
  green = [Model('green', i + len(blue), green_flag, blue_flag, wait_flag) for i in range(int(input()))]
  models = []
  
  bctr = len(blue)
  gctr = len(green)

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