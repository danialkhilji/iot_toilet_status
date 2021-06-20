import network
wifi = network.WLAN(network.STA_IF) # create station interface
wifi.active(True)       # activate the interface
wifi.scan()             # scan for access points
print(wifi.isconnected())      # check if the station is connected to an AP
wifi.connect('wifi-name', 'wifi-password') # connecting to Wi-Fi
wifi.config('mac')      # get the interface's MAC address
wifi.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses
print('Connection complete')

#To connect with MQTTClient
from umqtt.simple import MQTTClient
import time, urandom
from time import sleep
from machine import Pin, ADC, I2C, PWM #to configure pins of sensors

server = 'mqtt.thingspeak.com'
topic_mqtt = 'el-4012_toilet_status'
cnct = MQTTClient(topic_mqtt, server, ssl=True)
cnct.connect()

#Thingspeak API Write key and channel ID to connect with
chnl_id = ""
api_key = ""
topic_thingspeak = "channels/" + chnl_id + "/publish/" + api_key


import ssd1306 #lcd library
#lcd pins setup
i2c = I2C(-1, scl=Pin(22), sda=Pin(21), freq=100000)
lcd = ssd1306.SSD1306_I2C(128, 64, i2c)
#IR sensor: 0 - White,  4095 - Black
#IR sensor pins setup
analog_signal = ADC(Pin(34))
analog_signal.atten(ADC.ATTN_11DB) #ADC.ATTN_11DB = 0-3.3v range

while True:
        IR_value = analog_signal.read()
        print("IR value: ", IR_value)
        lcd.fill(0)
        lcd.text("IR sensor value:", 0, 20)
        lcd.text(str(IR_value), 40, 40)
        lcd.show()
        time.sleep(1)
        if (IR_value < 2000):
            print("Toilet occupied")
            lcd.fill(0)
            lcd.text("Toilet is", 10, 20)
            lcd.text("occupied!", 10, 40)
            lcd.show()
            time.sleep(1)
        else:
            print("Toilet free")
            lcd.fill(0)
            lcd.text("Toilet is", 10, 20)
            lcd.text("free!", 10, 40)
            lcd.show()
            time.sleep(1)
        
        print('Publishing on ThingSpeak')
        data = "field1="+str(IR_value)
        cnct.publish(topic_thingspeak, data)
        sleep(1) #program delay
        
        
        