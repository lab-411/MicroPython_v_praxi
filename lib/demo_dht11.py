from machine import Pin
import lib_dth11 as dht

s = dht.DHT11(Pin('PB5'))

s.temperature()
