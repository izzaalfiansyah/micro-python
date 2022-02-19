import network

def connectToWifi():  
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  
  wifi_ssid = 'V2026 14'
  wifi_password = '123456789'
  
  if not wlan.isconnected():
    print('Menghubungkan jaringan...')
    wlan.connect(wifi_ssid, wifi_password)
    while not wlan.isconnected():
      pass
      

connectToWifi()
