import time 
from machine import Pin

led = Pin(2, Pin.OUT)
timesleep = .5

print('Hello World!')

while True:
  led.value(1)
  time.sleep(timesleep)
  led.value(0)
  time.sleep(timesleep)



