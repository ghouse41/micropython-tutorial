import dht
import machine
import network
import sys
import time
import urequests
import config
def connect_wifi():
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to WiFi...')
        sta_if.active(True)
        sta_if.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        while not sta_if.isconnected():
            time.sleep(1)
    print('Network config:', sta_if.ifconfig())
def show_error():
    led = machine.Pin(config.LED_PIN, machine.Pin.OUT)
    led2 = machine.Pin(config.LED2_PIN, machine.Pin.OUT)
    for i in range(3):
        led.on()
        led2.off()
        time.sleep(0.5)
        led.off()
        led2.on()
        time.sleep(0.5)
    led.on()
    led2.on()
def is_debug():
    debug = machine.Pin(config.DEBUG_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    if debug.value() == 0:
        print('Debug mode detected.')
        return True
    return False
def get_temperature_and_humidity():
    dht22 = dht.DHT22(machine.Pin(config.DHT22_PIN))
    dht22.measure()
    temperature = dht22.temperature()
    if config.FAHRENHEIT:
        temperature = temperature * 9 / 5 + 32
    return temperature, dht22.humidity()
def log_data(temperature, humidity):
    print('Invoking log webhook')
    url = config.WEBHOOK_URL.format(temperature=temperature,
                                    humidity=humidity)
    response = urequests.get(url)
    if response.status_code < 400:
        print('Webhook invoked')
    else:
        print('Webhook failed')
        raise RuntimeError('Webhook failed')
def run():
    try:
        if machine.reset_cause() == machine.DEEPSLEEP_RESET:
            connect_wifi()
            temperature, humidity = get_temperature_and_humidity()
            log_data(temperature, humidity)
    except Exception as exc:
        sys.print_exception(exc)
        show_error()
    machine.deepsleep()
