import serial
import sys 
import time
import json
import random
import threading
from multiprocessing import process

lock = threading.Lock()
#m- motion
#s- status
#o- output

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
        self.usb.write(data) #to musi byc stringS

    def loopRecive(self):
        while 1==1:
            lock.acquire()
            print(threading.currentThread())
            print (self.usb.inWaiting())
            if self.usb.in_waiting != 0:
                data = self.usb.readline()
                first_char =  data[:1].decode('utf-8')

                if first_char=='g' or first_char=='T' or first_char=='F':
                    self.buf_s.append(data)
                elif first_char=='L' or first_char=='I' or first_char=='D':
                    self.buf_s.append(data)
                elif first_char=='H' or first_char=='A' or first_char=='J' or first_char=='S' or first_char=='Y':
                    self.buf_s.append(data)
                else: 
                    print('Incorrect comand: ')
                    print(data.decode('utf-8'))

            lock.release()
           
                # motion_test()

def random_test(group, cmd, y):
    x = random.randint(1,y)
    name = ('tests/{}_{}_{}.json'.format(group, cmd, x))
    print('Test name: {}'.format(name))
    with open(name) as json_file:
        data = json.load(json_file)
    return data 

def motion_test():
    while 1==1:
        lock.acquire()
        print(threading.currentThread())
        print("lalala")
        cmd_list = ["H","A","J","S","Y"]
        cmd = random.choice(cmd_list)
        cmd = "S"
        data = random_test('test_drive', cmd, 3)
        test_list = data["CMDS"]
        
        for x in test_list:
            if x["DIR"] == 'T':
                cmd_to_send = x["CMD_TO_SEND"].encode('utf-8')
                print(cmd_to_send)
                USB.send(cmd_to_send)
            elif x["DIR"] == 'R':
                t = time.time()

                while time.time() > t+x["TIMEOUT"]:
                    if len(USB.buf_m) != 0:
                        answ = USB.buf_m.pop()

                        if answ[1:] ==  x["CMD"] and answ[:2] == x["VAL"]:
                            print("OKEY")
                    else: print("Timeout")
        lock.release()

        time.sleep(1)

def state_test():
    pass

def output_test():
    pass

if __name__=='__main__':


    USB = USB_serial()
    th1 = threading.Thread(target = USB.loopRecive) 
    th2 = threading.Thread(target = motion_test) 

    th1.start()
    th2.start()

    th1.join()
    th2.join()
    
    
  

    

# print(data["BOUND"])
# y=json.dumps(data)
# print(y)
# USB.usb.write(b"start")
# print(usb_serial.name)

