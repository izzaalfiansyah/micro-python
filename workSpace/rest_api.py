import urequests as req
import time
import network
import ujson as json

wifi = {
  'ssid': 'vivo Y21s', 
  'password': 'Muhammad7#'
}

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def connect_to_wifi(wlan):
  if not wlan.isconnected():
    print('Menghubungkan ke jaringan...')
    wlan.connect(wifi['ssid'], wifi['password'])
    while not wlan.isconnected():
      pass

connect_to_wifi(wlan)

def cetakRamalanCuaca(data):
  temperatur = json.loads(data)['dataseries'][0]['temp2m']
  prediksiCuaca = json.loads(data)['dataseries'][0]['prec_type']
  prediksiKonversi = ''
  
  if prediksiCuaca == 'rain':
    prediksiKonversi = 'Hujan'
  elif prediksiCuaca == 'snow':
    prediksiKonversi = 'Bersalju'
  else:
    prediksiKonversi = 'Tidak Hujan'
    
  print('Temperatur     : %s derajat Celcius' % temperatur)
  print('Prediksi Cuaca : %s' % prediksiKonversi)

try:
  f = open('data.json', 'r')
  txt = f.read()
  f.close()
  print('Ramalan cuaca terakhir adalah: ')
  cetakRamalanCuaca(txt)
except OSError:
  print('Data ramalan cuaca tidak ditemukan')
  
print('Meminta data cuaca terkini...')

# Makkah
lon = '21.40303734031222'
lat = '39.77786966600221'

r = req.get('http://www.7timer.info/bin/astro.php?lon=%s&lat=%s&ac=0&unit=metric&output=json&tzshift=0' % (lon, lat))
cetakRamalanCuaca(r.text)

print('Menyimpan data...')
f = open('data.json', 'w')
f.write(r.text)
f.close()
r.close()

print('Selesai')

