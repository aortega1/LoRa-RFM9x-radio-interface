# Write your code here :-)
import time
import busio
import digitalio
import board
import analogio
import adafruit_rfm9x
import array
import adafruit_bme280
FEATHER_ID = 0x01
SENSOR_SEND_DELAY = 1
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
RADIO_FREQ_MHZ = 905.5
CS = digitalio.DigitalInOut(board.RFM9X_CS)
RESET = digitalio.DigitalInOut(board.RFM9X_RST)
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.tx_power = 13
bme280_data = bytearray(8)
vbat_voltage = analogio.AnalogIn(board.D9)
def get_voltage(pin):

    volts = (pin.value * 3.3) / 65536 * 2
    if volts >= 4.20:
        volts = 0.00
    return volts
while True:
 #   battery_voltage = get_voltage(vbat_voltage)
 #   if battery_voltage >= 4.20:
 #       battery_voltage = 0.00
 #   else:
 #       batt_float = get_voltage(vbat_voltage)
 #       print(batt_float)
 #       battery_voltage = int(batt_float * 100)
 #       print(" batt voltage: {:.2f}".format(battery_voltage))

#convert to celcius, and then remove outliers
    temp_val = int(bme280.temperature * 100)
    if temp_val >= 10:
        temp_val = 0
    print("\n")
    print("Temperature: %0.1f C" % bme280.temperature)
    humid_val = int(bme280.humidity * 100)
    if humid_val >= 100:
        humid_val = 0
    print("Humidity: %0.1f %%" % bme280.humidity)
    pres_val = int(bme280.pressure * 100)
    print("Pressure: %0.1f hPa" % bme280.pressure)
    batt_level = (str(get_voltage(vbat_voltage) * 1000))
    print(batt_level)
    bme280_data[0] = FEATHER_ID
    bme280_data[1] = (temp_val >> 8) & 0xff
    bme280_data[2] = temp_val & 0xff
    bme280_data[3] = (humid_val >> 8) & 0xff
    bme280_data[4] = humid_val & 0xff
    bme280_data[5] = (pres_val >> 16) & 0xff
    bme280_data[6] = (pres_val >> 8) & 0xff
    bme280_data[7] = pres_val & 0xff
    bme280_data_bytes = bytes(bme280_data)
    print('Sending data...')
    LED.value = True
    rfm9x.send(bme280_data)
    LED.value = False
    rfm9x.send(batt_level)
 #   bv = (battery_voltage >> 8) & 0xff
 #   bv = (battery_voltage)
#    print(bv)
#    LED.value = True

#    rfm9x.send(bv)
 #   print('sent batt level')
 #   LED.value = False
        # Wait to send the packet again
    time.sleep(SENSOR_SEND_DELAY * 60)




