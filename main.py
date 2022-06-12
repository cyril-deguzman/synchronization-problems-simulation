import threading
import time
import random as rand

class Model(threading.Thread):
  def __init__(self, color, id):
    super().__init__()
    self.id = id
    self.color = color
    self.hasDressed = 0

  def run(self):
    # arrival
    time.sleep(rand.randint(1, 21))

    while self.hasDressed is 0:
      # CRITICAL SECTION
      if lock.acquire(blocking=False):
        global status 
        status = self.color
        self.hasDressed = 1
      # END OF CRITICAL SECTION
      else:
        event.wait()
        self.fit()

  def fit(self):
    with slots:
      global entered
      # CRITICAL SECTION
      if self.color is status:
        entered += 1
        print(f'Person [{self.id}] with color [{self.color}] has entered the fitting room.')
        time.sleep(rand.randint(1, 21))
      # END OF CRITICAL SECTION

def main():
  # init global variables
  global event
  global status
  global lock
  global slots
  global entered
  global swap

  # init room
  swap = int(input())
  slots = threading.Semaphore(swap)
  event = threading.Event()
  lock = threading.Semaphore()
  status = 'empty'
  entered = 0
  
  # init models
  blue = [Model('blue', i) for i in range(int(input()))]
  green = [Model('green', i + len(blue)) for i in range(int(input()))]
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