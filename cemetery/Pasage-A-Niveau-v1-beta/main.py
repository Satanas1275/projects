from machine import *
import network
import utime

ESP32_IP = '192.168.1.10'

station = None
accessPoint = None

# LED sur p2
p2 = Pin(2, Pin.OUT)
# Capteur ultrasonique (TRIG = p2, ECHO = p4)
trig = Pin(2, Pin.OUT)
echo = Pin(4, Pin.IN)
# Servomoteur sur p5
servo = PWM(Pin(5), freq=50, duty=26)

def connect_station(ssid='', password='', ip='', mask='', gateway='', dhcp_hostname=''):
    global station
    station = network.WLAN(network.STA_IF)
    if station.isconnected() and station.config('essid') == ssid:
        print("Already connected on ssid: '%s'" % ssid)
        return
    elif station.isconnected():
        disconnect_station()

    print("\nTrying to connect to '%s' ..." % ssid)
    if ip:
        gateway = gateway or ip.rsplit('.', 1)[0] + '.1'
        mask = mask or '255.255.255.0'
        station.ifconfig([ip, mask, gateway, gateway])
    if not station.active():
        station.active(True)
    if dhcp_hostname:
        station.config(dhcp_hostname=dhcp_hostname)
    station.connect(ssid, password)
    while not station.isconnected():
        pass
    print("Station connected!")

def disconnect_station():
    if station and station.isconnected():
        ssid = station.config('essid')
        station.disconnect()
        for _ in range(100):
            if not station.isconnected():
                break
            utime.sleep(0.1)
        if not station.isconnected():
            station.active(False)
            print("Disconnected from '%s'\n" % ssid)
        else:
            print("Disconnection from '%s' failed.\n" % ssid)
    else:
        print("Station already disconnected.\n")

def hcsr04_getUltrasonicData(trig, echo, data='distance', timeout_us=30000):
    trig.off()
    utime.sleep_us(2)
    trig.on()
    utime.sleep_us(10)
    trig.off()
    duration = time_pulse_us(echo, 1, timeout_us) / 1e6  # en secondes
    if duration > 0:
        if data == 'distance':
            return 343 * duration / 2 * 100  # Distance en cm
        elif data == 'duration':
            return duration
    return -1  # Erreur de mesure

def setServoAngle(pin, angle):
    if 0 <= angle <= 180:
        duty_cycle = int(0.025 * 1023 + (angle * 0.1 * 1023) / 180)
        pin.duty(duty_cycle)
    else:
        raise ValueError("Angle doit être compris entre 0 et 180 degrés")

# Connexion au réseau
connect_station(ssid='NEATGEAR23', password='bluemesa488', ip=ESP32_IP)

# Initialisation LED
p2.off()
utime.sleep(1)
p2.on()

# Boucle principale
while True:
    distance = hcsr04_getUltrasonicData(trig, echo, data='distance')
    if distance != -1 and distance <= 10:
        setServoAngle(servo, 90)
        utime.sleep(1)
        setServoAngle(servo, 0)
    utime.sleep_ms(100)
