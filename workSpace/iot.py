import BlynkLib
import network
import machine
from machine import Pin, ADC
import time

led = Pin(2, Pin.OUT)

WIFI_SSID = 'vivo Y21s'
WIFI_PASS = 'Muhammad7#'

BLYNK_TEMPLATE_ID = "TMPLlPXtTM4m"
BLYNK_DEVICE_NAME = "Quickstart Template"
BLYNK_AUTH_TOKEN = "Ce7AY7YJyRBc4cz0f_cWrfwwFW_B_KnM"

pot = ADC(0)
pot_old = 0
pot_now = 0
pot_lock = 0
pot_time = 0
pot_value_old = 0
pot_value = False
pot_next_check = 300

def tombolSentuh():
  global pot, pot_old, pot_now, pot_lock, pot_time, pot_value_old, pot_value, pot_next_check
  now = time.ticks_ms()
  elapsed = int(now - pot_time)
  
  if elapsed > pot_next_check:
    pot_value = 0
    pot_old = pot_now
    
    for x in range(1, 5):
      pot_now = pot.read()
      new_value = False
      if abs(pot_now - pot_old) > 3:
        pot_value = 1
        break
      pot_old = pot_now
      time.sleep(0.01)
    
    pot_time = time.ticks_ms()
    
    if pot_value:
      pot_next_check = 500
    else:
      pot_next_check = 10
      
  return pot_value
  
gc.collect()

wifi = network.WLAN(network.STA_IF)

if not wifi.isconnected():
  print('Connecting to wifi...')
  wifi.active(True)
  wifi.connect(WIFI_SSID, WIFI_PASS)
  
  while not wifi.isconnected():
    pass
  
print('IP :', wifi.ifconfig()[0])

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

@blynk.on('connected')
def blynk_connected(ping):
  print('Blynk ready. Ping', ping, 'ms')
  print('Updating values from the server...')
  blynk.sync_virtual(0)
  blynk.sync_virtual(1)
  blynk.sync_virtual(2)
  
@blynk.on('disconnected')
def blynk_disconnected():
  print('Blynk disconnected')

@blynk.on('V0')
def v0_write_handler(values):
  value = values[0]
  print('Nilai tombol : %s' % value)
  if value == '1':
    led.value(0)
    print('LED menyala')
  else: 
    led.value(1)
    print('LED mati')
def v0_read_handler():
  blynk.virtual_write(0, led.value())
  
@blynk.on('V1')
def v1_write_handler(values):
  value = values[0]
  print('Tombol sentuh : %s' % value)
  pot_value = value
def v1_read_handler():
  if pot_value:
    blynk.virtual_write(1, 1)
  else:
    blynk.virtual_write(1, 0)

@blynk.on('V2')
def v2_write_handler(values):
  value = values[0]
  print('Uptime : %s' % value)
def v2_read_handler():
  blynk.virtual_write(2, time.time())
  
def runLoop():
  global pot_value_old, pot_value
  pot_value = tombolSentuh()
  firstBoot = time.time()
  oldTick = firstBoot
  
  while True:
    blynk.run()
    if time.time() > oldTick:
      blynk.virtual_write(2, time.time() - firstBoot)
      oldTick = time.time()
    
    pot_value = tombolSentuh()
    if pot_value_old != pot_value:
      pot_value_old = pot_value
      print('Status tombol : %s' % pot_value)
      if pot_value:
        blynk.virtual_write(1, 1)
      else:
        blynk.virtual_write(1, 0)
    
    machine.idle()
    gc.collect()
    
gc.collect()
runLoop()
  
  


