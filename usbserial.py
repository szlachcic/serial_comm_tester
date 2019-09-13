import serial
import threading
import time




class USB_serial(serial.Serial):
    buf_m = []
    buf_s = []
    buf_o = []


    def __init__(self):
        self.usb = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
        print("Serial connection: ", self.usb.is_open)
        print("Serial name: ", self.usb.name) 
        self.lock = threading.Lock()

    def __del__(self):
        self.usb.close()
        print("Serial comunication closed")
      
    def send(self, data):
        self.lock.acquire()
        self.usb.write(data) 
        self.lock.release()
    
    def loopRecive(self):
        while 1==1:
            # print(threading.currentThread())
            if self.usb.in_waiting != 0:
                self.lock.acquire()
                data = self.usb.readline()
                self.lock.release()
                print(data)
                first_char =  data[:1].decode('utf-8')
                print("check")
                if first_char=='W' or first_char=='T' or first_char=='F':
                    self.buf_s.append(data)
                elif first_char=='L' or first_char=='I' or first_char=='D':
                    self.buf_o.append(data)
                elif first_char=='H' or first_char=='A' or first_char=='J' or first_char=='S':
                    self.buf_m.append(data)
                elif first_char=='E' or first_char=='g':
                    self.buf_m.append(data)
                else: 
                    print('Incorrect comand: ')
                    print(data.decode('utf-8'))
            time.sleep(0.005)
           