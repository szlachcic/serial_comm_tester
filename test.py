import serial
import sys 
import time
import json
import random
import threading



class USB_serial(serial.Serial):
    
    buf_m = []
    buf_s = []
    buf_o = []

    def __init__(self):
        sys.stdout.write("Test\n")
        self.usb = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
        print("Serial connection: ", self.usb.is_open)
        print("Serial name: ", self.usb.name) 

    def __del__(self):
        self.usb.close()
        print("Serial comunication closed")
      
    def send(self, data):
        self.usb.write(data) #to musi byc string

    def loopRecive(self):
        while 1==1:
            string=b"start"
            USB.send(string)
            data = self.usb.readline()
            print(data.decode('utf-8'))
            first_char =  data[:1].decode('utf-8')

            if first_char=='W' or first_char=='T' or first_char=='F':
                buf_s.extend(data.decode('utf-8'))
            elif first_char=='L' or first_char=='I' or first_char=='D':
                buf_o.extend(data.decode('utf-8'))
            elif first_char=='H' or first_char=='A' or first_char=='J' or first_char=='S' or first_char=='Y':
                buf_m.extend(data.decode('utf-8'))
            else: 
                print('Incorrect comand')
                print(data[:1])


def random_test(group):
    x = random.randint(1,10)
    print(x)
    name = ('tests/test{}_{}.json'.format(group, x))
    print('Test name: {}'.format(name))
    with open(name) as json_file:
        data = json.load(json_file)

    return data 

def motion_test():
    data = random_test(1)
    print(data)

def state_test():
    pass

def output_test():
    pass

if __name__=='__main__':


    USB = USB_serial()
    threading.Thread(USB.loopRecive()).start()

    motion_test()

    threading.Thread(USB.loopRecive()).start()

# print(data["BOUND"])
# y=json.dumps(data)
# print(y)
# USB.usb.write(b"start")
# print(usb_serial.name)

