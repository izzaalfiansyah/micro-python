import time
from machine import Pin

led = Pin(2, Pin.OUT)
liveStatus = False
lastTick = 0

def updateLED():
  global liveStatus, lastTick
  if liveStatus:
    led.value(0)
    print('LED hidup')
  else:
    led.value(1)
    print('LED mati')

updateLED()

while True:
  tick = time.time()
  delta = tick - lastTick
  if delta > 2:
    liveStatus = not liveStatus
    updateLED()
    lastTick = tick

