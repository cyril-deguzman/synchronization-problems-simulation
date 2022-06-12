import threading 

lock = threading.Semaphore()
lock.acquire()

global status 
status = 'hello'

if lock.acquire():
  print(status)
else:
  print('blocked')