import BlynkLib
import network
import time
from machine import Pin

BLYNK_AUTH = "Bsq_nrdF0x7ccQ6QdntOinTCMHWw79j3"
blynk = BlynkLib.Blynk(BLYNK_AUTH, insecure=True)
led = Pin(2, Pin.OUT)
led.value(1)

def connectWifi():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  
  ssid = 'vivo Y21s'
  password = 'Muhammad7#'
  
  if not wlan.isconnected():
    print('Menghubungkan ke jaringan...')
    wlan.connect(ssid, password)
    
    while not wlan.isconnected():
      print('Gagal terhubung. Mencoba menghubungkan kembali...')
      time.sleep(1)
  
  print('IP address : %s' % wlan.ifconfig()[0])

connectWifi()

@blynk.on('connected')
def blynk_connected():
  blynk.sync_virtual(0, 1)
  print('Blynk berhasil terhubung')

@blynk.on('V1')
def blynk_v2_write(values):
  value = int(values[0][:2])
  if value > 0:
    blynk.set_property(0, 'color', 'green')
    led.value(0)
    print('Toko dibuka')
  else:
    blynk.set_property(0, 'color', 'red')
    led.value(1)
    print('Toko ditutup')

while True:
  blynk.run()
  blynk.virtual_write(0, 0)
