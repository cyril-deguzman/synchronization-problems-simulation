import threading 

lock = threading.Semaphore()
lock._value = 2
if lock.acquire():
  print(lock._value)
else:
  print('blocked')