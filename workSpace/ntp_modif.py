import time
import network
import ntptime

wifi_ssid = 'vivo Y21s'
wifi_password = 'Muhammad7#'
ntp_timezone = [
  {'zona': 'WIB', 'timezone': 7},
  {'zona': 'WITA', 'timezone': 8},
  {'zona': 'WIT', 'timezone': 9}
]

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
#print('Waktu sebelum sinkronasi: %s' % str(time.localtime()))

#ntptime.settime()
#print('Waktu setelah sinkronasi: %s' % str(time.localtime()))

#waktu_standar = time.time()
#waktu_lokal = time.localtime(waktu_standar + ntp_timezone * (60 * 60))
#print('Waktu lokal: %s' % str(waktu_lokal))

while True:
  for item in ntp_timezone:
    tick = time.time() + item['timezone'] * (60 * 60)
    menit, detik = divmod(tick, 60)
    jam, menit = divmod(menit, 60)
    jam = jam % 24
    print('Waktu di zona %s adalah %s:%s:%s' % (item['zona'], jam, menit, detik))
  
  time.sleep(1)
