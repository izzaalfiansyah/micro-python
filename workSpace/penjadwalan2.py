import time
import network
import ntptime
from machine import Pin

wifi_ssid = 'vivo Y21s'
wifi_password = 'Muhammad7#'
ntp_timezone = 7

jamHidup, menitHidup = 18, 20
jamMati, menitMati = 18, 21

led = Pin(2, Pin.OUT)

def connect_to_wifi(wlan, ssid, password):
  if not wlan.isconnected():
    print('Menghubungkan ke jaringan')
    wlan.connect(ssid, password)
    while not wlan.isconnected():
      pass
      
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

connect_to_wifi(wlan, wifi_ssid, wifi_password)

print('Ready')
print('Waktu sebelum sinkronisasi : %s' % str(time.localtime()))

ntptime.settime()
print('Waktu setelah sinkronisasi : %s' % str(time.localtime()))

waktuStandar = time.time()
waktuLokal = time.localtime(waktuStandar + ntp_timezone * 60 * 60)
print('Waktu lokal                : %s' % str(waktuLokal))

statusHidup = False
tickHidup = 0
tickMati = 0
tick = 0

def updateWaktu():
  global tickHidup, tickMati
  tick = time.time() + ntp_timezone * 60 * 60
  menit, detik = divmod(tick, 60)
  jam, menit = divmod(menit, 60)
  hari, jam = divmod(jam, 24)
  
  # 86400 = 60 detik * 60 menit * 24 jam, 3600 = 60 * 60
  tickHidup = (hari * 86400) + (jamHidup * 3600) + (menitHidup * 60)
  if tick > tickHidup:
    tickHidup = ((hari + 1) * 86400) + (jamHidup * 3600) + (menitHidup * 60)
    
  tickMati = (hari * 86400) + (jamMati * 3600) + (menitMati* 60)
  if tick > tickMati:
    tickMati = ((hari + 1) * 86400) + (jamMati * 3600) + (menitMati * 60)
    
def updateLED():
  global statusHidup, led
  if statusHidup:
    led.value(0)
    print('LED hidup')
  else:
    led.value(1)
    print('LED mati')
  
updateLED()
updateWaktu()

tickLama = 0
while True:
  tick = time.time() + ntp_timezone * 60 * 60
  
  if statusHidup:
    sisaDetikMati = tickMati - tick
    if sisaDetikMati <= 0:
      statusHidup = False
      updateWaktu()
      updateLED()
    else:
      if tick > tickLama:
        tickLama = tick
        menit, detik = divmod(sisaDetikMati, 60)
        jam, menit = divmod(menit, 60)
        jam = jam % 24
        print('OFF dalam %s : %s : %s' % (jam, menit, detik))
  else:
    sisaDetikHidup = tickHidup - tick
    if sisaDetikHidup <= 0:
      statusHidup = True
      updateWaktu()
      updateLED()
    else:
      if tick > tickLama:
        tickLama = tick
        menit, detik = divmod(sisaDetikHidup, 60)
        jam, menit = divmod(menit, 60)
        jam = jam % 24
        print('ON dalam %s : %s : %s' % (jam, menit, detik))







