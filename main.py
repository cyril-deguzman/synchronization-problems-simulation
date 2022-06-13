import threading
import time
import random as rand

class Model(threading.Thread):
  def __init__(self, color, id):
    super().__init__()
    self.color = color
    self.id = id
    self.hasDressed = False

  def run(self):
    global status

    # randomized time to arrive
    time.sleep(rand.randint(1, 3))

    while not self.hasDressed:
      slots.acquire()

      with status_lock:
        if status == 'Empty':
          status = self.color
          isAllowed = True
          print(status, 'only')
        elif status == self.color:
          isAllowed = True
        else:
          isAllowed = False
          slots.release()
      
      if isAllowed:
        self.fit()

  def fit(self):
    global status
    global limit
    global finished
    global gctr 
    global bctr 

    print(f'native_id: {self.native_id} id: {self.id} color: {self.color} has entered.')

    # randomized time to fit
    time.sleep(rand.randint(1, 3))
    self.hasDressed = True

    with status_lock:
      with finished_lock:
        finished += 1
        
        if self.color == 'Green':
          gctr -= 1
        else:
          bctr -= 1
        
        if finished == limit and bctr != 0 and gctr != 0:
          status = 'Green' if self.color == 'Blue' else 'Blue'
          print('Empty fitting room')
          print(status, 'only')
          self.replenish()
          finished = 0

        elif gctr == 0 and bctr == 0:
          print('Empty fitting room')

        elif self.color == 'Green' and gctr == 0:
          status = 'Blue'
          print('Empty fitting room')
          print(status, 'only')
          self.replenish()
          finished = 0

        elif self.color == 'Blue' and bctr == 0:
          status = 'Green'
          print('Empty fitting room')
          print(status, 'only')
          self.replenish()
          finished = 0

        elif self.color == 'Green' and gctr != 0 and bctr == 0 and finished == limit:
          self.replenish()
          print(status, 'only')
          finished = 0
          
        elif self.color == 'Blue' and bctr != 0 and gctr == 0 and finished == limit:
          self.replenish()
          print(status, 'only')
          finished = 0

  def replenish(self):
    global finished     
    for i in range(finished):
      slots.release()

def main():
  # init global variables
  global slots
  global limit
  global finished 
  global status
  global bctr
  global gctr

  global status_lock
  global finished_lock

  # init room
  limit = int(input('input slots: '))
  slots = threading.Semaphore(limit)
  status_lock = threading.Semaphore()
  finished_lock = threading.Semaphore()
  status = 'Empty'
  finished = 0

  # init models
  blue = [Model('Blue', i) for i in range(int(input('input blue threads: ')))]
  green = [Model('Green', i + len(blue)) for i in range(int(input('input green threads: ')))]
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