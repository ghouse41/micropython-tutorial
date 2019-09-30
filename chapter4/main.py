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
        print('Connecting to Wifi...')
        sta_if.active(True)
        sta_if.connect(config.WIFI_SSID,config.WIFI_PASSWORD)

        while not sta_if.isconnected():
            time.sleep(1)
        print('Network config:',sta_if.ifconfig())

def call_webhook():
    print('Invoking webhook...')
    response = urequests.post(config.WEBHOOK_URL,
                              json={'value1': config.BUTTON_ID})
    if response is not None and response.status_code < 400:
        print('Webhook invoked')
        print('status code:',response.status_code)
    else:
        print('webhook failed')
        raise RuntimeError('Webhook failed')

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

def run():
    try:
        if machine.reset_cause() == machine.DEEPSLEEP_RESET:
            connect_wifi()
            call_webhook()
    except Exception as exc:
        sys.print_exception(exc)
        show_error()
    machine.deepsleep()
run()