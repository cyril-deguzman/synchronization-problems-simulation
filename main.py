import threading
import time
import random as rand

class Model(threading.Thread):
  def __init__(self, color, id, flag, swap_flag):
    super().__init__()
    self.id = id
    self.color = color
    self.hasDressed = False
    self.flag = flag
    self.swap_flag = swap_flag
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
    
    # if first thread to enter an empty room
    slots.acquire()
    if self.first:
      self.flag.set()
    
    # CRITICAL SECTION
    with lock_entered:
      entered += 1
    # END OF CRITICAL SECTION
    
    print(f'Person [{self.id}] with color [{self.color}] has entered the fitting room.')
    time.sleep(rand.randint(1, 6))
    self.hasDressed = True

    # CRITICAL SECTION
    with lock_entered:
      if entered is limit:
        self.flag.clear()
        print('empty fitting room')
        self.swap_flag.set()
        slots._value = limit
    # CRITICAL SECTION

def main():
  # init global variables
  global lock
  global slots
  global limit
  global entered
  global lock_entered

  # init room
  limit = int(input())
  slots = threading.Semaphore(limit)
  lock = threading.Semaphore()
  lock_entered = threading.Semaphore()
  blue_flag = threading.Event()
  green_flag = threading.Event()
  entered = 0
  
  # init models
  blue = [Model('blue', i, blue_flag, green_flag) for i in range(int(input()))]
  green = [Model('green', i + len(blue), green_flag, blue_flag) for i in range(int(input()))]
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