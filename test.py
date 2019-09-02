import serial
import sys 
import io


sys.stdout.write("Test\n")

# usb_serial = serial.Serial()
# usb_serial.boundrate = 115200
# usb_serial.port='COM0'
# usb_serial.open()

usb_serial = serial.Serial('/dev/ttyUSB0', 38400)
# usb_serial.is_open()
usb_serial.write(b'start\n')
print(usb_serial.is_open)
print(usb_serial.read(5))

print(usb_serial.name)

usb_serial.close()